#!/usr/bin/env python3
"""Tests for operations.laplacian."""
from os import remove

import numpy as np
from pymatreader import read_mat

from nigsp.operations import laplacian


# ### Unit tests
def test_symmetric_norm(sc_mtx):
    mtx = read_mat(sc_mtx)
    mtx = mtx['SC_avg56']

    d = np.diag(mtx.sum(axis=-1) ** (-1/2))

    symm_norm = (d @ mtx @ d)

    lapl_in = np.eye(mtx.shape[0]) - symm_norm
    lapl_out = laplacian.symmetric_normalisation(mtx)

    assert (lapl_in == lapl_out).all()

    remove(sc_mtx)


def test_decomposition(sc_mtx):
    mtx = read_mat(sc_mtx)
    mtx = mtx['SC_avg56']

    eival, eivec = np.linalg.eig(mtx)

    idx = np.argsort(eival)
    eival = eival[idx]
    # #!# Check that eigenvec has the right index and not inverted 
    eivec = eivec[:, idx]

    eigenval, eigenvec = laplacian.decomposition(mtx)

    assert (eival == eigenval).all()
    assert (eivec == eigenvec).all()

    remove(sc_mtx)
