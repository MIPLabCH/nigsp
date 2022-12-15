#!/usr/bin/env python3
"""
Operations on graphs and graph derived properties.

Attributes
----------
LGR
    Logger
"""

import logging
from itertools import combinations

import numpy as np

from nigsp import references
from nigsp.due import due
from nigsp.utils import prepare_ndim_iteration

LGR = logging.getLogger(__name__)

SUPPORTED_METRICS = ["sdi", "dfc", "fc"]


@due.dcite(references.PRETI_2019)
def sdi(ts_split, mean=False, keys=None):
    """
    Compute the Structural Decoupling Index (SDI).

    i.e. the ratio between the norms of the "high" and the norm of the "low"
    "graph-filtered" timeseries.

    If the given dictionary does not contain the keywords "high" and "low",
    the SDI is computed as the ratio between the norm of the second and
    the norm of the first dictionary entry.
    "keys" can be used to indicate the order of the two keys, or to select two
    elements of a bigger dictionary.

    Parameters
    ----------
    ts_split : dict or numpy.ndarrays
        A dictionary containing two entries. If the two entries are "low" and
        "high", then SDI will be computed as the norm of the high vs the norm
        of the low, oterwise as the ratio between the second (second key in
        sorted keys) and the first.
    mean : bool, optional
        If True, compute mean over the last axis (e.g. between subjects)
    keys : None or list of strings, optional
        Can be used to select two entries from a bigger dictionary
        and/or to specify the order in which the keys should be read (e.g.
        forcing a different order from teh sorted keys).

    Returns
    -------
    numpy.ndarray
        Returns the structural decoupling index

    Raises
    ------
    ValueError
        If keys are provided but not contained in the dictionary
        If keys are not provided and the dictionary has more than 2 entries
    """
    # #!# Implement acceptance of two matrices and not only dictionary
    if keys is None:
        keys = list(ts_split.keys())
    else:
        if all(item in list(ts_split.keys()) for item in keys) is False:
            raise ValueError(
                f"The provided keys {keys} do not match the "
                "keys of the provided dictionary "
                f"({list(ts_split.keys())})"
            )

    if len(keys) != 2:
        raise ValueError(
            "`structural_decoupling_index` function requires "
            "a dictionary with exactly two timeseries as input."
        )

    check_keys = [item.lower() for item in keys]
    if all(item in ["low", "high"] for item in check_keys):
        # Case insensitively reorder the items of dictionary as ['low', 'high'].
        keys = [keys[check_keys.index("low")], keys[check_keys.index("high")]]

    norm = dict.fromkeys(keys)
    for k in keys:
        norm[k] = np.linalg.norm(ts_split[k], axis=1)

    LGR.info("Computing Structural Decoupling Index.")
    sdi = norm[keys[1]] / norm[keys[0]]

    if sdi.ndim >= 2 and mean:
        sdi = sdi.mean(axis=1)

    return np.log2(sdi)


def gsdi(ts_split, mean=False, keys=None):
    """Compute the generalised SDI.

    Parameters
    ----------
    ts_split : dict or numpy.ndarrays
        A dictionary containing two entries. If the two entries are "low" and
        "high", then SDI will be computed as the norm of the high vs the norm
        of the low, oterwise as the ratio between the second (second key in
        sorted keys) and the first.
    mean : bool, optional
        If True, compute mean over the last axis (e.g. between subjects)
    keys : None or list of strings, optional
        Can be used to select two entries from a bigger dictionary
        and/or to specify the order in which the keys should be read (e.g.
        forcing a different order from teh sorted keys).

    Returns
    -------
    dict of numpy.ndarray
        Returns a dictionary of computed gSDI.

    Raises
    ------
    ValueError
        If keys are provided but not contained in the dictionary.
    """
    # #!# Implement acceptance of N matrices and not only dictionary
    # #!# Check that this can overcome SDI
    if keys is None:
        keys = list(ts_split.keys())
    else:
        if all(item in list(ts_split.keys()) for item in keys) is False:
            raise ValueError(
                f"The provided keys {keys} do not match the "
                "keys of the provided dictionary "
                f"({list(ts_split.keys())})"
            )

    if len(keys) > 2:
        LGR.info("Prepare combinations of timeseries")
        # Combining two or more "timeseries splits" means nothing more than
        # adding them in this case.
        for n in range(2, len(keys)):
            for c in combinations(keys, n):
                comb_key = str(c).replace("'", "").replace(", ", "_and_")

                ts_split[comb_key] = np.zeros_like(ts_split[keys[0]], dtype="float32")
                for k in c:
                    ts_split[comb_key] = np.add(ts_split[comb_key], ts_split[k])

    # Obtain updated list of keys
    all_keys = list(ts_split.keys())
    norm = dict.fromkeys(all_keys)
    LGR.info("Computing norm of timeseries")
    for k in all_keys:
        norm[k] = np.linalg.norm(ts_split[k], axis=1)

    LGR.info("Computing generalised SDI")
    gsdi = dict()
    for k in keys:
        for j in all_keys:
            if not (k in j or f"({k}_" in j or f"_{k})" in j or f"_{k}_" in j):
                gsdi[f"{k}_over_{j}"] = norm[k] / norm[j]

    if list(gsdi.values())[0].ndim >= 2 and mean:
        for k in gsdi.keys():
            gsdi[k] = np.log2(gsdi[k].mean(axis=1))
    else:
        for k in gsdi.keys():
            gsdi[k] = np.log2(gsdi[k])

    return gsdi


@due.dcite(references.GRIFFA_2022)
def functional_connectivity(timeseries, mean=False):
    """
    Compute Functional Connectivity of timeseries.

    It is assumed that time is encoded in the second dimension (axis 1),
    e.g. for 90 voxels and 300 timepoints, shape is [90, 300].

    Parameters
    ----------
    timeseries : numpy.ndarray or dict of numpy.ndarray
        Adictionary of (or a single) 2- or 3-D matrix with timeseries along axis 1.
    mean : bool, optional
        If timeseries is 3D and this is True, return the average FC along the last axis.

    Returns
    -------
    numpy.ndarray or dict of numpy.ndarray
        Functional Connectivity of the given timeseries input.
    """

    def _fc(timeseries, mean=False):
        """
        Quick functional connectivity computation.

        This is not meant to be used outside of other functions.

        It is assumed that time is encoded in the second dimension (axis 1),
        e.g. for 90 voxels and 300 timepoints, shape is [90, 300].

        Parameters
        ----------
        timeseries : numpy.ndarray
            A 2- or 3-D matrix containing timeseries along axis 1.
        mean : bool, optional
            If timeseries is 3D and this is True, return the average FC along the last axis.

        Returns
        -------
        numpy.ndarray
            FC matrix
        """
        timeseries = timeseries.squeeze()
        if timeseries.ndim < 2:
            LGR.warning("Computing functional connectivity of a 1D array (== 1)!")
            return 1
        elif timeseries.ndim == 2:
            return np.corrcoef(timeseries)
        else:
            # reshape the array to allow reiteration on unknown dimensions of timeseries
            temp_ts, _ = prepare_ndim_iteration(timeseries, 2)
            fcorr = np.empty(
                ([temp_ts.shape[0]] * 2 + [temp_ts.shape[-1]]), dtype="float32"
            )
            for i in range(temp_ts.shape[-1]):
                fcorr[:, :, i] = np.corrcoef(temp_ts[..., i])

            if timeseries.ndim > 3:
                new_shape = (timeseries.shape[0],) * 2 + timeseries.shape[2:]
                fcorr = fcorr.reshape(new_shape)

            if mean:
                fcorr = fcorr.mean(axis=2).squeeze()
            return fcorr

    if type(timeseries) is dict:
        fc = dict()
        for k in timeseries.keys():
            fc[k] = _fc(timeseries[k], mean)
    else:
        fc = _fc(timeseries, mean)

    return fc


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
