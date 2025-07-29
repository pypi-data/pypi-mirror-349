# -*- coding: utf-8 -*-
import logging
import os
import shlex
import shutil
import subprocess  # nosec
import threading
import time
from typing import Tuple

import psutil
from chaoslib import decode_bytes
from chaoslib.exceptions import ActivityFailed

__all__ = ["run_proxy", "stop_proxy", "run_demo"]

logger = logging.getLogger("chaostoolkit")
lock = threading.Lock()

PROCS: dict[str, psutil.Process] = {}


def run_proxy(
    proxy_args: str,
    verbose: bool = False,
) -> Tuple[int, str, str]:
    """
    Run the fault proxy with the given command line arguments. Use the
    name argument to track the started process, this can be used to call
    `stop_proxy` from a rollback action.

    The function will set the `FAULT_HTTP_PROXY_ADDRESS` to the actual proxy
    bound address. You can reuse this information from subsequent actions
    to point your clients to it.

    See https://fault-project.com/reference/cli-commands/#run for all proxy
    arguments.
    """
    fault_path = shutil.which("fault")
    if not fault_path:
        raise ActivityFailed("fault cli: not found")

    cmd = [fault_path]
    if verbose:
        cmd.extend(["--log-stdout", "--log-level", "debug"])
    else:
        cmd.extend(["--log-stdout"])
    cmd.extend(["run"])

    if "--proxy-address" not in proxy_args:
        cmd.extend(["--proxy-address", "0.0.0.0:3180"])

    if "--upstream" not in proxy_args:
        cmd.extend(["--upstream", "*"])

    cmd.extend(shlex.split(proxy_args))

    env = {}  # type: dict[str, str]
    stdout = stderr = b""
    try:
        logger.debug(f"Running fault proxy: '{shlex.join(cmd)}'")
        p = psutil.Popen(  # nosec
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            shell=False,
        )

        while not p.is_running():
            time.sleep(0.1)

        logger.debug(f"fault proxy is now running with PID {p.pid}")
        logger.debug("fault guessing proxy listening address")

        bound_proxy_addr = ""
        for _ in range(10):
            if bound_proxy_addr:
                break

            time.sleep(0.1)

            for c in p.net_connections():
                if c.status == "LISTEN":
                    addr = c.laddr
                    bound_proxy_addr = f"http://{addr[0]}:{addr[1]}"
                    logger.debug(f"fault proxy listening on {bound_proxy_addr}")
                    break

        if bound_proxy_addr:
            logger.debug(f"fault proxy env variables to {bound_proxy_addr}")
            os.environ["FAULT_HTTP_PROXY_ADDRESS"] = bound_proxy_addr
            os.environ["OHA_HTTP_PROXY"] = bound_proxy_addr
            os.environ["OHA_HTTPS_PROXY"] = bound_proxy_addr

        with lock:
            PROCS["proxy"] = p

        stdout, stderr = p.communicate(timeout=None)
    except KeyboardInterrupt:
        logger.debug(
            "Caught SIGINT signal while running load test. Ignoring it."
        )
    finally:
        try:
            p.terminate()
        except psutil.NoSuchProcess:
            pass
        finally:
            with lock:
                PROCS.pop("proxy", None)

            code = p.returncode

            if code != 0:
                logger.error(
                    f"Failed to launch fault proxy {code}: "
                    f"STDOUT: {decode_bytes(stdout)}"
                    "\n"
                    f"STDERR: {decode_bytes(stderr)}"
                )

                raise ActivityFailed(f"fault proxy process failed: {code}")

            return (code, decode_bytes(stdout), decode_bytes(stderr))


def stop_proxy() -> None:
    """
    Terminate the fault proxy
    """
    with lock:
        p = PROCS.pop("proxy", None)
        if p is not None:
            try:
                p.terminate()
            except psutil.Error:
                pass

        logger.debug("Unset fault proxy env variables")
        os.environ.pop("FAULT_HTTP_PROXY_ADDRESS", None)
        os.environ.pop("OHA_HTTP_PROXY", None)
        os.environ.pop("OHA_HTTPS_PROXY", None)


def run_demo(
    duration: float | None = None, port: int = 7070
) -> Tuple[int, str, str]:
    """
    Run the fault demo web application.
    """
    fault_path = shutil.which("fault")
    if not fault_path:
        raise ActivityFailed("fault: not found")

    cmd = [fault_path]
    cmd.extend(["demo", "run", "0.0.0.0", str(port)])

    env: dict[str, str] = {}

    proxy_addr = os.getenv("FAULT_HTTP_PROXY_ADDRESS")

    if proxy_addr:
        env["HTTP_PROXY"] = proxy_addr
        env["HTTPS_PROXY"] = proxy_addr

    stdout = stderr = b""
    try:
        logger.debug(f"Running fault demo: '{shlex.join(cmd)}'")
        p = psutil.Popen(  # nosec
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            shell=False,
        )

        stdout, stderr = p.communicate(timeout=duration)
    except KeyboardInterrupt:
        logger.debug(
            "Caught SIGINT signal while running load test. Ignoring it."
        )
    except subprocess.TimeoutExpired:
        pass
    finally:
        try:
            p.terminate()
        except psutil.NoSuchProcess:
            pass
        finally:
            code = p.returncode

            if code != 0:
                logger.error(
                    f"Failed to launch fault demo {code}: "
                    f"STDOUT: {decode_bytes(stdout) or ''}"
                    "\n"
                    f"STDERR: {decode_bytes(stderr) or ''}"
                )

                raise ActivityFailed(f"fault demo process failed: {code}")

            return (code, decode_bytes(stdout), decode_bytes(stderr))
