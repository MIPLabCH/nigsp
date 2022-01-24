#!/usr/bin/env python3
"""
I/O and related utils.

Attributes
----------
EXT_1D : list
    List of supported TXT/1D file extensions, in lower case.
EXT_NIFTI : list
    List of supported nifti file extensions, in lower case.
FIGSIZE : tuple
    Figure size
SET_DPI : int
    DPI of the figure
LGR :
    Logger
"""

import logging

import nibabel as nib
import numpy as np
import scipy.interpolate as spint


SET_DPI = 100
FIGSIZE = (18, 10)
EXT_1D = ['.txt', '.csv', '.tsv', '.1d', '.par', '.tsv.gz']
EXT_NIFTI = ['.nii', '.nii.gz']

LGR = logging.getLogger(__name__)
LGR.setLevel(logging.INFO)


def if_declared_force_type(var, dtype, varname='an input variable', silent=False):
    """
    Make sure `var` is of type `dtype`.

    Parameters
    ----------
    var : str, int, or float
        Variable to change type of
    dtype : str
        Type to change `var` to
    varname : str, optional
        The name of the variable
    silent : bool, optional
        If True, don't return any message

    Returns
    -------
    int, float, str, list, or var
        The given `var` in the given `dtype`, or `var` if '' or None

    Raises
    ------
    NotImplementedError
        If dtype is not 'int', 'float', 'str', or 'list'
    """
    if var:
        if dtype == 'int':
            tmpvar = int(var)
        elif dtype == 'float':
            tmpvar = float(var)
        elif dtype == 'str':
            tmpvar = str(var)
        elif dtype == 'list':
            if type(var) == list:
                tmpvar = var
            else:
                tmpvar = [var]
        else:
            raise NotImplementedError(f'Type {dtype} not supported')

        if not silent:
            if type(tmpvar) != type(var):
                if varname != 'an input variable':
                    varname = f'variable {varname}'

                LGR.warning(f'Changing type of {varname} from {type(var)} to {dtype}')

        return tmpvar

    else:
        return var


def check_ext(all_ext, fname, remove=False):
    """
    Check which extension a file has, and possibly remove it.

    Parameters
    ----------
    all_ext : list
        All possible extensions to check within
    fname : str
        The filename to check
    remove : bool, optional
        Remove the extention from fname if it has one

    Returns
    -------
    str :
        If "remove" is True, return (extensionless) fname
    has_ext : boolean
        True if the extension is found, false otherwise
    """
    has_ext = False
    all_ext = if_declared_force_type(all_ext, 'list', silent=True)
    for ext in all_ext:
        if fname.lower().endswith(ext):
            has_ext = True
            break

    if remove:
        if has_ext:
            return fname[:-len(ext)], has_ext  # case insensitive solution
        else:
            return fname, has_ext
    else:
        return has_ext


def check_nifti_dim(fname, data, dim=4):
    """
    Remove extra dimensions.

    Parameters
    ----------
    fname : str
        The name of the file representing `data`
    data : np.ndarray
        The data which dimensionality needs to be checked
    dim : int, optional
        The amount of dimensions expected/desired in the data.

    Returns
    -------
    np.ndarray
        If `len(data.shape)` = `dim`, returns data.
        If `len(data.shape)` > `dim`, returns a version of data without the
        dimensions above `dim`.

    Raises
    ------
    ValueError
        If `data` has less dimensions than `dim`
    """
    if len(data.shape) < dim:
        raise ValueError(f'{fname} does not seem to be a {dim}D file. '
                         f'Plase provide a {dim}D nifti file.')
    if len(data.shape) > dim:
        LGR.warning(f'{fname} has more than {dim} dimensions. Removing D > {dim}.')
        for ax in range(dim, len(data.shape)):
            data = np.delete(data, np.s_[1:], axis=ax)

    return np.squeeze(data)


def load_nifti_get_mask(fname, is_mask=False, mask_dim=3):
    """
    Load a nifti file and returns its data, its image, and a 3d mask.

    Parameters
    ----------
    fname : str
        The filename to read in
    is_mask : bool, optional
        If the file contains a mask.
        Default: False
    mask_dim : int
        The number of dimensions expected in the mask

    Returns
    -------
    data : np.ndarray
        Data from nifti file.
    mask : np.ndarray
        If `is_mask` is False, np.ndarray of one dimension less than data,
        in which any element that has at least a value different from zero
        in the last dimension of `data` is True.
        If `is_mask` is True, mask is a boolean representation of data.
    img : nib.img
        Image object from nibabel.

    """
    img = nib.load(fname)
    LGR.info(f'Loading {fname}')
    data = img.get_fdata()

    if is_mask:
        data = check_nifti_dim(fname, data, dim=mask_dim)
        mask = (data < 0) + (data > 0)
    else:
        data = check_nifti_dim(fname, data)
        mask = np.squeeze(np.any(data, axis=-1))

    return data, mask, img


def export_regressor(regr_t, petco2hrf_shift, func_t, outname, suffix='petco2hrf', ext='.1D'):
    """
    Export generated regressors for fMRI analysis.

    Parameters
    ----------
    regr_t : np.ndarray
        The time range of the fMRI data, with the same sampling of `petco2hrf_shift`
        Its last element should be equal to the last element of `func_t`
    petco2hrf_shift : np.ndarray
        The regressors that needs to be exported, in its original sample
    func_t : np.ndarray
        The time range of the fMRI data, with the fMRI data sampling.
        Its last element should be equal to the last element of `regr_t`
    outname : str or path
        Prefix of the output file - can contain a path.
    suffix : str, optional
        The suffix of the output file.
    ext : str, optional
        The extension of the output file.

    Returns
    -------
    petco2hrf_demean : np.ndarray
        Interpolated version of `petco2hrf_shift` in the sampling of the fMRI data.
    """
    if regr_t[-1] != func_t[-1]:
        raise ValueError('The two given time ranges do not express the same range!')
    f = spint.interp1d(regr_t, petco2hrf_shift, fill_value='extrapolate')
    petco2hrf_shift = f(func_t)
    petco2hrf_demean = petco2hrf_shift - petco2hrf_shift.mean()
    np.savetxt(f'{outname}_{suffix}{ext}', petco2hrf_demean, fmt='%.6f')

    return petco2hrf_demean


def export_nifti(data, img, fname):
    """
    Export a nifti file.

    Parameters
    ----------
    data : np.ndarray
        Data to be exported
    img : nib.img
        Nibabel image object
    fname : str or path
        Name of the output file
    """
    if fname.endswith('.nii.gz'):
        fname = fname[:-7]

    out_img = nib.Nifti1Image(data, img.affine, img.header)
    out_img.to_filename(f'{fname}.nii.gz')


"""
Copyright 2021, Stefano Moia.

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
