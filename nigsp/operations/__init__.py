"""
The core functions of `nigsp`.

They are organised into modules by type of operation.

Each function is callable through their respective module or directly
as an `operations` function, and each module can be called directly as a
`nigsp` module.

For example, calling `nigsp.operations.metrics.sdi` is equivalent to calling
`nigsp.operations.sdi` or `nigsp.metrisc.sdi`.
"""


# Import all operations.
from .graph import nodestrength, zerocross
from .laplacian import decomposition, symmetric_normalised_laplacian
from .metrics import functional_connectivity, gsdi, sdi
from .nifti import apply_atlas, apply_mask, mat_to_vol, unfold_atlas, unmask, vol_to_mat
from .surrogates import random_sign, sc_informed, sc_uninformed, test_significance
from .timeseries import (
    graph_filter,
    graph_fourier_transform,
    median_cutoff_frequency_idx,
    normalise_ts,
)
