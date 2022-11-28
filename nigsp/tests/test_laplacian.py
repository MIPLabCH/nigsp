#!/usr/bin/env python3
"""Tests for operations.laplacian."""
from copy import deepcopy as dc

import numpy as np
from pytest import mark, raises

from nigsp.operations import laplacian


# ### Unit tests
def test_compute_laplacian():
    def glap(mtx):
        deg = mtx.sum(axis=1)
        adj = dc(mtx)
        adj[np.diag_indices(mtx.shape[0])] = 0

        L = np.diag(deg) - adj
        return L, deg

    mtx = np.random.rand(4, 4)
    mtx = (mtx + mtx.T) / 2

    L, deg = glap(mtx)
    lapl, degree = laplacian.compute_laplacian(mtx)

    assert (lapl == L).all()
    assert (degree == deg).all()

    mtx = mtx - mtx.mean()

    mtx_abs = abs(mtx)
    mtx_rem = dc(mtx)
    mtx_rem[mtx < 0] = 0
    mtx_res = (mtx - mtx.min()) / mtx.max()

    L, deg = glap(mtx_abs)
    lapl, degree = laplacian.compute_laplacian(mtx, negval="absolute")
    assert (lapl == L).all()
    assert (degree == deg).all()

    L, deg = glap(mtx_rem)
    lapl, degree = laplacian.compute_laplacian(mtx, negval="remove")
    assert (lapl == L).all()
    assert (degree == deg).all()

    L, deg = glap(mtx_res)
    lapl, degree = laplacian.compute_laplacian(mtx, negval="rescale")
    assert (lapl == L).all()
    assert (degree == deg).all()


@mark.xfail
def test_normalisation():

    L = np.random.rand(4, 4)
    L = (L + L.T) / 2
    d = np.random.rand(4)
    d[2] = 0

    lapl_symm = laplacian.normalisation(L, d, norm="symmetric")

    d = np.diag(d)
    lapl_rw = laplacian.normalisation(L, d, norm="random walk")

    d[2] = 1
    d_symm = np.diag(d ** (-1 / 2))
    d_rw = np.diag(d ** (-1))

    assert (lapl_symm == (d_symm @ L @ d_symm)).all()
    assert (lapl_rw == d_rw @ L).all()


def test_symmetric_normalised_laplacian():
    mtx = np.random.rand(4, 4)
    mtx = (mtx + mtx.T) / 2

    d = np.diag(mtx.sum(axis=-1) ** (-1 / 2))

    symm_norm = d @ mtx @ d

    lapl_in = np.eye(mtx.shape[0]) - symm_norm
    lapl_out = laplacian.symmetric_normalised_laplacian(mtx)

    assert (lapl_in == lapl_out).all()

    dg1 = np.diag(np.ones(mtx.shape[0]))
    lapl_in = np.eye(mtx.shape[0]) - (dg1 @ mtx @ dg1)
    lapl_out = laplacian.symmetric_normalised_laplacian(mtx, dg1)

    assert (lapl_in == lapl_out).all()

    dgv1 = np.ones(mtx.shape[0])
    lapl_out = laplacian.symmetric_normalised_laplacian(mtx, dgv1)

    assert (lapl_in == lapl_out).all()


def test_decomposition():
    mtx = np.random.rand(4, 4)
    mtx = (mtx + mtx.T) / 2

    eival, eivec = np.linalg.eig(mtx)

    idx = np.argsort(eival)
    eival = eival[idx]
    eivec = eivec[:, idx]

    eigenval, eigenvec = laplacian.decomposition(mtx)

    assert (eival == eigenval).all()
    assert (eivec == eigenvec).all()


def test_recomposition():
    mtx = np.random.rand(4, 4)
    mtx = (mtx + mtx.T) / 2

    eival, eivec = np.linalg.eig(mtx)

    idx = np.argsort(eival)
    eival = eival[idx]
    eivec = eivec[:, idx]

    mtx_rec = laplacian.recomposition(eival, eivec)

    assert abs(mtx - mtx_rec).sum().round(6) < 10**-6


# ### Break tests
def test_break_compute_laplacian():
    mtx = np.random.rand(4, 4)
    mtx = mtx - mtx.mean()
    with raises(NotImplementedError) as errorinfo:
        laplacian.compute_laplacian(mtx, negval="random")
    assert 'Behaviour "random" to deal' in str(errorinfo.value)


def test_break_normalisation():
    lapl = np.random.rand(4, 4, 4)
    d = np.random.rand(4)
    with raises(NotImplementedError) as errorinfo:
        laplacian.normalisation(lapl, d)
    assert "degree matrix is 1D" in str(errorinfo.value)

    lapl = np.random.rand(4, 4)
    d = np.diag(d)
    d[1, 2] = 1
    with raises(ValueError) as errorinfo:
        laplacian.normalisation(lapl, d)
    assert "not a diagonal matrix" in str(errorinfo.value)

    d = np.random.rand(6)
    with raises(ValueError) as errorinfo:
        laplacian.normalisation(lapl, d)
    assert "degree matrix has shape" in str(errorinfo.value)

    d = np.random.rand(4)
    with raises(NotImplementedError) as errorinfo:
        laplacian.normalisation(lapl, d, norm="echo")
    assert 'Normalisation type "echo"' in str(errorinfo.value)


def test_break_symmetric_normalised_laplacian():

    mtx = np.random.rand(4, 4)

    d = np.diag(np.ones(4), k=1)
    with raises(ValueError) as errorinfo:
        laplacian.symmetric_normalised_laplacian(mtx, d)
    assert "not a diagonal" in str(errorinfo.value)

    d = np.diag(np.ones(3))
    with raises(ValueError) as errorinfo:
        laplacian.symmetric_normalised_laplacian(mtx, d)
    assert "has shape" in str(errorinfo.value)


def test_break_recomposition():

    eivec = np.random.rand(4, 4, 2)
    eival = np.random.rand(4)

    with raises(NotImplementedError) as errorinfo:
        laplacian.recomposition(eival, eivec)
    assert "matrix dimensionality (3)" in str(errorinfo.value)

    eivec = np.random.rand(4, 4)
    # with raises(ValueError) as errorinfo:
    #     laplacian.recomposition(eival, eivec)
    # assert "Not enough dimensions" in str(errorinfo.value)

    eival = np.random.rand(4, 4)
    with raises(ValueError) as errorinfo:
        laplacian.recomposition(eival, eivec)
    assert "not a diagonal" in str(errorinfo.value)

    eival = np.random.rand(4, 4, 6)
    with raises(ValueError) as errorinfo:
        laplacian.recomposition(eival, eivec)
    assert "Too many dimensions" in str(errorinfo.value)
