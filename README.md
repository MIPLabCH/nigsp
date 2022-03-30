NiGSP
=====

[![Latest version](https://img.shields.io/pypi/v/nigsp?style=flat&logo=pypi)](https://pypi.org/project/nigsp/)
[![Latest DOI](https://zenodo.org/badge/446805866.svg?style=flat&logo=zenodo&label=Latest_DOI)](https://zenodo.org/badge/latestdoi/446805866)
[![Licensed Apache 2.0](https://img.shields.io/github/license/MIPLabCH/nigsp?style=flat)](https://github.com/MIPLabCH/nigsp/blob/master/LICENSE)

[![Codecov](https://codecov.io/gh/MIPLabCH/nigsp/branch/master/graph/badge.svg?style=flat&logo=codecov)](https://codecov.io/gh/MIPLabCH/nigsp)
[![Build Status](https://circleci.com/gh/MIPLabCH/nigsp.svg?style=shield&logo=circleci)](https://circleci.com/gh/MIPLabCH/nigsp)
<!--[![See the documentation at: https://nigsp.readthedocs.io](https://readthedocs.org/projects/nigsp/badge/?version=latest)](https://nigsp.readthedocs.io/en/latest/?badge=latest) -->

[![Auto Release](https://img.shields.io/badge/release-auto.svg?colorA=888888&colorB=9B065A&label=auto)](https://github.com/intuit/auto)
[![Supports python version](https://img.shields.io/pypi/pyversions/nigsp?style=shield&logo=python)](https://pypi.org/project/nigsp/)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat)](#contributors)
<!-- ALL-CONTRIBUTORS-BADGE:END -->


A python library (and toolbox!) to run Graph Signal Processing on multimodal MRI data.

**The project is currently under development stage alpha**.
Any suggestion/bug report is welcome! Feel free to open an issue.

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

Documentation
=============

Full documentation coming soon!

Cite
----

If you use `nigsp` in your work, please cite either the all-time Zenodo DOI [![general Zenodo DOI](https://zenodo.org/badge/110845855.svg)](https://zenodo.org/badge/latestdoi/110845855) or the Zenodo DOI related to the version you are using.
Please cite the following paper(s) too:
> Preti, M.G., Van De Ville, D. _Decoupling of brain function from structure reveals regional behavioral specialization in humans_. Nat Commun 10, 4747 (2019). https://doi.org/10.1038/s41467-019-12765-7.

If you are using the Couple/Decoupled Functional Connectivity, please cite also:
> Griffa, A., et al. _Brain structure-function coupling provides signatures for task decoding and individual fingerprinting_. NeuroImage 250, 118970 (2022). https://doi.org/10.1016/j.neuroimage.2022.118970.

Installation
------------

Install on any `*nix` system using python and pip, or clone this repository and install locally (run setup.py or pip).
Currently, the only necessary dependency is `numpy`. However, to gain access to more features, other libraries might be required.
It's easy to install them through pip.
`nigsp` supports python versions 3.6+. However, please note that tests are run on python 3.7+.

### Install with `pip` (recommended)

:exclamation::exclamation::exclamation: Please note that some systems might require to use `pip3` instead of `pip`.

#### Basic installation:
For basic installation, simply run:
```bash
pip install nigsp
```

#### Richer installation
To install the dependencies to enable more features, you can append labels to `nigsp`, e.g:
```bash
pip install nigsp[nifti]
```

The possible features are:
- `[mat]`: to load and export MATLAB (`.mat`) files.
- `[nifti]`: to load and export nifti (`.nii` and `.nii.gz`) files.
- `[viz]`: to allow the creation of various plots during the workflow.
- `[all]`: to install all of the above.

### Clone from Github / install without `pip`

:exclamation::exclamation::exclamation: Please note that `nigsp` is continuously deployed, i.e. the latest feature available are immediately released on PyPI.
To install `nigsp` from Github, clone the repository first, then move to the cloned folder and run:
```bash
python setup.py install
```

Alternatively, `pip` can be used too:
```bash
pip install .
```

### Developer installation

To be sure you have everything installed to develop (and test) `nigsp`, **fork** `MIPLabCH/nigsp` to your repository, then clone it locally and move inside the cloned folder. Finally, install with `pip` using the developer mode and the `[dev]` label:
```bash
pip install -e .[dev]
```


Run/use `nigsp`
---------------

You can run the `nigsp` workflow in a shell session (or in your code) - just follow the help:
```shell
nigsp --help
```

Alternatively, you can use nigsp as a module in a python session (or within your python script):
```python
import nigsp

nigsp.__version__
```

Full API coming soon.


<!-- ## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)): -->

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->


<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->


License
-------

Copyright 2022, Stefano Moia.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

