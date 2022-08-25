#!/usr/bin/env python3
"""
Operations for timeseries.

Attributes
----------
LGR
    Logger
"""

import logging

import numpy as np

from nigsp.utils import change_var_type, pairwise, prepare_ndim_iteration

LGR = logging.getLogger(__name__)


def normalise_ts(timeseries, globally=False):
    """
    Normalise given timeseries (i.e. mean=0, std=1).

    It is assumed that time is encoded in the second dimension (axis 1),
    e.g. for 90 voxels and 300 timepoints, shape is [90, 300].

    Any timeseries with std == 0 is returned as a series of 0s.

    Parameters
    ----------
    timeseries : numpy.ndarray
        The input timeseries. It is assumed that the second dimension is time.
    globally : bool, optional
        If True, normalise timeseries across the first two axes

    Returns
    -------
    numpy.ndarray
        The normalised timeseries (mean=0 std=1) if timeseries is not a 1D array.
        If timeseries is a 1D array, it is returned as is.
    """
    if timeseries.ndim < 2 or (timeseries.ndim == 2 and timeseries.shape[1] == 1):
        LGR.warning(
            "Given timeseries seems to be a single timepoint. " "Returning it as is."
        )
        return timeseries

    if globally:
        z = (timeseries - timeseries.mean(axis=(0, 1))) / timeseries.std(
            axis=(0, 1), ddof=1
        )
    else:
        z = (timeseries - timeseries.mean(axis=1)[:, np.newaxis, ...]) / timeseries.std(
            axis=1, ddof=1
        )[:, np.newaxis, ...]

    z[np.isnan(z)] = 0

    return z


def spc_ts(timeseries, globally=False):
    """
    Express timeseries in signal percentage change.

    It is assumed that time is encoded in the second dimension (axis 1),
    e.g. for 90 voxels and 300 timepoints, shape is [90, 300].

    Parameters
    ----------
    timeseries : numpy.ndarray
        The input timeseries. It is assumed that the second dimension is time.
    globally : bool, optional
        If True, SPC timeseries across the first two axes (mainly for similarity with other functions.)

    Returns
    -------
    numpy.ndarray
        The timeseries in SPC if timeseries is not a 1D array.
        If timeseries is a 1D array, it is returned as is.
    """
    if timeseries.ndim < 2 or (timeseries.ndim == 2 and timeseries.shape[1] == 1):
        LGR.warning(
            "Given timeseries seems to be a single timepoint. " "Returning it as is."
        )
        return timeseries

    if globally:
        scp = (timeseries - timeseries.mean(axis=(0, 1))) / timeseries.mean(axis=(0, 1))
    else:
        scp = (
            timeseries - timeseries.mean(axis=1)[:, np.newaxis, ...]
        ) / timeseries.mean(axis=1)[:, np.newaxis, ...]

    scp[np.isnan(scp)] = timeseries[np.isnan(scp)]

    return scp


def demean_ts(timeseries, globally=False):
    """
    Demean timeseries.

    It is assumed that time is encoded in the second dimension (axis 1),
    e.g. for 90 voxels and 300 timepoints, shape is [90, 300].

    Parameters
    ----------
    timeseries : numpy.ndarray
        The input timeseries. It is assumed that the second dimension is time.
    globally : bool, optional
        If True, demean timeseries across the first two axes.

    Returns
    -------
    numpy.ndarray
        The demeaned timeseries if timeseries is not a 1D array.
        If timeseries is a 1D array, it is returned as is.
    """
    if timeseries.ndim < 2 or (timeseries.ndim == 2 and timeseries.shape[1] == 1):
        LGR.warning(
            "Given timeseries seems to be a single timepoint. " "Returning it as is."
        )
        return timeseries

    if globally:
        return timeseries - timeseries.mean(axis=(0, 1))
    else:
        return timeseries - timeseries.mean(axis=1)[:, np.newaxis, ...]


def rescale_ts(timeseries, vmin=0, vmax=1, globally=False):
    """
    Rescale given timeseries between given max and min value.

    It is assumed that time is encoded in the second dimension (axis 1),
    e.g. for 90 voxels and 300 timepoints, shape is [90, 300].

    Any timeseries with std == 0 is returned as a series of 0s.

    Parameters
    ----------
    timeseries : numpy.ndarray
        The input timeseries. It is assumed that the second dimension is time.
    vmin : float, optional
        The minimum value to scale between
    vmax : float, optional
        The maximum value to scale between
    globally : bool, optional
        If True, rescale timeseries across the first two axes

    Returns
    -------
    numpy.ndarray
        The normalised timeseries (mean=0 std=1) if timeseries is not a 1D array.
        If timeseries is a 1D array, it is returned as is.
    """
    if timeseries.ndim < 2 or (timeseries.ndim == 2 and timeseries.shape[1] == 1):
        LGR.warning(
            "Given timeseries seems to be a single timepoint. " "Returning it as is."
        )
        return timeseries

    if globally:
        res = timeseries - timeseries.min(axis=(0, 1))
        res = res / res.max(axis=(0, 1))
    else:
        res = timeseries - timeseries.min(axis=1)[:, np.newaxis, ...]
        res = res / res.max(axis=1)[:, np.newaxis, ...]

    res = res * (vmax - vmin) + vmin
    return res


def resize_ts(timeseries, resize=None, globally=False):
    """
    Rescale timeseries with some methods.

    It is assumed that time is encoded in the second dimension (axis 1),
    e.g. for 90 voxels and 300 timepoints, shape is [90, 300].

    Parameters
    ----------
    timeseries : numpy.ndarray
        The input timeseries. It is assumed that the second dimension is time.
    resize : 'spc', 'norm', 'gnorm', 'demean', 'gdemean' tuple, list, or None, optional
        Whether to resize the signal or not before plotting.
        If 'spc', compute signal percentage change
        If 'norm', normalise signals (z-score)
        If 'demean', remove signal average
        If 'gsr', remove global signal (average across points)
        If tuple or list, rescale signals between those two values
        If None, don't do anything (default)
    globally : bool, optional
        If True, rescale timeseries across the first two axes

    Returns
    -------
    numpy.ndarray
        The timeseries after resizing if timeseries is not a 1D array.
        If timeseries is a 1D array, it is returned as is.

    """
    if resize and timeseries.ndim > 1:
        if resize == "spc":  # pragma: no cover
            LGR.info("Expressing timeseries in signal percentage change")
            timeseries = spc_ts(timeseries, globally=globally)
        elif resize == "norm":  # pragma: no cover
            LGR.info("Normalise timeseries")
            timeseries = normalise_ts(timeseries, globally=globally)
        elif resize == "demean":  # pragma: no cover
            LGR.info("Demean timeseries")
            timeseries = demean_ts(timeseries, globally=globally)
        elif resize == "gsr":
            LGR.info("Remove Global Signal from timeseries")
            timeseries = timeseries - timeseries.mean(axis=0)
        elif type(resize) in [tuple, list]:
            if len(resize) != 2:
                raise NotImplementedError("Required two elements to express rescaling")
            LGR.info(
                f"Expressing timeseries in given range {resize}"
            )  # pragma: no cover
            timeseries = resize(
                timeseries, vmin=resize[0], vmax=resize[1], globally=globally
            )  # pragma: no cover
        else:
            raise NotImplementedError(
                f"Chosen rescaling method {resize} is not supported."
            )

    return timeseries


def graph_fourier_transform(timeseries, eigenvec, energy=False, mean=False):
    """
    Projet a graph decomposition onto the timeseries.

    It returns the result of the projection or the energy of the spectral
    density of the projection.

    If `mean` is true and the timeseries has 3 dimensions, it returns the
    mean across the last dimension.

    It is assumed that time is encoded in the second dimension of timeseries (axis 1),
    e.g. for 90 voxels and 300 timepoints, shape is [90, 300].

    Parameters
    ----------
    timeseries : numpy.ndarray
        The input timeseries. It is assumed that the second dimension (axis 1) is time.
    eigenvec : numpy.ndarray
        The eigenvector resulting from the Laplacian decomposition.
    energy : bool, optional
        If True, returns the energy (power) of the spectral density instead of
        the projection.
    mean : bool, optional
        If True and timeseries has 3 dimensions, returns the mean across axis 1 (time).

    Returns
    -------
    np.ndarray
        Returns either the projection of the graph on the timeseries, or its energy.
    """
    timeseries = timeseries.squeeze()
    if timeseries.ndim < 3:
        proj = eigenvec.conj().T @ timeseries
    else:
        temp_ts, proj = prepare_ndim_iteration(timeseries, 2)
        for i in range(temp_ts.shape[-1]):
            proj[:, :, i] = eigenvec.conj().T @ np.squeeze(temp_ts[:, :, i])
        if timeseries.ndim > 3:
            proj = proj.reshape(timeseries.shape)

    if timeseries.ndim > 2 and mean and not energy:
        proj = proj.mean(axis=1)

    if energy:
        # Compute energy of the spectral density
        energy = proj**2
        if proj.ndim > 2 and mean:
            energy = energy.mean(axis=1)

        return energy

    else:
        return proj


def median_cutoff_frequency_idx(energy):
    """
    Find the frequency that splits the energy of a timeseries in two roughly equal parts.

    Parameters
    ----------
    energy : numpy.ndarray
        The array representing the energy (power) spectral density of a timeseries.
        this array can be 1D or 2D - if 2D it's assumed that the second dimension
        represents subjects.

    Returns
    -------
    int
        The index of the frequency that splits the spectral power into two
        (more or less) equal parts.

    Raises
    ------
    NotImplementedError
        If the provided array is 3D or more.
    """
    if energy.ndim > 2:
        raise NotImplementedError(
            "Provided energy spectral density data have "
            f"{energy.ndim} dimensions, but arrays of more "
            "than 2 dimensions are not supported yet"
        )

    if energy.ndim == 2:
        energy = energy.mean(axis=-1)
    half_tot_auc = np.trapz(energy, axis=0) / 2
    LGR.debug(f"Total AUC = {half_tot_auc*2}, targetting half of total AUC")

    # Compute the AUC from first to one to last frequency,
    # skipping first component because AUC(1)=0.
    # Returns first idx for which AUC reaches half of total AUC.
    # It could be computed from high to low, but in theory
    # there would be more cycles, as #eigenvec(h) > #eigenvec(l).
    for freq_idx in range(1, energy.size):
        LGR.debug(
            f"Frequency idx {freq_idx}, "
            f"AUC = {np.trapz(energy[:freq_idx])}, "
            f"target AUC = {half_tot_auc}"
        )
        if np.trapz(energy[:freq_idx]) >= half_tot_auc:
            break

    LGR.info(f"Found {freq_idx} as splitting index")
    return freq_idx


def graph_filter(timeseries, eigenvec, freq_idx, keys=["low", "high"]):
    """
    Filter a graph decomposition into two parts based on freq_idx.

    Return the two eigenvector lists (high freq and low freq) that are equal
    to the original eigenvector list, but "low" is zero-ed for all frequencies
    >= of the given index, and "high" is zero-ed for all frequencies < to the
    given index.
    Also return their projection onto a timeseries.

    Parameters
    ----------
    timeseries : numpy.ndarray
        The input timeseries. It is assumed that the second dimension is time.
    eigenvec : numpy.ndarray
        The eigenvector resulting from the Laplacian decomposition.
    freq_idx : int or list
        The index of the frequency that splits the spectral power into two
        (more or less) equal parts - i.e. the index of the first frequency in
        the "high" component.
    keys : list, optional
        The keys to call the splitted parts with

    Returns
    -------
    dict of numpy.ndarray
        Return first the split eigenvectors
    dict of numpy.ndarray
        Return second the projected split eigenvectors onto the timeseries.

    Raises
    ------
    IndexError
        If the given index is 0 (all "high"), the last possible index (all "low"),
        or higher than the last possible index (not applicable).
    """
    # #!# Find better name
    # #!# Implement an index splitter
    freq_idx = change_var_type(freq_idx, list, stop=False, silent=True)

    for f in freq_idx:
        if f == 0 or f >= eigenvec.shape[0] - 1:
            raise IndexError(
                f"Selected index {f} is not valid to split "
                f"eigenvector matrix of shape {eigenvec.shape}."
            )

    LGR.info(f"Splitting graph into {len(freq_idx)+1} parts")

    # Check that there is the right amount of keys
    if len(keys) > len(freq_idx) + 1:
        LGR.warning(
            f"The declared keys list ({keys}) has {len(keys)} elements. "
            f"Since the frequency index list ({freq_idx}) has {len(freq_idx)}, "
            f"any keys after {keys[len(freq_idx)]} will be ignored."
        )
        keys = keys[: len(freq_idx) + 1]
    elif len(keys) < len(freq_idx) + 1:
        LGR.warning(
            f"The declared keys list ({keys}) has {len(keys)} elements. "
            f"Since the frequency index list ({freq_idx}) has {len(freq_idx)}, "
            f"more keys will be created after {keys[len(freq_idx)]} ."
        )

        for i in range(len(keys), len(freq_idx) + 1):
            keys = keys + [f"key-{i+1:03d}"]

    # Add 0 and None to freq_idx to have full indexes
    freq_idx = [0] + freq_idx + [None]

    evec_split = dict.fromkeys(keys)
    ts_split = dict.fromkeys(keys)

    for n, idx in enumerate(pairwise(freq_idx)):
        i, j = idx
        k = j if j is not None else eigenvec.shape[-1]
        evec_split[keys[n]] = np.append(
            np.append(
                np.zeros_like(eigenvec[:, :i], dtype="float32"),
                eigenvec[:, i:j],
                axis=-1,
            ),
            np.zeros_like(eigenvec[:, k:], dtype="float32"),
            axis=-1,
        )

    LGR.info("Compute graph fourier coefficients.")
    fourier_coeff = graph_fourier_transform(timeseries, eigenvec)

    for k in keys:
        LGR.info(f"Compute {k} part of timeseries.")
        ts_split[k] = graph_fourier_transform(fourier_coeff, evec_split[k].T)

    return evec_split, ts_split


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
