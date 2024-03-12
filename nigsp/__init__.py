from . import (
    blocks,
    cli,
    due,
    io,
    objects,
    operations,
    references,
    utils,
    viz,
    workflow,
)
from ._version import get_versions
from .cli import run
from .operations import graph, laplacian, metrics, nifti, surrogates, timeseries

SKIP_MODULES = ["tests"]

__version__ = get_versions()["version"]
del get_versions
