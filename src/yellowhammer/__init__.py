from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("yellowhammer")
except PackageNotFoundError:
    __version__ = "develop"

__all__ = ("__version__",)
