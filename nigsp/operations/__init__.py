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
from .graph import zerocross, nodestrength
from .laplacian import symmetric_normalisation, decomposition
from .metrics import sdi, gsdi
from .nifti import (vol_to_mat, mat_to_vol, apply_mask, unmask, apply_atlas,
                    unfold_atlas)
from .surrogates import (random_sign, sc_informed, sc_uninformed,
                         test_significance)
from .timeseries import (normalise_ts, graph_fourier_transform,
                         median_cutoff_frequency_idx, graph_filter,
                         functional_connectivity)
