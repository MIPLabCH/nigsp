#!/usr/bin/env python3
"""
Operations on nifti files.

Attributes
----------
LGR
    Logger
"""

import logging

import numpy as np

LGR = logging.getLogger(__name__)


def vol_to_mat(data):
    """
    Reshape <3D in 1D or 4D into 2D.

    Parameters
    ----------
    data : numpy.ndarray
        The data to be transformed into 2D.

    Returns
    -------
    numpy.ndarray
        2D reshaped data.
    """
    LGR.info(f"Reshape {data.ndim}D volume into 1[+1]D (space[*time]) matrix.")
    return data.reshape(((-1,) + data.shape[3:]), order="F")


def mat_to_vol(data, shape=None, asdata=None):
    """
    Reshape nD data (normally 2D) using either shape or data shape).

    Parameters
    ----------
    data : numpy.ndarray
        Data to be reshaped.
    shape : None or list of int, optional
        New shape.
    asdata : None or numpy.ndarray, optional
        Numpy ndarray to use the shape of.

    Returns
    -------
    numpy.ndarray
        Reshaped data.

    Raises
    ------
    ValueError
        If both shape and asdata are empty.
    """
    if asdata is not None:
        if shape is not None:
            LGR.warning(
                "Both shape and asdata were defined. "
                f"Overwriting shape {shape} with asdata {asdata.shape}"
            )
        shape = asdata.shape
    elif shape is None:
        raise ValueError(
            "Both shape and asdata are empty. " "Must specify at least one"
        )

    LGR.info(f"Reshape {data.ndim}D matrix into volume with shape {shape}.")
    return data.reshape(shape, order="F")


def apply_mask(data, mask):
    """
    Reduce shape and size of data based on mask.

    Uses the concept of "mask" as defined in neuroimaging, not in numpy:
    every voxel that is not 0 is kept, the 0 are excluded.

    Parameters
    ----------
    data : numpy.ndarray
        Data to be masked.
    mask : numpy.ndarray
        Mask to be applied - where all elements that are 0 are eliminated.

    Returns
    -------
    numpy.ndarray
        Masked (data.ndim-1 Dimensions) array.

    Raises
    ------
    ValueError
        If the first mask.ndim dimensions of data have a different shape from mask.
    """
    if data.shape[: mask.ndim] != mask.shape:
        raise ValueError(
            f"Cannot mask data with shape {data.shape} using mask "
            f"with shape {mask.shape}"
        )
    if (data.ndim - mask.ndim) > 1:
        LGR.warning(f"Returning volume with {data.ndim-mask.ndim+1} dimensions.")
    else:
        LGR.info(f"Returning {data.ndim-mask.ndim+1}D array.")

    mask = mask != 0
    return data[mask]


def unmask(data, mask, shape=None, asdata=None):
    """
    Unmask 1D or 2D into an nD based on shape or asdata.

    Parameters
    ----------
    data : numpy.ndarray (1D or 2D)
        The data to unmask.
    mask : numpy.ndarray
        The nD mask to use to unwrap (unmask) the data.
        All elements different from 0 will be used as entries for data.
    shape : None or list of int, optional
        List indicating shape of nD array.
    asdata : None or numpy.ndarray, optional
        Array to take the same shape of.

    Returns
    -------
    numpy.ndarray
        The unmasked nD array version of data.

    Raises
    ------
    ValueError
        If both `shape` and `asdata` are empty
        If the first dimension of `data` and the number of available voxels in
        mask do not match.
        If the mask shape does not match the first (mask)
    """
    if asdata is not None:
        if shape is not None:
            LGR.warning(
                "Both shape and asdata were defined. "
                f"Overwriting shape {shape} with asdata {asdata.shape}"
            )
        shape = asdata.shape
    elif shape is None:
        raise ValueError(
            "Both shape and asdata are empty. " "Must specify at least one."
        )

    if shape[: mask.ndim] != mask.shape:
        raise ValueError(
            f"Cannot unmask data into shape {shape} using mask "
            f"with shape {mask.shape}"
        )
    if data.ndim > 1 and (data.shape[0] != mask.sum()):
        raise ValueError(
            "Cannot unmask data with first dimension "
            f"{data.shape[0]} using mask with "
            f"{mask.sum()} entries)"
        )

    LGR.info(f"Unmasking matrix into volume of shape {shape}")
    mask = mask != 0
    out = np.zeros(shape, dtype="float32")
    out[mask] = data
    return out


def apply_atlas(data, atlas, mask=None):
    """
    Extract average timeseries from an atlas.

    Parameters
    ----------
    data : numpy.ndarray
        A 3- or 4- D matrix (normally nifti data) of timeseries.
    atlas : numpy.ndarray
        A 2- or 3- D matrix representing the atlas, each parcel represented by a different int.
    mask : None or numpy.ndarray, optional
        A 2- or 3- D matrix representing a mask, all voxels == 0 are excluded from the computation.

    Returns
    -------
    numpy.ndarray
        A [data.ndim-1]D matrix representing the average timeseries of each parcels.

    Raises
    ------
    NotImplementedError
        If atlas is 4+ D
    ValueError
        If atlas or mask have a different shape than the first dimensions of data
    """
    if mask is None:
        mask = (data != 0).any(axis=-1)
    else:
        # Ensure that mask is boolean
        mask = mask != 0

    # #!# Add nilearn's fetching atlases utility

    if atlas.ndim > 3:
        raise NotImplementedError(
            f"Files with {atlas.ndim} dimensions are not " "supported as atlases."
        )
    if data.shape[: mask.ndim] != mask.shape:
        raise ValueError(
            f"Cannot mask data with shape {data.shape} using mask "
            f"with shape {mask.shape}"
        )
    if data.shape[: atlas.ndim] != atlas.shape:
        raise ValueError(
            f"Cannot apply atlas with shape {atlas.shape} on data "
            f"with shape {data.shape}"
        )
    if (data.ndim - atlas.ndim) > 1:
        LGR.warning(f"returning volume with {data.ndim-atlas.ndim+1} dimensions.")
    else:
        LGR.info(
            f"Returning {data.ndim-atlas.ndim+1}D array of signal averages "
            f"in atlas {atlas}."
        )

    # Mask data and atlas first
    atlas = atlas * mask
    labels = np.unique(atlas)
    labels = labels[labels > 0]
    LGR.info(f"Labels: {labels}, numbers: {len(labels)}")
    # Initialise dataframe and dictionary for series
    parcels = np.empty([len(labels), data.shape[-1]], dtype="float32")

    # Compute averages
    for n, l in enumerate(labels):
        parcels[n, :] = data[atlas == l].mean(axis=0)

    return parcels


def unfold_atlas(data, atlas, mask=None):
    """
    Return a lower dimensional matrix into a 3- or 4- D matrix based on an atlas.

    (i.e. unfold a matrix into a 3D atlas)

    Parameters
    ----------
    data : numpy.ndarray
        A 1- or 2- D matrix of shape parcels*timepoints.
    atlas : numpy.ndarray
        A 3D matrix that represents an atlas.
    mask : None or numpy.ndarray, optional
        A matrix with the same shape as atlas. All non-zero elements will be
        considered for the unfolding, all zero elements will be excluded.

    Returns
    -------
    numpy.ndarray
        A 3- or 4- D matrix of shape [atlas]*[timepoints]. Contains the
        timeseries unfolded in the atlas.

    Raises
    ------
    ValueError
        If atlas and mask have dimensions that are too different (i.e. more than
        1 dimension of difference)
        If mask has different shapes from atlas.
        If the first dimension of the data is not equal to the amount of label
        in the atlas.
    """
    if mask is None:
        mask = atlas != 0
    else:
        # Check that mask contains bool
        mask = mask != 0

    if (mask.ndim - atlas.ndim) == 1:
        atlas = atlas[..., np.newaxis]
    elif (atlas.ndim - mask.ndim) == 1:
        mask = mask[..., np.newaxis]
    elif abs(mask.ndim - atlas.ndim) > 1:
        raise ValueError(f"Cannot use {mask.ndim}D mask on {atlas.ndim}D atlas.")

    if atlas.shape[: mask.ndim] != mask.shape:
        raise ValueError(
            f"Cannot mask atlas with shape {atlas.shape} using mask "
            f"with shape {mask.shape}"
        )
    atlas = atlas * mask

    labels = np.unique(atlas)
    labels = labels[labels > 0]
    if data.shape[0] != len(labels):
        raise ValueError(
            f"Cannot unfold data with shape {data.shape} on atlas "
            f"with {len(labels)} parcels"
        )

    LGR.info(f"Unmasking data into atlas-like volume of {3+data.ndim-1} dimensions.")
    out = np.zeros_like(atlas, dtype="float32")

    for ax in range(1, data.ndim):
        if data.shape[ax] > 1:
            out = out[..., np.newaxis].repeat(data.shape[ax], axis=-1)

    for n, l in enumerate(labels):
        out[atlas == l] = data[n, ...]

    return out


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
