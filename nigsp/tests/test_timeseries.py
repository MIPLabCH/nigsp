#!/usr/bin/env python3
"""Tests for operations.timeseries."""

import numpy as np
from numpy.random import rand
from pytest import mark, raises

from nigsp.operations import timeseries
from nigsp.utils import prepare_ndim_iteration


# ### Unit tests
def test_normalise_ts():
    ts = np.arange(24).reshape(2, 3, 4, order="F")

    z = np.asarray([[-1, 0, 1], [-1, 0, 1]], dtype="float64")
    z = np.repeat(z[..., np.newaxis], 4, axis=-1)

    zg = np.arange(6).reshape(3, 2).T
    zg = (zg - zg.mean()) / zg.std(ddof=1)
    zg = np.repeat(zg[..., np.newaxis], 4, axis=-1)

    tsz = timeseries.normalise_ts(ts)

    tsgz = timeseries.normalise_ts(ts, globally=True)

    assert (tsz == z).all()
    assert (tsz.sum() - 0) < 1e-10
    assert (tsgz == zg).all()
    assert (tsgz.sum() - 0) < 1e-10

    ts = np.arange(4)
    assert (ts == timeseries.normalise_ts(ts)).all()


def test_spc_ts():
    ts = np.arange(24).reshape(2, 3, 4, order="F")
    spc = (ts - ts.mean(axis=1)[:, np.newaxis, ...]) / ts.mean(axis=1)[
        :, np.newaxis, ...
    ]
    spc[np.isnan(spc)] = 0

    spcg = (ts - ts.mean(axis=(0, 1))) / ts.mean(axis=(0, 1))
    spcg[np.isnan(spcg)] = 0

    tsspc = timeseries.spc_ts(ts)

    tsgspc = timeseries.spc_ts(ts, globally=True)

    assert (tsspc == spc).all()
    assert (tsspc.sum() - 0) < 1e-10
    assert (tsgspc == spcg).all()
    assert (tsgspc.sum() - 0) < 1e-10

    ts = np.arange(4)
    assert (ts == timeseries.spc_ts(ts)).all()


def test_demean_ts():
    ts = np.arange(24).reshape(2, 3, 4, order="F")

    dm = np.asarray([[-2, 0, 2], [-2, 0, 2]], dtype="float64")
    dm = np.repeat(dm[..., np.newaxis], 4, axis=-1)

    dmg = np.repeat(
        np.arange(-2.5, 2.6, 1).reshape(3, 2).T[..., np.newaxis], 4, axis=-1
    )

    tsdm = timeseries.demean_ts(ts)

    tsgdm = timeseries.demean_ts(ts, globally=True)

    assert (tsdm == dm).all()
    assert (tsgdm == dmg).all()

    ts = np.arange(4)
    assert (ts == timeseries.demean_ts(ts)).all()


def test_rescale_ts():
    ts = np.arange(24).reshape(2, 3, 4, order="F")

    res = np.asarray([[1, 1.5, 2], [1, 1.5, 2]], dtype="float64")
    res = np.repeat(res[..., np.newaxis], 4, axis=-1)

    resg = np.repeat(
        np.arange(1, 2.1, 0.2).round(1).reshape(3, 2).T[..., np.newaxis], 4, axis=-1
    )

    tsres = timeseries.rescale_ts(ts, vmin=1, vmax=2)

    tsgres = timeseries.rescale_ts(ts, vmin=1, vmax=2, globally=True)

    assert (tsres == res).all()
    assert (tsgres == resg).all()

    ts = np.arange(4)
    assert (ts == timeseries.rescale_ts(ts)).all()


def test_resize_ts():
    ts = np.arange(24).reshape(2, 3, 4, order="F")
    gsr = np.repeat(
        np.repeat(
            np.asarray([-0.5, 0.5], dtype="float64")[..., np.newaxis], 3, axis=-1
        )[..., np.newaxis],
        4,
        axis=-1,
    )

    tsgsr = timeseries.resize_ts(ts, resize="gsr")

    assert (tsgsr == gsr).all()
    assert (ts == timeseries.resize_ts(ts)).all()

    ts = np.arange(4)
    assert (ts == timeseries.resize_ts(ts)).all()


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


# ### Break tests
def test_break_resize_ts():
    with raises(NotImplementedError) as errorinfo:
        timeseries.resize_ts(np.arange(6).reshape(2, 3), resize=[2, 3, 4])
    assert "two elements" in str(errorinfo.value)

    with raises(NotImplementedError) as errorinfo:
        timeseries.resize_ts(np.arange(6).reshape(2, 3), resize="Jonah")
    assert "method Jonah" in str(errorinfo.value)


def test_break_median_cutoff_frequency_idx():
    with raises(NotImplementedError) as errorinfo:
        timeseries.median_cutoff_frequency_idx(rand(2, 3, 4))
    assert "have 3 dimensions" in str(errorinfo.value)


@mark.parametrize("freq", [(0), (2), (4)])
def test_break_graph_filter(freq):
    with raises(IndexError) as errorinfo:
        timeseries.graph_filter(rand(2, 3), rand(2, 2), freq)
    assert f"index {freq} is not valid" in str(errorinfo.value)
