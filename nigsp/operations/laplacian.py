#!/usr/bin/env python3
"""
Operations for laplacian decomposition.

Attributes
----------
LGR
    Logger
"""

import logging

import numpy as np

LGR = logging.getLogger(__name__)


def symmetric_normalisation(mtx, d=None, fix_zeros=True):
    """
    Compute symmetrically normalised Laplacian (SNL) matrix.

    The SNL is obtained by pre- and post- multiplying mtx by its diagonal.
    Alternatively, it is possible to specify a different diagonal to do so.
    With zero-order nodes, the diagonals will contain 0s, returning a Laplacian
    with NaN elements. To avoid that, 0 elements in d will be changed to 1.

    Parameters
    ----------
    mtx : numpy.ndarray
        A [structural] matrix
    d : np.ndarray or None, optional
        Either an array or a
    fix_zeros : bool, optional
        Description

    Returns
    -------
    numpy.ndarray
        The symmetrically normalised version of mtx

    See Also
    --------
    https://en.wikipedia.org/wiki/Laplacian_matrix#Symmetrically_normalized_Laplacian_2
    """

    if d is not None:
        if d.ndim == 1:
            if d.size == 0:
                raise ValueError("The provided diagonal is empty.")
            d = np.diag(d)
        else:
            if not (np.diag(d) == d.sum(axis=-1)).all():
                raise ValueError(
                    "The provided matrix for symmetric normalisation "
                    "is not a diagonal matrix."
                )
        if d.shape != mtx.shape:
            raise ValueError(
                f"The provided diagonal has shape {d.shape} while the "
                f"provided matrix has shape {mtx.shape}."
            )

    colsum = mtx.sum(axis=-1)
    if fix_zeros:
        colsum[colsum == 0] = 1
    if d is None:
        d = np.diag(colsum ** (-1 / 2))

    symm_norm = d @ mtx @ d

    return np.eye(mtx.shape[0]) - symm_norm


def decomposition(mtx):
    """
    Run a eigenvector decomposition on input.

    Parameters
    ----------
    mtx : numpy.ndarray
        The matrix to decompose

    Returns
    -------
    numpy.ndarray
        The eigenvalues resulting from the decomposition
    numpy.ndarray
        The eigenvectors resulting from the decomposition
    """
    eigenval, eigenvec = np.linalg.eig(mtx)

    idx = np.argsort(eigenval)
    eigenval = eigenval[idx]
    # #!# Check that eigenvec has the right index and not inverted
    eigenvec = eigenvec[:, idx]

    return eigenval, eigenvec


def recomposition(eigenval, eigenvec):
    """
    Recompose a matrxi from its eigenvalues and eigenvectors.

    At the moment, it supports only 2D (not stacks).

    Parameters
    ----------
    eigenval : numpy.ndarray
        Array of eigenvalues. The program detects if it's a diagonal matrix or not.
    eigenvec : numpy.ndarray
        Matrix of eigenvectors.

    Returns
    -------
    numpy.ndarray
        The reconstructed matrix
    """
    if eigenvec.ndim > 2:
        raise NotImplementedError(
            f"Given matrix dimensionality ({eigenvec.ndim}) is not supported."
        )

    if eigenval.ndim == eigenvec.ndim - 1:
        eigenval = np.diag(eigenval)
    elif eigenval.ndim < eigenvec.ndim - 1:
        raise ValueError("Not enough dimensions in given eigenvalue matrix.")
    elif eigenval.ndim > eigenvec.ndim:
        raise ValueError("Too many dimensions in given eigenvalue matrix.")
    elif not (np.diag(eigenval) == eigenval.sum(axis=-1)).all():
        raise ValueError("The provided eigenvalue matrix is not a diagonal matrix.")

    mtx = eigenvec @ eigenval @ eigenvec.T

    return mtx


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
