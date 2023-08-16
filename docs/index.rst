.. nigsp documentation master file, created by
   sphinx-quickstart on Tue Jul 12 11:04:40 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root ``toctree`` directive.

:hide-toc:

NiGSP (NeuroImaging Graph Signal Processing)
============================================

|Latest version| |Release date| |Auto Release|

|See the documentation at: https://nigsp.readthedocs.io| |Latest DOI|
|Licensed Apache 2.0|

|Codecov| |Build Status| |Documentation Status|

|image1| |Supports python version|

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
Zenodo DOI |general Zenodo :hide-toc:DOI| or the Zenodo DOI related to the version
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



.. |Latest version| image:: https://img.shields.io/github/v/release/MIPLabCH/nigsp?style=flat&logo=github&sort=semver
   :target: https://github.com/MIPLabCH/nigsp/releases
.. |Release date| image:: https://img.shields.io/github/release-date/MIPLabCH/nigsp?style=flat&logo=github
   :target: https://github.com/MIPLabCH/nigsp/releases
.. |Auto Release| image:: https://img.shields.io/badge/release-auto.svg?style=flat&colorA=888888&colorB=9B065A&label=auto&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAACzElEQVR4AYXBW2iVBQAA4O+/nLlLO9NM7JSXasko2ASZMaKyhRKEDH2ohxHVWy6EiIiiLOgiZG9CtdgG0VNQoJEXRogVgZYylI1skiKVITPTTtnv3M7+v8UvnG3M+r7APLIRxStn69qzqeBBrMYyBDiL4SD0VeFmRwtrkrI5IjP0F7rjzrSjvbTqwubiLZffySrhRrSghBJa8EBYY0NyLJt8bDBOtzbEY72TldQ1kRm6otana8JK3/kzN/3V/NBPU6HsNnNlZAz/ukOalb0RBJKeQnykd7LiX5Fp/YXuQlfUuhXbg8Di5GL9jbXFq/tLa86PpxPhAPrwCYaiorS8L/uuPJh1hZFbcR8mewrx0d7JShr3F7pNW4vX0GRakKWVk7taDq7uPvFWw8YkMcPVb+vfvfRZ1i7zqFwjtmFouL72y6C/0L0Ie3GvaQXRyYVB3YZNE32/+A/D9bVLcRB3yw3hkRCdaDUtFl6Ykr20aaLvKoqIXUdbMj6GFzAmdxfWx9iIRrkDr1f27cFONGMUo/gRI/jNbIMYxJOoR1cY0OGaVPb5z9mlKbyJP/EsdmIXvsFmM7Ql42nEblX3xI1BbYbTkXCqRnxUbgzPo4T7sQBNeBG7zbAiDI8nWfZDhQWYCG4PFr+HMBQ6l5VPJybeRyJXwsdYJ/cRnlJV0yB4ZlUYtFQIkMZnst8fRrPcKezHCblz2IInMIkPzbbyb9mW42nWInc2xmE0y61AJ06oGsXL5rcOK1UdCbEXiVwNXsEy/6+EbaiVG8eeEAfxvaoSBnCH61uOD7BS1Ul8ESHBKWxCrdyd6EYNKihgEVrwOAbQruoytuBYIFfAc3gVN6iawhjKyNCEpYhVJXgbOzARyaU4hCtYizq5EI1YgiUoIlT1B7ZjByqmRWYbwtdYjoWoN7+LOIQefIqKawLzK6ID69GGpQgwhhEcwGGUzfEPAiPqsCXadFsAAAAASUVORK5CYII=
   :target: https://github.com/intuit/auto
.. |See the documentation at: https://nigsp.readthedocs.io| image:: https://img.shields.io/badge/docs-read%20latest-informational?style=flat&logo=readthedocs
   :target: https://nigsp.readthedocs.io/en/latest/?badge=latest
.. |Latest DOI| image:: https://zenodo.org/badge/446805866.svg?style=flat&logo=zenodo
   :target: https://zenodo.org/badge/latestdoi/446805866
.. |Licensed Apache 2.0| image:: https://img.shields.io/github/license/MIPLabCH/nigsp?style=flat&logo=apache
   :target: https://github.com/MIPLabCH/nigsp/blob/master/LICENSE
.. |Codecov| image:: https://img.shields.io/codecov/c/gh/MIPlabCH/nigsp?style=flat&label=codecov&logo=codecov
   :target: https://codecov.io/gh/MIPLabCH/nigsp
.. |Build Status| image:: https://img.shields.io/circleci/build/github/MIPLabCH/nigsp?style=flat&label=circleci&logo=circleci
   :target: https://circleci.com/gh/MIPLabCH/nigsp
.. |Documentation Status| image:: https://img.shields.io/readthedocs/nigsp?style=flat&label=readthedocs&logo=readthedocs
   :target: https://nigsp.readthedocs.io/en/latest/?badge=latest
.. |image1| image:: https://img.shields.io/pypi/v/nigsp?style=flat&logo=pypi&logoColor=white
   :target: https://pypi.org/project/nigsp/
.. |Supports python version| image:: https://img.shields.io/pypi/pyversions/nigsp?style=flat&logo=python&logoColor=white
   :target: https://pypi.org/project/nigsp/
.. |All Contributors| image:: https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat
   :target: #contributors
.. |general Zenodo DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.6373436.svg
   :target: https://zenodo.org/badge/latestdoi/446805866

.. toctree::
   :caption: Usage
   :hidden:
   :maxdepth: 2

   Installation <usage/installation>
   User Guide <usage/user_guide>
   Command Line Interface (CLI) <usage/cli>
   Output <usage/output>
   Licence <usage/licence>

.. toctree::
   :caption: API
   :hidden:
   :maxdepth: 1
   :glob:

   api/*

.. toctree::
   :caption: Graph Signal Processing
   :hidden:
   :maxdepth: 1

   About GSP <about_gsp>

.. toctree::
   :caption: Developers
   :hidden:
   :maxdepth: 1

   How to Contribute <developers/how_to_contribute>
   Contributor Guide <developers/contributor_guide>
   Code of Conduct <developers/code_of_conduct>
