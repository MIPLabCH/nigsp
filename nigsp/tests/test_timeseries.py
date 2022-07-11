#!/usr/bin/env python3
"""Tests for operations.timeseries."""

import numpy as np
from numpy.random import rand
from pytest import mark, raises

from nigsp.operations import timeseries
from nigsp.utils import prepare_ndim_iteration


# ### Unit tests
def test_normalise_ts():
    ts = rand(3, 20)
    z = ((ts - ts.mean(axis=1)[:, np.newaxis, ...]) /
         ts.std(axis=1, ddof=1)[:, np.newaxis, ...])
    z[np.isnan(z)] = 0

    tsz = timeseries.normalise_ts(ts)

    assert (tsz == z).all()


def test_graph_fourier_transform():
    ts = rand(3, 6)
    ev = rand(3, 3)
    pr = ev.conj().T @ ts

    proj = timeseries.graph_fourier_transform(ts, ev)

    assert (proj == pr).all()

    ts = rand(3, 6, 2, 2)
    tsr, pr = prepare_ndim_iteration(ts, 2)

    for i in range(2):
        pr[:, :, i] = ev.conj().T @ np.squeeze(tsr[:, :, i])
    pr = pr.reshape(ts.shape)
    prm = pr.mean(axis=1)
    engm = (pr ** 2).mean(axis=1)

    proj = timeseries.graph_fourier_transform(ts, ev, mean=True)
    eng = timeseries.graph_fourier_transform(ts, ev, energy=True, mean=True)

    assert (proj == prm).all()
    assert (eng == engm).all()


def test_median_cutoff_frequency_idx():
    pass


def test_graph_filter():
    pass


def test_functional_connectivity():
    pass


# ### Break tests
def test_break_median_cutoff_frequency_idx():
    with raises(NotImplementedError) as errorinfo:
        timeseries.median_cutoff_frequency_idx(rand(2, 3, 4))
    assert 'have 3 dimensions' in str(errorinfo.value)


@mark.parametrize('freq', [
    (0),
    (2),
    (4)
])
def test_break_graph_filter(freq):
    with raises(IndexError) as errorinfo:
        timeseries.graph_filter(rand(2, 3), rand(2, 2), freq)
    assert f'index {freq} is not valid' in str(errorinfo.value)
