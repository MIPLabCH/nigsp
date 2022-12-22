#!/usr/bin/env python3
"""
I/O and related utils.

Attributes
----------
EXT_1D : list
    List of supported TXT/1D file extensions, in lower case.
EXT_MAT : list
    List of supported matlab file extensions, in lower case.
EXT_NIFTI : list
    List of supported nifti file extensions, in lower case.
EXT_XLS : list
    List of supported XLS-like file extensions, in lower case.
LGR
    Logger
"""

import logging
from os import makedirs
from os.path import exists, join

import numpy as np

from nigsp.utils import change_var_type

EXT_1D = [".txt", ".csv", ".tsv", ".1d", ".par", ".tsv.gz", ".csv.gz"]
EXT_XLS = [".xls"]
EXT_MAT = [".mat"]
EXT_NIFTI = [".nii", ".nii.gz"]
EXT_ALL = EXT_1D + EXT_XLS + EXT_MAT + EXT_NIFTI

EXT_DICT = {"1D": EXT_1D, "xls": EXT_XLS, "mat": EXT_MAT, "nifti": EXT_NIFTI}

LGR = logging.getLogger(__name__)


def check_ext(all_ext, fname, scan=False, remove=False):
    """
    Check which extension a file has, and possibly remove it.

    Parameters
    ----------
    all_ext : list
        All possible extensions to check within
    fname : str or os.PathLikeLike
        The filename to check
    scan : bool, optional
        Scan the given path to see if there is a file with that extension
        If True and no path declared, check if fname has a path, if not scan '.'
        If False, don't scan any folder
    remove : bool, optional
        Remove the extention from fname if it has one

    Returns
    -------
    obj_return : Uses a list to return variable amount of options.
        has_ext : boolean
            True if the extension is found, false otherwise
        fname : str or os.PathLike
            If `remove` is True, return (extensionless) fname
        ext : str
            If both `remove` and `has_ext` are True, returns also found extension
    """
    has_ext = False
    all_ext = change_var_type(all_ext, list, stop=False, silent=True)
    for ext in all_ext:
        if fname.lower().endswith(ext):
            has_ext = True
            LGR.debug(f"{fname} ends with extension {ext}")
            break

    if not has_ext and scan:
        for ext in all_ext:
            if exists(f"{fname}{ext}"):
                fname = f"{fname}{ext}"
                LGR.warning(f"Found {fname}{ext}, using it as input henceforth")
                has_ext = True
                break

    obj_return = [has_ext]

    if remove:
        if has_ext:
            obj_return += [fname[: -len(ext)], ext]  # case insensitive solution
        else:
            obj_return += [fname, ""]
    else:
        obj_return += [fname]

    return obj_return[:]


def check_nifti_dim(fname, data, dim=4):
    """
    Check number of dimensions in nifti file.

    Parameters
    ----------
    fname : str
        The name of the file representing `data`
    data : numpy.ndarray
        The data which dimensionality needs to be checked
    dim : int, optional
        The amount of dimensions expected/desired in the data.

    Returns
    -------
    numpy.ndarray
        If `data.ndim` = `dim`, returns data.

    Raises
    ------
    ValueError
        If `data` has different dimensions than `dim`
    """
    data = data.squeeze()

    if data.ndim != dim:
        raise ValueError(
            f"A {dim}D nifti file is required, but {fname} is "
            f"{data.ndim}D. Please check the input file."
        )

    return data


def check_mtx_dim(fname, data, shape=None):
    """
    Check dimensions of a matrix.

    Parameters
    ----------
    fname : str
        The name of the file representing `data`
    data : np.ndarray
        The data which dimensionality needs to be checked
    shape : None, 'square', or 'rectangle'}, str, optional
        Shape of matrix, if empty, skip shape check

    Returns
    -------
    np.ndarray
        If `data.ndim` = 2, returns data.
        If `data.ndim` = 1 and `shape` == 'rectangle',
        Returns data with added empty axis.

    Raises
    ------
    NotImplementedError
        If `data` has more than 3 dimensions.
        If `shape` is not None but `data` is 3D.
    ValueError
        If `data` is empty
        If `shape` == 'square' and `data` dimensions have different lenghts.
    """
    data = data.squeeze()
    LGR.info("Checking data shape.")

    if data.shape[0] == 0:
        raise ValueError(f"{fname} is empty!")
    if data.ndim > 3:
        raise NotImplementedError(
            "Only matrices up to 3D are supported, but "
            f"given matrix is {data.ndim}D."
        )
    if shape is not None:
        if data.ndim > 2:
            raise NotImplementedError("Cannot check shape of 3D matrix.")
        if data.ndim == 1 and shape == "rectangle":
            data = data[..., np.newaxis]
            LGR.warning(
                f"Rectangular matrix required, but {fname} is a vector. "
                "Adding empty dimension."
            )
        if shape == "square" and data.shape[0] != data.shape[1]:
            raise ValueError(
                f"Square matrix required, but {fname} matrix has "
                f"shape {data.shape}."
            )

    return data


def load_nifti_get_mask(fname, is_mask=False, ndim=4):
    """
    Load a nifti file and returns its data, its image, and a 3d mask.

    Parameters
    ----------
    fname : str
        The filename to read in
    is_mask : bool, optional
        If the file contains a mask.
        Default: False
    ndim : int or None, optional
        The number of dimensions expected in the data.
        If None (default), 4 dimensions are expected, unless is_mask=True.
        In the latter case, 3 dimensions will be checked.

    Returns
    -------
    data : numpy.ndarray
        Data from nifti file.
    mask : numpy.ndarray
        If `is_mask` is False, numpy.ndarray of one dimension less than data,
        in which any element that has at least a value different from zero
        in the last dimension of `data` is True.
        If `is_mask` is True, mask is a boolean representation of data.
    img : nib.img
        Image object from nibabel.

    """
    try:
        import nibabel as nib
    except ImportError:
        raise ImportError(
            "nibabel is required to import nifti files. "
            "Please see install instructions."
        )

    LGR.info(f"Loading {fname}.")
    img = nib.load(fname)
    data = img.get_fdata()

    if ndim is None:
        ndim = 3 if is_mask else 4

    data = check_nifti_dim(fname, data, dim=ndim)

    if is_mask:
        mask = data != 0
        LGR.info(f"{fname} loaded as mask.")
    else:
        mask = data.any(axis=-1).squeeze()
        LGR.info(f"Data loaded from {fname}.")

    return data, mask, img


def load_txt(fname, shape=None):
    """
    Read files in textual format.

    Parameters
    ----------
    fname : str or os.PathLike
        Path to the txt file
    shape : None, 'square', or 'rectangle', optional
        Shape of matrix, if empty, skip check

    Returns
    -------
    mtx : numpy.ndarray
        Data matrix

    See also
    --------
    check_mtx_dim
    """
    LGR.info(f"Loading {fname}.")

    _, _, ext = check_ext(EXT_1D, fname, scan=True, remove=True)

    if ext in [".csv", ".csv.gz"]:
        delimiter = ","
    elif ext in [".tsv", ".tsv.gz"]:
        delimiter = "\t"
    elif ext in [".txt", ".1d", ".par"]:
        delimiter = " "
    else:
        delimiter = None

    mtx = np.genfromtxt(fname, delimiter=delimiter)

    mtx = check_mtx_dim(fname, mtx, shape)

    return mtx


def load_mat(fname, shape=None):
    """
    Read files in matlab format.

    Assumes the existence of a matrix/vector in the mat file, rendered as
    a numpy.ndarray. If there is more than a marix, the one with the largest
    size will be selected.

    Parameters
    ----------
    fname : str or os.PathLike
        Path to the mat file
    shape : None, 'square', or 'rectangle'}, str, optional
        Shape of matrix, if empty, skip check

    Returns
    -------
    mtx : numpy.ndarray
        Data matrix

    Notes
    -----
    Requires module pymatreader to work

    See also
    --------
    check_mtx_dim

    Raises
    ------
    EOFError
        If the mat file does not contain matrix or vectors.
    ImportError
        If pymatreader is not installed or can't be read.
    """
    try:
        from pymatreader import read_mat
    except ImportError:
        raise ImportError(
            "pymatreader is required to import mat files. "
            "Please see install instructions."
        )

    LGR.info(f"Loading {fname}.")
    data = read_mat(fname)

    data_keys = []
    for k in data.keys():
        # Check data key only if it's not hidden
        # (skip '__header__', '__version__', '__global__')
        if "__" not in k:
            LGR.info(
                f"Checking {fname} key {str(k)} content for data "
                "(float array/matrices in MATLAB)."
            )
            if type(data[k]) is np.ndarray:
                data_keys.append(k)

    if len(data_keys) < 1:
        raise EOFError(f"{fname} does not seem to contain a numeric matrix.")
    elif len(data_keys) > 1:
        LGR.warning(
            "Found multiple possible arrays to load. "
            "Selecting the biggest (highest pythonic size)."
        )

    key = data_keys[0]
    for k in data_keys[1:]:
        if data[k].size > data[key].size:
            key = k

    LGR.info(f"Selected data from MATLAB variable {key}")
    mtx = data[key]
    mtx = check_mtx_dim(fname, mtx, shape)

    return mtx


def load_xls(fname, shape=""):
    """
    Read files in xls format.

    Parameters
    ----------
    fname : str or os.PathLike
        Path to the mat file
    shape : None, 'square', or 'rectangle'}, str, optional
        Shape of matrix, if empty, skip check

    Notes
    -----
    Requires module _ to work

    See also
    --------
    check_mtx_dim

    Raises
    ------
    NotImplementedError
        Spreadheet loading is not implemented yet.
    """
    raise NotImplementedError("Spreadsheet loading is not implemented yet")


def export_nifti(data, img, fname):
    """
    Export a nifti file.

    Parameters
    ----------
    data : numpy.ndarray
        Data to be exported
    img : nib.img
        Nibabel image object
    fname : str or os.PathLike
        Name of the output file
    """
    try:
        import nibabel as nib
    except ImportError:
        raise ImportError(
            "nibabel is required to export nifti files. "
            "Please see install instructions."
        )

    for e in EXT_NIFTI:
        has_ext, fname, ext = check_ext(e, fname, remove=True)
        if has_ext:
            break

    if ext == "":
        ext = ".nii.gz"

    LGR.info(f"Exporting nifti data into {fname}{ext}.")
    out_img = nib.Nifti1Image(data, img.affine, img.header)
    out_img.to_filename(f"{fname}{ext}")

    return 0


def export_txt(data, fname, ext=None):
    """
    Export data into a text-like or mat file.

    Parameters
    ----------
    data : np.ndarray
        Data to be exported.
    fname : str or os.PathLike
        Name of the output file.
    ext : str or None, optional
        Selected extension for export.

    Returns
    -------
    0
        On a successful run
    """
    if ext.lower() in [".csv", ".csv.gz", "", None]:
        delimiter = ","
    elif ext.lower() in [".tsv", ".tsv.gz"]:
        delimiter = "\t"
    elif ext.lower() in [".txt", ".1d", ".par"]:
        delimiter = " "
    else:
        delimiter = None

    if data.ndim < 3:
        np.savetxt(f"{fname}{ext}", data, fmt="%.6f", delimiter=delimiter)
    elif data.ndim == 3:
        makedirs(fname, exist_ok=True)
        for i in range(data.shape[-1]):
            np.savetxt(
                join(fname, f"{i:03d}{ext}"),
                data[:, :, i],
                fmt="%.6f",
                delimiter=delimiter,
            )

    return 0


def export_mtx(data, fname, ext=None):
    """
    Export data into a text-like or mat file.

    Parameters
    ----------
    data : np.ndarray
        Data to be exported.
    fname : str or os.PathLike
        Name of the output file.
    ext : str or None, optional
        Selected extension for export.

    Notes
    -----
    Requires module scipy to export in .mat format.
    (Will require other modules to export in XLS-like format)

    Raises
    ------
    BrokenPipeError
        If somewhat an extension that is not supported passes all checks.
        (This should never happen)
    ImportError
        If scipy is not installed or cannot be found.
    NotImplementedError
        Spreadheet output is not implemented yet.

    Returns
    -------
    0
        On a successful run
    """
    if ext is None:
        # Check if extension was provided in fname.
        for e in EXT_ALL:
            has_ext, fname, ext = check_ext(e, fname, remove=True)
            if has_ext:
                break
    elif ext.lower() not in EXT_ALL:
        # Check if extension is supported.
        ext = None

    if ext in [None, ""]:
        LGR.warning(
            "Extension not specified, or specified extension not "
            "supported. Forcing export in CSV format."
        )
        ext = ".csv"
    elif ext.lower() in EXT_NIFTI:
        LGR.warning("Found nifti extension, exporting data in .1D instead")
        ext = ".1D"

    LGR.info(f"Exporting data into {fname}{ext}.")
    if ext.lower() in EXT_MAT:
        try:
            import scipy
        except ImportError:
            raise ImportError(
                "To export .mat files, scipy is required. " "Please install it."
            )
        scipy.io.savemat(f"{fname}{ext}", {"data": data})
    elif ext.lower() in EXT_XLS:
        raise NotImplementedError("Spreadsheet output is not implemented yet")
    elif ext.lower() in EXT_1D:
        export_txt(data, fname, ext)
    else:
        raise BrokenPipeError(
            f"This should not have happened: {ext} was the " "selected extension."
        )

    return 0


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
