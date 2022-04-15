#!/usr/bin/env python3
"""Tests for operations.laplacian."""
from os.path import remove

import numpy as np

from nigsp.operations import laplacian


# ### Unit tests
def test_symmetric_norm(sc_mtx):

    d = np.diag(sc_mtx.sum(axis=-1) ** (-1/2))

    symm_norm = (d @ sc_mtx @ d)

    lapl_in = np.eye(sc_mtx.shape[0]) - symm_norm
    lapl_out = laplacian.symmetric_normalisation(sc_mtx)

    assert lapl_in == lapl_out

    remove(sc_mtx)


def test_decomposition(sc_mtx):

    eival, eivec = np.linalg.eig(sc_mtx)

    idx = np.argsort(eival)
    eival = eival[idx]
    # #!# Check that eigenvec has the right index and not inverted 
    eivec = eivec[:, idx]

    eigenval, eigenvec = laplacian.decomposition(sc_mtx)

    assert (eival == eigenval).all()
    assert (eivec == eigenvec).all()


# ### Break tests
