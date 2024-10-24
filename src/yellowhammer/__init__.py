from importlib.metadata import PackageNotFoundError, version
from .magics import DatalabMagics

try:
    __version__ = version("yellowhammer")
except PackageNotFoundError:
    __version__ = "develop"

__all__ = ("__version__",)


def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    ipython.register_magics(DatalabMagics)
