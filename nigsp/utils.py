#!/usr/bin/env python3
"""
General utils.

Attributes
----------
LGR
    Logger
"""

import logging
from itertools import tee

from numpy import asarray, empty, ndarray, prod

LGR = logging.getLogger(__name__)


def pairwise(iterable):
    """
    Recreate `itertools.pairwise` behaviour for python < 3.10 compatibility.

    Parameters
    ----------
    iterable : any iterable object
        The object to iterate through

    Returns
    -------
    tuple
        The couple of adjacent elements

    Notes
    -----
    The original function is: https://docs.python.org/3/library/itertools.html#itertools.pairwise
    Credit to the Python Software Foundation, this function is under BSD licence.
    To be replaced by itertools' pairwise import once support for python < 3.10 is dropped
    """
    a, b = tee(iterable, 2)
    next(b, None)
    return zip(a, b)


def change_var_type(var, dtype, varname="an input variable", stop=True, silent=False):
    """
    Make sure `var` is of type `dtype`.

    Parameters
    ----------
    var : str, int, or float
        Variable to change type of
    dtype : type
        Type to change `var` to
    varname : str, optional
        The name of the variable
    stop : bool, optional
        If True, raises TypeError if `var` is not of `dtype`
    silent : bool, optional
        If True, don't return any message

    Returns
    -------
    int, float, str, list, or var
        The given `var` in the given `dtype`, or `var` if '' or None

    Raises
    ------
    NotImplementedError
        If dtype is not int, float, str, or list
    TypeError
        If variable var is not of type and stop is True
    """
    if type(var) is not dtype and stop:
        if varname != "an input variable":
            varname = f"variable {varname}"
        raise TypeError(f"{varname} is not of type {dtype}")

    if dtype is int:
        tmpvar = int(var)
    elif dtype is float:
        tmpvar = float(var)
    elif dtype is str:
        tmpvar = str(var)
    elif dtype is ndarray:
        tmpvar = asarray(var)
    elif dtype is list:
        if type(var) is list:
            tmpvar = var
        else:
            tmpvar = [var]
    else:
        raise NotImplementedError(f"Type {dtype.__name__} not supported")

    if type(tmpvar) is not type(var):
        if varname != "an input variable":
            varname = f"variable {varname}"
        msg = f"Changing type of {varname} from {type(var)} to {dtype}"

        if silent:
            LGR.debug(msg)
        else:
            LGR.warning(msg)

    return tmpvar


def prepare_ndim_iteration(data, idx):
    """
    Reshape data to have idx+1 dimensions.

    This should allow iterations over unknown numbers of dimensions above idx
    when needed.

    Parameters
    ----------
    data : np.ndarray
        The data to reiterate over
    idx : int
        The number of dimensions that should be fixed

    Returns
    -------
    np.ndarray, np.ndarray
        The reshaped data and an empty array like it.
    """
    if data.ndim > idx + 1:
        new_shape = list(data.shape[:idx]) + [prod(data.shape[idx:])]
        data = data.reshape(new_shape)

    return data, empty(data.shape, dtype="float32")


"""
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
"""
