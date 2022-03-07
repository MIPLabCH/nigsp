#!/usr/bin/env python3
"""
Surrogate utility.

Attributes
----------
LGR
    Logger
"""

import logging

from math import factorial, floor

import numpy as np

from .timeseries import graph_fourier_transform
from .laplacian import decomposition


LGR = logging.getLogger(__name__)
SURR_TYPE = ['informed', 'uninformed']
STAT_METHOD = ['Bernoulli', 'frequentist']


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
    # #!# Allow for input of random sign matrix, if None call random sign.
    if seed is not None:
        # Reinitialise the random seed for repeatability
        np.random.rand(seed)

    if eigenvec.ndim > 3:
        raise NotImplementedError(f'Provided data has {eigenvec.ndim} dimensions, '
                                  'but data of more than 3 dimensions are not '
                                  'supported yet')

    rand_evec = np.empty_like(eigenvec, dtype='float32')
    rand_evec = rand_evec[..., np.newaxis].repeat(n_surr, axis=-1)

    LGR.info('Randomly switching signs of eigenvectors to create surrogates.')
    for i in range(n_surr):
        # #!# Check if two conditions can be merged.
        if eigenvec.ndim < 3:
            r_sign = np.random.rand(eigenvec.shape[0]).round()
            r_sign[r_sign == 0] = -1
            rand_evec[..., i] = eigenvec * r_sign
        else:
            for j in range(eigenvec.shape[2]):
                r_sign = np.random.rand(eigenvec.shape[0]).round()
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

    surr = np.empty_like(timeseries, dtype='float32')
    surr = surr[..., np.newaxis].repeat(n_surr, axis=-1)

    fourier_coeff = graph_fourier_transform(timeseries, eigenvec)

    LGR.info('Projecting the timeseries onto the surrogate eigenvectors.')
    if stack:
        n_surr += 1
    for i in range(n_surr):
        if timeseries.ndim < 3 and rand_evec.ndim == timeseries.ndim+1:
            surr[..., i] = graph_fourier_transform(fourier_coeff, rand_evec[..., i].T)
        elif timeseries.ndim == 3:
            for j in range(timeseries.shape[2]):
                # #!# Check if two conditions can be merged.
                if rand_evec.ndim < 4:
                    surr[:, :, j, i] = graph_fourier_transform(fourier_coeff,
                                                               rand_evec[..., i].T)
                else:
                    surr[:, :, j, i] = graph_fourier_transform(fourier_coeff,
                                                               rand_evec[:, :, j, i].T)
        else:
            raise NotImplementedError('No solution implemented for timeseries '
                                      f'of {timeseries.ndim} dimensions and '
                                      f'eigenvector matrix of {eigenvec.ndim}')
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
        raise NotImplementedError(f'Provided timeseries has {timeseries.ndim} '
                                  'dimensions, but timeseries of more than 3 '
                                  'dimensions are not supported yet.')

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
        raise NotImplementedError(f'Provided timeseries has {timeseries.ndim} '
                                  'dimensions, but timeseries of more than 3 '
                                  'dimensions are not supported yet.')

    symm_norm = np.eye(lapl_mtx.shape[0]) - lapl_mtx
    symm_norm_sum = symm_norm.sum(axis=-1)

    conf_model = np.outer(symm_norm_sum,
                          symm_norm_sum.T) / symm_norm.sum()

    conf_lapl = np.diag(symm_norm_sum) - conf_model

    _, surr_eigenvec = decomposition(conf_lapl)

    return _create_surr(timeseries, surr_eigenvec, n_surr, seed, stack)


def test_significance(surr, data=None, method='Bernoulli', p=0.1,
                      return_masked=False, mean=False):
    """
    Test the significance of the empirical data against surrogates.

    Two methods are implemented, 'Bernoulli' and 'frequentist'.
    - 'Bernoulli' is a group test. It tests that the number of subjects for
      which the empirical data is higher (or lower) than all surrogates is at
      the tail of a binomial cumulative distribution (where 'tail' is defined by p).
    - 'frequentist' is a group or single subject test. It tests that the
      empirical data are in the highest (or lowest) percentile (where the
      percentile is defined by p).

    Note that p is expressed as two-tails test.

    Both surr and data are expected to have first dimensions: observations x [subjects].

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
        The probability threshold to adopt. Note that this is a two-tails test.
    return_masked : bool, optional
        If True, returns the masked data. If False, returns a mask that holds
        True where the masked data are (inverse of numpy mask).
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
    NotImplementedError
        If any other method rather than those listed above is selected.

    """
    # #!# Check that the surrogate shape has parcels in the first axis!
    # If provided, append data to surr
    if data is not None:
        if surr.shape[:data.ndim] != data.shape:
            raise ValueError('Provided empirical data and surrogate data shapes '
                             f'does not agree, with shapes {data.shape} and '
                             f'{surr.shape[:data.ndim]} (last axis excluded)')
        surr = np.append(surr, data[..., np.newaxis], axis=-1)

    # Reorder the surrogate matrix, then find where the real surrogate is
    LGR.info('Reordering surrogates for test')
    real_idx = surr.shape[-1]-1
    reord_surr = (np.argsort(surr, axis=-1) == real_idx)

    # Testing both tails requires to split p
    LGR.info(f'Testing for p={p} two-tails (p={p/2} each tail)')
    p = p / 2

    LGR.info(f'Adopting {method} method')
    if method == 'Bernoulli':
        # The following computes the CDF of a binomial distribution
        # Difference with scipy's binom.cdf (100 samples) is: 5.066394802133445e-06
        # #!# See if there is a quicker way to get this (probably invert testing)

        def _pmf(x, n, p):
            f = ((factorial(n) / (factorial(x) * factorial(n - x))) * p ** x *
                 (1 - p) ** (n - x))
            return f

        x = np.arange(0, 101, 1)
        # Generate the PMF of the binomial distribution
        y = np.asarray([_pmf(i, 100, p) for i in x], dtype='float32')
        # Generate the CDF, then invert it.
        y = 1 - np.cumsum(y)
        # Find the number of subjects necessary to be statistically significant,
        # adjusted for the number of subjects in the surrogates.
        # Then find all parcels for which the real surrogate is higher or lower
        # than all surrogates in enough subjects.
        # The +1 in thr is to be conservative on the number of subjects.
        thr = x[np.argwhere(y < p/surr.shape[0])]
        thr = np.floor(surr.shape[1] / 100 * thr)+1
        # #!# This is one sided so FIX P
        # #!# The last and first is just due to the number of surrogates but it should be frequentist.
        stat_mask = ((reord_surr[..., -1].sum(axis=1) > thr) +
                     (reord_surr[..., 0].sum(axis=1) > thr))
    elif method == 'frequentist':
        # real_idx serendipitously is the number of surrogates.
        stat_mask = (reord_surr[..., :floor(real_idx * p)].any(axis=-1) +
                     reord_surr[..., -floor(real_idx * p):].any(axis=-1))
    else:
        raise NotImplementedError('Other testing methods than Bernoulli or '
                                  'frequentist are not '
                                  'implemented at the moment.')

    if return_masked:
        LGR.info('Returning masked empirical data')
        stat_mask = surr[stat_mask, :, -1].squeeze()

        if mean and stat_mask.ndim == 2:
            LGR.info('Returning average')
            stat_mask = stat_mask.mean(axis=-1)
    else:
        LGR.info('Returning mask')

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
