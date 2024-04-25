#!/usr/bin/env python3
"""
Operations for laplacian decomposition.

Attributes
----------
LGR
    Logger
"""

import logging
from copy import deepcopy

import numpy as np

LGR = logging.getLogger(__name__)


def compute_laplacian(mtx, negval="absolute", selfloops=False):
    """
    Compute Laplacian (L) matrix from a square matrix.

    mtx is supposed to be a connectivity matrix - its diagonal will be removed.
    L is obtained by subtracting the adjacency matrix from the degree matrix.

    Parameters
    ----------
    mtx : numpy.ndarray
        A square matrix
    negval : "absolute", "remove", or "rescale"
        The intended behaviour to deal with negative values in matrix:
        - "absolute" will take absolute values of the matrix
        - "remove" will set all negative elements to 0
        - "rescale" will rescale the matrix between 0 and 1.
        Default is "absolute".
    selfloops : "degree", bool, or numpy.ndarray
        Allow or remove self-loops in input matrix. A numpy array can be used to specify
        particular loops directly in the adjacency matrix.
        The degree matrix of the Adjacency matrix can also be used instead.
        In the last two cases, the degree matrix will be updated accordingly.
        Default is to remove self loops (False).

    Returns
    -------
    numpy.ndarray
        The laplacian of mtx
    numpy.ndarray
        The degree matrix of mtx as a (mtx.ndim-1)D array, updated with selfloops in
        case.

    Raises
    ------
    NotImplementedError
        If negval is not "absolute", "remove", or "rescale"
        If selfloop

    Notes
    -----
    https://en.wikipedia.org/wiki/Laplacian_matrix
    """
    mtx = deepcopy(mtx)
    if mtx.min() < 0:
        if negval == "absolute":
            mtx = abs(mtx)
        elif negval == "remove":
            mtx[mtx < 0] = 0
        elif negval == "rescale":
            mtx = (mtx - mtx.min()) / mtx.max()
        else:
            raise NotImplementedError(
                f'Behaviour "{negval}" to deal with negative values is not supported'
            )

    adjacency = deepcopy(mtx)

    if selfloops is False:
        adjacency[np.diag_indices(adjacency.shape[0])] = 0
    elif selfloops is True:
        pass
    elif type(selfloops) is np.ndarray:
        if selfloops.ndim > 1:
            raise NotImplementedError(
                "Multidimensional arrays are not implemented to specify self-loops"
            )
        if selfloops.shape[0] != mtx.shape[0]:
            raise ValueError(
                f"Array specified for self-loops has {selfloops.shape[0]} elements, "
                f"but specified matrix has {mtx.shape[0]} diagonal elements."
            )
        adjacency[np.diag_indices(adjacency.shape[0])] = selfloops
    elif selfloops == "degree":
        adjacency[np.diag_indices(adjacency.shape[0])] = 0
        adjacency[np.diag_indices(adjacency.shape[0])] = adjacency.sum(axis=1)
    else:
        raise NotImplementedError(
            f'Value "{selfloops}" for self-loops settings is not supported'
        )

    degree = adjacency.sum(axis=1)  # This is fixed to across columns

    degree_mat = np.zeros_like(mtx)
    degree_mat[np.diag_indices(degree_mat.shape[0])] = degree

    return degree_mat - adjacency, degree


def normalisation(lapl, degree, norm="symmetric", fix_zeros=True):
    """Normalise a Laplacian (L) matrix using either symmetric or random walk normalisation.

    Parameters
    ----------
    lapl : numpy.ndarray
        A square matrix that is a Laplacian, or a stack of Laplacian matrices.
    degree : np.ndarray or None, optional
        An array, a diagonal matrix, or a stack of either. This will be used as the
        the degree matrix for the normalisation.
        It's assumed that degree.ndim == lapl.ndim or degree.ndim == lapl.ndim-1.
    norm : ["symmetric", "symm", "random walk", "rw", random walk inflow", "rwi", "random walk outflow", "rwo"], str, optional
        The type of normalisation to perform. Default to symmetric.
        - "symmetric": D^(-1/2) @ L @ ^(-1/2), a.k.a. symmetric laplacian normalisation
        - "random walk", "random walk inflow": D^(-1) @ L, a.k.a. random walk
          It normalises the inflow, i.e. it is row-optimised (each row = 0).
          Normally used in e.g. consensus networks.
        - "random walk outflow": L @ D^(-1)
          It normalises the outflow, i.e. it is column-optimised (each column = 0).
          Normally used in e.g. physical distribution networks.
    fix_zeros : bool, optional
        Whether to change 0 elements in the degree matrix to 1 to avoid multiplying by
        0. Default is to do so.

    Returns
    -------
    numpy.ndarray
        The normalised laplacian

    Raises
    ------
    NotImplementedError
        If `lapl.ndim` - `degree.ndim` > 1
        If "norm" is not supported.
    ValueError
        If `d` in not a diagonal matrix or an array
        If `d` and `mtx` have different shapes.

    Notes
    -----
    https://en.wikipedia.org/wiki/Laplacian_matrix
    """  # noqa: E501
    deg = deepcopy(degree)
    if lapl.ndim - deg.ndim > 1:
        raise NotImplementedError(
            f"The provided degree matrix is {deg.ndim}D while the "
            f"provided laplacian matrix is {lapl.ndim}D."
        )
    elif lapl.ndim == deg.ndim:
        if not (deg.diagonal() == deg.sum(axis=1)).all():
            raise ValueError(
                "The provided degree matrix is not a diagonal matrix (or a stack of)."
            )
        deg = deepcopy(deg.diagonal())

    if deg.shape != lapl.shape[1:]:
        raise ValueError(
            f"The provided degree matrix has shape {deg.shape} while the "
            f"provided matrix has shape {lapl.shape}."
        )

    if fix_zeros:
        deg[deg == 0] = 1

    d = np.zeros_like(lapl)

    # Attention: using ** to compute inverses works only on arrays.
    # Diagonal matrices are ok, but off-diagonal elements needs to be set to 0.
    # Otherwise np.linalg.inv or np.linalg.pinv are necessary.
    if norm in ["symmetric", "symm"]:
        d[np.diag_indices(d.shape[0])] = deg ** (-1 / 2)
        return d @ lapl @ d
    elif norm in ["random walk", "rw", "random walk inflow", "rwi"]:
        d[np.diag_indices(d.shape[0])] = deg ** (-1)
        return d @ lapl
    elif norm in ["random walk outflow", "rwo"]:
        d[np.diag_indices(d.shape[0])] = deg ** (-1)
        return lapl @ d
    else:
        raise NotImplementedError(f'Normalisation type "{norm}" is not supported.')


def symmetric_normalised_laplacian(mtx, d=None, fix_zeros=True):
    """
    Compute symmetric normalised Laplacian (SNL) matrix.

    The SNL is obtained by pre- and post- multiplying mtx by the square root of the
    inverse of the diagonal and subtract the result from the identity matrix.
    Alternatively, it is possible to specify a different diagonal to do so.
    With zero-order nodes, the diagonals will contain 0s, returning a Laplacian
    with NaN elements. To avoid that, 0 elements in d will be changed to 1.

    Parameters
    ----------
    mtx : numpy.ndarray
        A [structural] matrix
    d : np.ndarray or None, optional
        Either an array or a diagonal matrix. If specified, d will be used as the
        **normalisation factor** (not the degree matrix).
    fix_zeros : bool, optional
        Whether to change 0 elements in the degree matrix to 1 to avoid multiplying by 0

    Returns
    -------
    numpy.ndarray
        The symmetric normalised laplacian of mtx

    Raises
    ------
        ValueError
            If `d` in not a diagonal matrix or an array
            If `d` and `mtx` have different shapes.

    Notes
    -----
    This is here mainly for tests and legacy code, but it would be better not to use it!

    https://en.wikipedia.org/wiki/Laplacian_matrix#Symmetrically_normalized_Laplacian_2
    """
    if d is not None:
        if d.ndim == 1:
            d = np.diag(d)
        elif not (np.diag(d) == d.sum(axis=-1)).all():
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

    identity_mat = np.zeros_like(colsum)
    identity_mat[colsum != 0] = 1
    identity_mat = np.diag(identity_mat)

    if fix_zeros:
        colsum[colsum == 0] = 1
    if d is None:
        d = np.diag(colsum ** (-1 / 2))

    symm_norm = d @ mtx @ d

    return identity_mat - symm_norm
    # ## Fix Identity matrix by giving


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
    Recompose a matrix from its eigenvalues and eigenvectors.

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
