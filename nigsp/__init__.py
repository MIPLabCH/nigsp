"""Hopefully importing everything."""

import pkgutil

from ._version import get_versions
from .operations import graph, laplacian, metrics, nifti, surrogates, timeseries

SKIP_MODULES = ["tests"]

__version__ = get_versions()["version"]
del get_versions

__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    if "tests" not in module_name:
        __all__.append(module_name)
        _module = loader.find_module(module_name).load_module(module_name)
        globals()[module_name] = _module
