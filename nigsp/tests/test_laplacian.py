#!/usr/bin/env python3
"""Tests for operations.laplacian."""
from os import remove

import numpy as np
from pymatreader import read_mat
from pytest import raises

from nigsp.operations import laplacian


# ### Unit tests
def test_symmetric_norm(sc_mtx):
    mtx = read_mat(sc_mtx)
    mtx = mtx["SC_avg56"]

    d = np.diag(mtx.sum(axis=-1) ** (-1 / 2))

    symm_norm = d @ mtx @ d

    lapl_in = np.eye(mtx.shape[0]) - symm_norm
    lapl_out = laplacian.symmetric_normalisation(mtx)

    assert (lapl_in == lapl_out).all()

    dg1 = np.diag(np.ones(mtx.shape[0]))
    lapl_in = np.eye(mtx.shape[0]) - (dg1 @ mtx @ dg1)
    lapl_out = laplacian.symmetric_normalisation(mtx, dg1)

    assert (lapl_in == lapl_out).all()

    dgv1 = np.ones(mtx.shape[0])
    lapl_out = laplacian.symmetric_normalisation(mtx, dgv1)

    assert (lapl_in == lapl_out).all()

    remove(sc_mtx)


def test_decomposition(sc_mtx):
    mtx = read_mat(sc_mtx)
    mtx = mtx["SC_avg56"]

    eival, eivec = np.linalg.eig(mtx)

    idx = np.argsort(eival)
    eival = eival[idx]
    # #!# Check that eigenvec has the right index and not inverted
    eivec = eivec[:, idx]

    eigenval, eigenvec = laplacian.decomposition(mtx)

    assert (eival == eigenval).all()
    assert (eivec == eigenvec).all()

    remove(sc_mtx)


# ### Break tests
def test_break_decomposition():

    mtx = np.random.rand(4, 4)

    d = np.empty(0)
    with raises(ValueError) as errorinfo:
        laplacian.symmetric_normalisation(mtx, d)
    assert "is empty" in str(errorinfo.value)

    d = np.diag(np.ones(4), k=1)
    with raises(ValueError) as errorinfo:
        laplacian.symmetric_normalisation(mtx, d)
    assert "not a diagonal" in str(errorinfo.value)

    d = np.diag(np.ones(3))
    with raises(ValueError) as errorinfo:
        laplacian.symmetric_normalisation(mtx, d)
    assert "has shape" in str(errorinfo.value)
