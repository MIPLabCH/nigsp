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


def symmetric_normalisation(mtx):
    """
    Compute symmetrically normalised Laplacian matrix.

    Parameters
    ----------
    mtx : numpy.ndarray
        A [structural] matrix

    Returns
    -------
    numpy.ndarray
        The symmetrically normalised version of mtx

    See Also
    --------
    https://en.wikipedia.org/wiki/Laplacian_matrix#Symmetrically_normalized_Laplacian_2
    """
    d = np.diag(mtx.sum(axis=-1) ** (-1/2))

    symm_norm = (d @ mtx @ d)

    return (np.eye(mtx.shape[0]) - symm_norm)


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
