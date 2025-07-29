from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("chaostoolkit-fault")
except PackageNotFoundError:
    __version__ = "unknown"
