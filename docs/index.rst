.. nigsp documentation master file, created by
   sphinx-quickstart on Tue Jul 12 11:04:40 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

NiGSP (NeuroImaging Graph Signal Processing)
============================================

|Latest version| |Latest DOI| |Licensed Apache 2.0|

|Codecov| |Build Status|

|Auto Release| |Supports python version|

|All Contributors|


A python library (and toolbox!) to run Graph Signal Processing on
multimodal MRI data.

**The project is currently under development stage alpha**. Any
suggestion/bug report is welcome! Feel free to open an issue.

This project follows the
`all-contributors <https://github.com/all-contributors/all-contributors>`__
specification. Contributions of any kind welcome!

Cite
----

If you use ``nigsp`` in your work, please cite either the all-time
Zenodo DOI |general Zenodo DOI| or the Zenodo DOI related to the version
you are using. Please cite the following paper(s) too:

   Preti, M.G., Van De Ville, D. *Decoupling of brain function from
   structure reveals regional behavioral specialization in humans*. Nat
   Commun 10, 4747 (2019).
   `https://doi.org/10.1038/s41467-019-12765-7 <https://doi.org/10.1038/s41467-019-12765-7>`__.

If you are using the Couple/Decoupled Functional Connectivity, please
cite also:

   Griffa, A., et al. *Brain structure-function coupling provides
   signatures for task decoding and individual fingerprinting*.
   NeuroImage 250, 118970 (2022).
   `https://doi.org/10.1016/j.neuroimage.2022.118970 <https://doi.org/10.1016/j.neuroimage.2022.118970>`__.



.. |Latest version| image:: https://img.shields.io/pypi/v/nigsp?style=flat&logo=pypi
   :target: https://pypi.org/project/nigsp/
.. |Latest DOI| image:: https://zenodo.org/badge/446805866.svg?style=flat&logo=zenodo&label=Latest_DOI
   :target: https://zenodo.org/badge/latestdoi/446805866
.. |Licensed Apache 2.0| image:: https://img.shields.io/github/license/MIPLabCH/nigsp?style=flat
   :target: https://github.com/MIPLabCH/nigsp/blob/master/LICENSE
.. |Codecov| image:: https://codecov.io/gh/MIPLabCH/nigsp/branch/master/graph/badge.svg?style=flat&logo=codecov
   :target: https://codecov.io/gh/MIPLabCH/nigsp
.. |Build Status| image:: https://circleci.com/gh/MIPLabCH/nigsp.svg?style=shield&logo=circleci
   :target: https://circleci.com/gh/MIPLabCH/nigsp
.. |Auto Release| image:: https://img.shields.io/badge/release-auto.svg?colorA=888888&colorB=9B065A&label=auto
   :target: https://github.com/intuit/auto
.. |Supports python version| image:: https://img.shields.io/pypi/pyversions/nigsp?style=shield&logo=python
   :target: https://pypi.org/project/nigsp/
.. |All Contributors| image:: https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat
   :target: #contributors
.. |general Zenodo DOI| image:: https://zenodo.org/badge/110845855.svg
   :target: https://zenodo.org/badge/latestdoi/110845855



.. toctree::
   :titlesonly:
   :maxdepth: 0
   :hidden:

   NiGSP <self>

.. toctree::
   :caption: Usage
   :maxdepth: 5
   :hidden:

   Installation <usage/installation>
   User Guide <usage/user_guide>
   Command Line Interface (CLI) <usage/cli>
   Output <usage/output>
   Licence <usage/licence>

.. toctree::
   :caption: API
   :maxdepth: 5
   :hidden:

   api/workflow
   api/objects
   api/io
   api/viz
   api/utils
   api/blocks
   api/operations

.. toctree::
   :caption: Graph Signal Processing
   :maxdepth: 5
   :hidden:

   About GSP <about_gsp>

.. toctree::
   :caption: Developers
   :maxdepth: 5
   :hidden:

   How to Contribute <developers/how_to_contribute>
   Contributor Guide <developers/contributor_guide> 
   Code of Conduct <developers/code_of_conduct>
