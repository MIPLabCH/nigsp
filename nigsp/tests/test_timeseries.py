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
    z = (ts - ts.mean(axis=1)[:, np.newaxis, ...]) / ts.std(axis=1, ddof=1)[
        :, np.newaxis, ...
    ]
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

    for i in range(tsr.shape[-1]):
        pr[:, :, i] = ev.conj().T @ np.squeeze(tsr[:, :, i])
    pr = pr.reshape(ts.shape)
    prm = pr.mean(axis=1)
    engm = (pr**2).mean(axis=1)

    proj = timeseries.graph_fourier_transform(ts, ev, mean=True)
    eng = timeseries.graph_fourier_transform(ts, ev, energy=True, mean=True)

    assert (proj == prm).all()
    assert (eng == engm).all()


def test_median_cutoff_frequency_idx():
    energy = np.array([[0, 3], [1, 2], [0, 1], [0.5, 0.5]])
    freq_t = 2

    freq_idx = timeseries.median_cutoff_frequency_idx(energy)

    assert freq_t == freq_idx


def test_graph_filter():
    ts = rand(4, 10)
    ev = rand(4, 4)

    keys = ["hi", "ho"]
    freq_idx = 2

    ev_s = dict.fromkeys(keys)
    ts_s = dict.fromkeys(keys)

    ev_s["hi"] = np.append(
        ev[:, :freq_idx], np.zeros_like(ev[:, freq_idx:], dtype="float32"), axis=-1
    )
    ev_s["ho"] = np.append(
        np.zeros_like(ev[:, :freq_idx], dtype="float32"), ev[:, freq_idx:], axis=-1
    )

    fcf = timeseries.graph_fourier_transform(ts, ev)
    ts_s["ho"] = timeseries.graph_fourier_transform(fcf, ev_s["ho"].T)
    ts_s["hi"] = timeseries.graph_fourier_transform(fcf, ev_s["hi"].T)

    evec_split, ts_split = timeseries.graph_filter(ts, ev, freq_idx, keys)

    assert all(item in keys for item in list(evec_split.keys()))
    assert all(item in keys for item in list(ts_split.keys()))
    for k in keys:
        assert (ev_s[k] == evec_split[k]).all()
        assert (ts_s[k] == ts_split[k]).all()


def test_functional_connectivity():
    assert timeseries.functional_connectivity(rand(6)) == 1

    ts = rand(3, 6, 2, 2)

    tst, _ = prepare_ndim_iteration(ts, 2)
    fc = np.empty(([tst.shape[0]] * 2 + [tst.shape[-1]]), dtype="float32")
    for i in range(tst.shape[-1]):
        fc[:, :, i] = np.corrcoef(tst[..., i])

    ns = (ts.shape[0],) * 2 + ts.shape[2:]
    fc = fc.reshape(ns).mean(axis=2).squeeze()

    fc_t = timeseries.functional_connectivity(ts, mean=True)

    assert (fc == fc_t).all()

    tsd = {"hi": rand(3, 6), "lo": rand(3, 6)}

    fcd = timeseries.functional_connectivity(tsd)

    assert all(item in list(tsd.keys()) for item in list(fcd.keys()))

    for k in fcd.keys():
        assert (fcd[k] == np.corrcoef(tsd[k])).all()


# ### Break tests
def test_break_median_cutoff_frequency_idx():
    with raises(NotImplementedError) as errorinfo:
        timeseries.median_cutoff_frequency_idx(rand(2, 3, 4))
    assert "have 3 dimensions" in str(errorinfo.value)


@mark.parametrize("freq", [(0), (2), (4)])
def test_break_graph_filter(freq):
    with raises(IndexError) as errorinfo:
        timeseries.graph_filter(rand(2, 3), rand(2, 2), freq)
    assert f"index {freq} is not valid" in str(errorinfo.value)
