.. _api:

.. currentmodule:: nigsp


nigsp package
=============

:mod:`nigsp.workflow` - Primary workflows
-----------------------------------------

.. currentmodule:: nigsp.workflow

.. autosummary::
   :template: function.rst
   :toctree: generated/

   nigsp

:mod:`nigsp.operations.graph` - Operations on graphs
----------------------------------------------------

.. currentmodule:: nigsp.operations.graph

.. autosummary::
   :template: function.rst
   :toctree: generated/

   zerocross
   nodestrength

:mod:`nigsp.operations.laplacian` - Operations on/for Laplacians
----------------------------------------------------------------

.. currentmodule:: nigsp.operations.laplacian

.. autosummary::
   :template: function.rst
   :toctree: generated/

   compute_laplacian
   normalisation
   symmetric_normalised_laplacian
   decomposition
   recomposition

:mod:`nigsp.operations.metrics` - Metrics computation
-----------------------------------------------------

.. currentmodule:: nigsp.operations.metrics

.. autosummary::
   :template: function.rst
   :toctree: generated/

   sdi
   gsdi
   functional_connectivity

:mod:`nigsp.operations.nifti` - Operations on nifti-like data
-------------------------------------------------------------

.. currentmodule:: nigsp.operations.nifti

.. autosummary::
   :template: function.rst
   :toctree: generated/

   vol_to_mat
   mat_to_vol
   apply_mask
   unmask
   apply_atlas
   unfold_atlas

:mod:`nigsp.operations.surrogates` - Surrogate computations and testing
-----------------------------------------------------------------------

.. currentmodule:: nigsp.operations.surrogates

.. autosummary::
   :template: function.rst
   :toctree: generated/

   random_sign
   sc_informed
   sc_uninformed
   test_significance

:mod:`nigsp.operations.timeseries` - Operations on/involving timeseries
-----------------------------------------------------------------------

.. currentmodule:: nigsp.operations.timeseries

.. autosummary::
   :template: function.rst
   :toctree: generated/

   normalise_ts
   spc_ts
   demean_ts
   rescale_ts
   resize_ts
   graph_fourier_transform
   median_cutoff_frequency_idx
   graph_filter

:mod:`nigsp.io` - I/O functions: checks
---------------------------------------

.. currentmodule:: nigsp.io

.. autosummary::
   :template: function.rst
   :toctree: generated/

   check_ext
   check_nifti_dim
   check_mtx_dim

:mod:`nigsp.io` - I/O functions: load
-------------------------------------

.. currentmodule:: nigsp.io

.. autosummary::
   :template: function.rst
   :toctree: generated/

   load_nifti_get_mask
   load_txt
   load_mat
   load_xls

:mod:`nigsp.io` - I/O functions: export
---------------------------------------

.. currentmodule:: nigsp.io

.. autosummary::
   :template: function.rst
   :toctree: generated/

   export_nifti
   export_txt
   export_mtx

:mod:`nigsp.io` - I/O functions: supported extensions
-----------------------------------------------------

.. currentmodule:: nigsp.io

.. autosummary::
   :template: attribute.rst
   :toctree: generated/

   EXT_1D
   EXT_MAT
   EXT_NIFTI
   EXT_XLS

:mod:`nigsp.viz` - Visualisations
---------------------------------

.. currentmodule:: nigsp.viz

.. autosummary::
   :template: function.rst
   :toctree: generated/

   plot_connectivity
   plot_greyplot
   plot_nodes
   plot_edges

:mod:`nigsp.utils` - Utility functions
--------------------------------------

.. currentmodule:: nigsp.utils

.. autosummary::
   :template: function.rst
   :toctree: generated/

   pairwise
   change_var_type
   prepare_ndim_iteration

:mod:`nigsp.objects` - Data objects
----------------------------------------------

.. automodule:: nigsp.objects
   :no-members:
   :no-inherited-members:

.. currentmodule:: nigsp.objects

.. autosummary::
   :template: class.rst
   :toctree: generated/

   SCGraph

:mod:`nigsp.blocks` - Workflow blocks
-------------------------------------

.. currentmodule:: nigsp.blocks

.. autosummary::
   :template: function.rst
   :toctree: generated/

   nifti_to_timeseries
   export_metric
   plot_metric
