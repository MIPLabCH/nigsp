#!/usr/bin/env python3
"""
Surrogate utility.

Attributes
----------
LGR
    Logger
"""

import logging
from copy import deepcopy
from math import ceil, factorial, floor

import numpy as np

from nigsp.operations.laplacian import decomposition
from nigsp.operations.timeseries import graph_fourier_transform

LGR = logging.getLogger(__name__)
SURR_TYPE = ["informed", "uninformed"]
STAT_METHOD = ["Bernoulli", "frequentist"]


def random_sign(eigenvec, n_surr=1000, seed=42, stack=False):
    """
    Create surrogates by randomly switching signs of eigenvectors.

    Parameters
    ----------
    eigenvec : numpy.ndarray
        A matrix of eigenvectors
    n_surr : int, optional
        Number of surrogates to create
    seed : int or None, optional
        Random seed (for repeatability)
    stack : bool, optional
        If True, add original eigenvec as last entry of the last dimension
        of the created surrogate matrix

    Returns
    -------
    numpy.ndarray
        The matrix of surrogates, of shape eigenvec * n_surr(+1)

    Raises
    ------
    NotImplementedError
        If eigenvec is 4+ D.
    """
    # Reinitialise the random seed for repeatability
    rng = np.random.default_rng(seed)

    if eigenvec.ndim > 3:
        raise NotImplementedError(
            f"Provided data has {eigenvec.ndim} dimensions, "
            "but data of more than 3 dimensions are not "
            "supported yet"
        )

    rand_evec = np.empty((eigenvec.shape + (n_surr,)), dtype="float32")

    LGR.info("Randomly switching signs of eigenvectors to create surrogates.")
    for i in range(n_surr):
        # #!# Check if two conditions can be merged.
        if eigenvec.ndim < 3:
            r_sign = rng.integers(0, 1, eigenvec.shape[0], endpoint=True)
            r_sign[r_sign == 0] = -1
            rand_evec[..., i] = eigenvec * r_sign
        else:
            for j in range(eigenvec.shape[2]):
                r_sign = rng.integers(0, 1, eigenvec.shape[0], endpoint=True)
                r_sign[r_sign == 0] = -1
                rand_evec[:, :, j, i] = eigenvec[..., j] * r_sign

    if stack:
        rand_evec = np.append(rand_evec, eigenvec[..., np.newaxis], axis=-1)

    return rand_evec


def _create_surr(timeseries, eigenvec, n_surr, seed, stack):
    """
    Proper surrogate creation step.

    This is not meant to be called as a function.

    Parameters
    ----------
    timeseries : numpy.ndarray
        A 3D (or less) array coding a timeseries in the second axis (axis 1).
    eigenvec : numpy.ndarray
        The eigenvector matrix from a previous Laplacian decomposition.
    n_surr : int
        The number of surrogates to create
    seed : int or None
        The seed to reinitialise the RNG - used for replicability.
    stack : bool
        If True, append the real matrix at the end of the stack.

    Returns
    -------
    numpy.ndarray
        The surrogate matrix, of shape timeseries.shape, n_surr

    Raises
    ------
    NotImplementedError
        If timeseries is 4+ D and/or eigenvector matrix has not enough dimensions.
    """
    rand_evec = random_sign(eigenvec, n_surr, seed, stack)

    if stack:
        n_surr += 1

    surr = np.empty((timeseries.shape + (n_surr,)), dtype="float32")

    fourier_coeff = graph_fourier_transform(timeseries, eigenvec)

    LGR.info("Projecting the timeseries onto the surrogate eigenvectors.")
    for i in range(n_surr):
        if timeseries.ndim < 3 and rand_evec.ndim == timeseries.ndim + 1:
            surr[..., i] = graph_fourier_transform(fourier_coeff, rand_evec[..., i].T)
        elif timeseries.ndim == 3:
            if rand_evec.ndim < 4:
                surr[..., i] = graph_fourier_transform(
                    fourier_coeff, rand_evec[..., i].T
                )
            else:
                for j in range(rand_evec.shape[2]):
                    surr[:, :, j, i] = graph_fourier_transform(
                        fourier_coeff, rand_evec[:, :, j, i].T
                    )
        else:
            raise NotImplementedError(
                "No solution implemented for timeseries "
                f"of {timeseries.ndim} dimension(s) and "
                f"eigenvector matrix of {eigenvec.ndim} "
                "dimension(s)"
            )
    return surr


def sc_informed(timeseries, eigenvec, n_surr=1000, seed=124, stack=False):
    """
    Create surrogates informed by the real structural connectivity.

    Parameters
    ----------
    timeseries : numpy.ndarray
        A 3D (or less) array coding a timeseries in the second axis (axis 1).
    eigenvec : numpy.ndarray
        The eigenvector matrix from a previous Laplacian decomposition.
    n_surr : int, optional
        The number of surrogates to create
    seed : int or None, optional
        The seed to reinitialise the RNG - used for replicability.
    stack : bool, optional
        If True, append the real matrix at the end of the stack.

    Returns
    -------
    numpy.ndarray
        The surrogate matrix, of shape timeseries.shape, n_surr

    Raises
    ------
    NotImplementedError
        If timeseries is 4+ D.
    """
    if timeseries.ndim > 3:
        raise NotImplementedError(
            f"Provided timeseries has {timeseries.ndim} "
            "dimensions, but timeseries of more than 3 "
            "dimensions are not supported yet."
        )

    return _create_surr(timeseries, eigenvec, n_surr, seed, stack)


def sc_uninformed(timeseries, lapl_mtx, n_surr=1000, seed=98, stack=False):
    """
    Create surrogates ignorant of the real structural connectivity.

    Parameters
    ----------
    timeseries : numpy.ndarray
        A 3D (or less) array coding a timeseries in the second axis (axis 1).
    lapl_mtx : numpy.ndarray
        A symmetrically normalised laplacian matrix.
    n_surr : int, optional
        The number of surrogates to create
    seed : int or None, optional
        The seed to reinitialise the RNG - used for replicability.
    stack : bool, optional
        If True, append the real matrix at the end of the stack.

    Returns
    -------
    numpy.ndarray
        The surrogate matrix, of shape timeseries.shape, n_surr

    Raises
    ------
    NotImplementedError
        If timeseries is 4+ D.
    """
    if timeseries.ndim > 3:
        raise NotImplementedError(
            f"Provided timeseries has {timeseries.ndim} "
            "dimensions, but timeseries of more than 3 "
            "dimensions are not supported yet."
        )

    symm_norm = np.eye(lapl_mtx.shape[0]) - lapl_mtx
    symm_norm_sum = symm_norm.sum(axis=-1)

    conf_model = np.outer(symm_norm_sum, symm_norm_sum.T) / symm_norm.sum()

    conf_lapl = np.diag(symm_norm_sum) - conf_model

    _, surr_eigenvec = decomposition(conf_lapl)

    return _create_surr(timeseries, surr_eigenvec, n_surr, seed, stack)


def test_significance(
    surr,
    data=None,
    method="Bernoulli",
    p=0.05,
    p_bernoulli=None,
    return_masked=False,
    mean=False,
):
    """
    Test the significance of the empirical data against surrogates.

    Two methods are implemented, 'Bernoulli' and 'frequentist'.
    - 'frequentist' is a group or single subject test. It tests that the
      empirical data are in the highest (or lowest) percentile (where the
      percentile is defined by p/2).
    - 'Bernoulli' is a group test. It tests that the number of subjects for
      which the empirical data is higher (or lower) than a set of surrogates
      (frequentist approach) is at the tail of a binomial cumulative
      distribution (where 'tail' is defined by p).

    Note that p is expressed as two-tails test for the frequentist approach and
    a one-tail test for the Bernoulli approach.

    Both surr and data are expected to have first dimensions: observations [x subjects].

    Parameters
    ----------
    surr : numpy.ndarray
        The surrogate matrix, where all surrogates are aligned along the last axis.
        May have the empirical data matrix last along the last axis.
        Expected to have shape: observations, [subjects,] surrogates.
    data : numpy.ndarray or None, optional
        The empirical data matrix. If given, it's appended at the end of the
        surrogate matrix.
        Expected to have shape: observations[, subjects].
    method : 'Bernoulli' or 'frequentist', optional
        The method to adopt for testing, either based on a Bernoulli process
        or a frequentist observation (see above).
    p : float, optional
        The probability threshold to adopt for the frequentist approach part.
        Note that this is a two-tails test.
    p_bernoulli : float or None, optional
        The probability threshold to adopt for Bernoulli's test.
        If left as None, the specified p value will be used instead,
        and p will be set to 0.1.
        Note that this is a one-tail test.
    return_masked : bool, optional
        If True, returns the masked data. If False, returns a mask that holds
        True where the good data are (inverse of numpy mask). Mask has the same
        shape as data.
    mean : bool, optional
        If True, returns the average of the masked data along the last axis.

    Returns
    -------
    numpy.ndarray
        A numpy.ndarray shaped obervations[, subjects]. If return_masked is True,
        returns the masked version of `data`, otherwise returns the mask.
        If mean is True, returns the average along the subject axis.

    Raises
    ------
    ValueError
        If data is not None and the surrogate shape (except last axis) is
        different from the data shape
    NotImplementedError
        If any other method rather than those listed above is selected.

    """
    # #!# Check that the surrogate shape has parcels in the first axis!
    # If provided, append data to surr
    if data is not None:
        if surr.shape[: data.ndim] != data.shape:
            raise ValueError(
                "Provided empirical data and surrogate data shapes "
                f"do not agree, with shapes {data.shape} and "
                f"{surr.shape[:data.ndim]} (last axis excluded)"
            )
        if not (surr[..., -1] == data).all():
            # Check that data was not appended yet.
            surr = np.append(surr, data[..., np.newaxis], axis=-1)

    if p < 0 or p > 1:
        raise ValueError(
            "p values should always be between 0 and 1. The "
            f"provided value of {p} is out of these boundaries"
        )
    elif p == 0 or p == 1:
        LGR.warning(
            f"The selected p value of {p} is at the limits of the "
            "possible range of [0, 1]. Statistical thresholding might "
            "not be interpretable."
        )

    if surr.ndim < 3:
        LGR.warning(
            f"Warning: surrogate dimensions ({surr.ndim}) are less than "
            "the program expects - check that you mean to run a test on "
            "an average or that you have enough surrogates."
        )

    # Reorder the surrogate matrix, then find where the real surrogate is
    LGR.info("Reordering surrogates for test")
    real_idx = surr.shape[-1] - 1
    reord_surr = np.argsort(surr, axis=-1) == real_idx

    LGR.info(f"Adopting {method} testing method.")
    # Testing both tails requires to split p
    if method == "frequentist":
        LGR.info(f"Testing for p={p} two-tails (p={p/2} each tail)")
        p = p / 2
        # If there aren't enough surrogates, send a warning message on the real p
        # Then update p
        if 1 / surr.shape[-1] > p:
            LGR.warning(
                "The generated surrogates are not enough to test for "
                f"the selected p ({p*2} two-tails), since at least "
                f"{ceil(1/p)-1} surrogates are required for the selected "
                f"p value. Testing for p={1/surr.shape[-1]} two-tails instead."
            )
            p = 1 / surr.shape[-1]

    elif method == "Bernoulli":
        # If there aren't enough subjects, send a warning message on the real p
        # Then update group level p
        if p_bernoulli is None:
            p_bernoulli = deepcopy(p)
            p = 0.1
        if 1 / surr.shape[1] > p_bernoulli:
            LGR.warning(
                "The provided subjects are not enough to test for "
                f"p={p_bernoulli} one-tail at the group level, since "
                f"at least {ceil(1/p_bernoulli)} subjects are required."
            )
            p_bernoulli = 1 / surr.shape[1]
        # If there aren't enough surrogates, send a warning message on the real p
        # Then update subject level p
        if 1 / surr.shape[-1] > p:
            LGR.warning(
                "The generated surrogates are not enough to test for "
                f"p={p} two-tails at the subject level. "
                f"{ceil(1/p)-1} surrogates are required for p={p}."
            )
            p = 1 / surr.shape[-1]

        LGR.info(
            f"Testing for p={p_bernoulli} one-tail at the group level and "
            f"at p={p*2} two-tails (p={p} each tail) at the subject level."
        )
    else:
        raise NotImplementedError(
            "Other testing methods than Bernoulli or "
            "frequentist are not implemented at the moment."
        )

    # First, and no matter what, apply frequentist approach to find where
    # the real data index (real_idx) is at the extremes of the matrix last axis
    # (with tolerance on the extremes depending on p).
    # real_idx serendipitously is the number of surrogates.
    stat_mask = reord_surr[..., : floor(real_idx * p) + 1].any(axis=-1) + reord_surr[
        ..., -floor(real_idx * p) - 1 :
    ].any(axis=-1)

    if method == "Bernoulli" and surr.shape[1] > 1 and surr.ndim >= 3:
        # The following computes the CDF of a binomial distribution
        # Difference with scipy's binom.cdf (100 samples) is: 5.066394802133445e-06
        # #!# See if there is a quicker way to get this (probably invert testing)

        def _pmf(x, n, p):
            f = (
                (factorial(n) / (factorial(x) * factorial(n - x)))
                * p**x
                * (1 - p) ** (n - x)
            )
            return f

        x = np.arange(0, 100, 1)
        # Generate the PMF of the binomial distribution
        y = np.asarray([_pmf(i, 100, p) for i in x], dtype="float32")
        # Generate the CDF, then invert it.
        y = 1 - np.cumsum(y)
        # Find the number of subjects necessary to be statistically significant,
        # adjusted for the number of subjects in the surrogates.
        # Then find all parcels for which the real data is higher or lower
        # than all surrogates in enough subjects.
        # The +1 in thr is to be conservative on the number of subjects.
        # p_bernoulli/surr.shape[0] is a Bonferroni correction.
        thr = x[y < p_bernoulli / surr.shape[0]][0]
        thr = np.floor(surr.shape[1] / 100 * thr) + 1
        # On top of the frequentist approach, find the parcels that pop up
        # in the frequentist approach for enough subjects.
        stat_mask = stat_mask.sum(axis=1) > thr
        # repeat stat_mask for the number of subjects.
        stat_mask = stat_mask[..., np.newaxis].repeat(surr.shape[1], axis=-1)
    elif surr.shape[1] == 1 and surr.ndim >= 3:
        LGR.warning(
            'The "Bernoulli" method is a group test that requires '
            "multiple subjects to be run."
        )
    elif surr.ndim < 3:
        LGR.warning(
            "The dimensionality of the data is not enough to run "
            'the "Bernoulli" method.'
        )

    if return_masked:
        LGR.info("Returning masked empirical data")
        stat_mask = np.ma.array(
            data=surr[..., -1], mask=np.invert(stat_mask), fill_value=np.NINF
        ).squeeze()
    else:
        LGR.info("Returning mask")

    if mean and stat_mask.ndim >= 2:
        LGR.info("Returning average across subjects (axis 1)")
        stat_mask = stat_mask.mean(axis=1)

    if return_masked:
        stat_mask = stat_mask.filled()

    return stat_mask


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
