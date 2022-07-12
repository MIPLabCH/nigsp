Getting Started!
================

First of all: thank you!

Contributions can be made in different ways, not only code! As we follow
the
[all-contributors](https://github.com/all-contributors/all-contributors)
specification, any contribution will be recognised accordingly.

Follow these steps to get started:

1.  Have a look at the [contributor guide](contributor_guide.md) page as
    well as the [code of conduct](code_of_conduct.md).
2.  Make sure that you have a GitHub account. You can set up a [free
    GitHub account](https://github.com/); here are some
    [instructions](https://help.github.com/articles/signing-up-for-a-new-github-account).
3.  If you intend to contribute code and/or use the `nigsp` packages
    in any way, check that you have `git` and `pip` installed on your
    system. Then install the package as a developer. This will let you
    run the program with the latest modifications, without requiring to
    re-install it every time.

!!! note
    The following instructions are provided assuming that python 3 is
    **not** your default version of python. If it is, you might need to use
    `pip` instead of `pip3`, although some OSs do adopt `pip3` anyway. If
    you want to check your OS behaviour, type `python --version` in a terminal.


## Linux, Mac, and Windows developer installation

Be sure to have `git` and `pip` installed. Fork the `nigsp` repository
in GitHub, then open a terminal and run the following code to clone the
forked repository and set it as your *origin*:

```shell
$ git clone https://github.com/{username}/nigsp.git
# or in case you prefer to use ssh:
$ git clone git@github.com:{username}/nigsp.git
```

We also recommend to set up the [`MIPLabCH/nigsp`](https://github.com/MIPLabCH/nigsp) repository as
*upstream*. In this way you can always keep your main branch
up to date with the command *git pull upstream master*:

```shell
$ cd nigsp
$ git remote add upstream https://github.com/physiopy/{physiopy-package}.git
$ git pull upstream master
```

## Full developer installation

If it's your first experience as a python developer, or you just want
to be sure that you have everything you need to work on `nigsp`, you
can install it with all the other packages that are frequently
used during development in one step!

Go to the `nigsp` repository folder and execute the command:

```shell
$ cd nigsp
$ pip3 install -e .[dev]
```

This will install:

- `nigsp` as an editable package, which means that you can
 modify the program and run it without having to reinstall it every
 time!
- All `nigsp` required dependencies.
- All `nigsp` optional dependencies:
    + All packages used for **filetypes I/O** (`pymatreader`, `scipy`, `nibabel`)
    + All packages used for **visualisation and plotting** (`matplotlib`, `nilearn`)
- All **documentation** modules (`mkdocs` based), so that you can
 build the docs locally before submitting them.
- All **test** modules (`pytest`, `coverage`), in order for you to test your
 code locally before committing it!

## Check your installation!

Type the commands:

```shell
$ cd nigsp
$ pytest
```

This will execute the tests locally and check that your phys2bids
installation works properly - it should look like this:

```
==================================== test session starts ====================================
platform linux -- Python 3.7.13, pytest-7.1.1, pluggy-1.0.0
rootdir: /home/nemo/Scrivania/gitlab/nigsp, configfile: setup.cfg
plugins: cov-3.0.0
collected 56 items

nigsp/tests/test_graph.py ..                                                           [  3%]
nigsp/tests/test_integration.py .                                                      [  5%]
nigsp/tests/test_io.py ..........................                                      [ 51%]
nigsp/tests/test_nifti.py ...........                                                  [ 71%]
nigsp/tests/test_utils.py ................                                             [100%]

============================== 56 passed in 96.57s (0:01:36) ================================

```

Do **not** worry if there is a xfail error in the log. This happens when
we know that a test will fail for known reasons, and we are probably
working to fix it (see
[here](https://docs.pytest.org/en/latest/skipping.html#xfail-mark-test-functions-as-expected-to-fail)).
However, if you do encounter any other error, check that you are connected to internet, you have all the extra dependencies installed, and their version meets `nigsp`
requirements.
