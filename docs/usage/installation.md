Installation
============

Install on any `*nix` system using python and pip, or clone this repository and install locally (run setup.py or pip).
Currently, the only necessary dependency is `numpy`. However, to gain access to more features, other libraries might be required.
It's easy to install them through pip.
`nigsp` supports python versions 3.6+. However, please note that tests are run on python 3.7+.

## Install with `pip` (recommended)

:exclamation::exclamation::exclamation: Please note that some systems might require to use `pip3` instead of `pip`.

### Basic installation:
For basic installation, simply run:
```shell
$ pip install nigsp
```

### Richer installation
To install the dependencies to enable more features, you can append labels to `nigsp`, e.g:
```shell
$ pip install nigsp[nifti]
```


The possible features are:

-  `[mat]`: to load and export MATLAB (`.mat`) files.
-  `[nifti]`: to load and export nifti (`.nii` and `.nii.gz`) files.
-  `[viz]`: to allow the creation of various plots during the workflow.
-  `[all]`: to install all of the above.

## Clone from Github / install without `pip`

:exclamation::exclamation::exclamation: Please note that `nigsp` is continuously deployed, i.e. the latest feature available are immediately released on PyPI.
To install `nigsp` from Github, clone the repository first, then move to the cloned folder and run:
```shell
$ python setup.py install
```

Alternatively, `pip` can be used too:
```shell
$ pip install .
```

## Check `nigsp` installation

You can check if `nigsp` was installed correctly from a shell terminal:
```shell
$ nigsp --help
```

Alternatively, import it in python and check the version

```python
import nigsp

nigsp.__version__
```
