from ._version import get_versions
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

__version__ = get_versions()["version"]
del get_versions
