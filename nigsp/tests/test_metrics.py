#!/usr/bin/env python3
"""Tests for operations.metrics."""

import numpy as np
from numpy.random import rand
from pytest import raises

from nigsp.operations import metrics
from nigsp.utils import prepare_ndim_iteration


# ### Unit tests
def test_sdi():

    ts1 = np.arange(1, 3)[..., np.newaxis]
    ts2 = np.arange(3, 5)[..., np.newaxis]
    ts3 = np.arange(5, 7)[..., np.newaxis]
    sdi_in = np.log2(np.arange(3.0, 1.0, -1.0))

    ts = {"low": ts1, "high": ts2}
    sdi_out = metrics.sdi(ts)
    assert (sdi_out == sdi_in).all()

    ts = {"HIGH": ts2, "LOW": ts1}
    sdi_out = metrics.sdi(ts)
    assert (sdi_out == sdi_in).all()

    ts = {"alpha": ts1, "beta": ts2, "gamma": ts3}
    sdi_out = metrics.sdi(ts, keys=["alpha", "beta"])
    assert (sdi_out == sdi_in).all()

    ts = {
        "low": np.repeat(np.repeat(ts1[..., np.newaxis], 3, axis=1), 3, axis=2),
        "high": np.repeat(np.repeat(ts2[..., np.newaxis], 3, axis=1), 3, axis=2),
    }
    sdi_out = metrics.sdi(ts, mean=True)
    sdi_out = np.around(sdi_out, decimals=15)
    assert (sdi_out == sdi_in).all()


def test_gsdi():
    ts1 = np.arange(1, 3)[..., np.newaxis]
    ts2 = np.arange(3, 5)[..., np.newaxis]
    ts3 = np.arange(5, 7)[..., np.newaxis]
    ts = {"alpha": ts1, "beta": ts2, "gamma": ts3}
    gsdi_in = np.log2(np.arange(3.0, 1.0, -1.0))
    gsdi_and_in = np.log2(
        np.linalg.norm(ts1, axis=1) / np.linalg.norm(np.add(ts2, ts3), axis=1)
    )
    # fmt: off
    keys_in = ['alpha_over_beta', 'alpha_over_gamma', 'alpha_over_(beta_and_gamma)',
               'beta_over_alpha', 'beta_over_gamma', 'beta_over_(alpha_and_gamma)',
               'gamma_over_alpha', 'gamma_over_beta', 'gamma_over_(alpha_and_beta)']
    # fmt: on
    gsdi_out = metrics.gsdi(ts)

    assert all(item in keys_in for item in list(gsdi_out.keys()))
    assert (gsdi_out["beta_over_alpha"] == gsdi_in).all()
    assert (gsdi_out["alpha_over_(beta_and_gamma)"] == gsdi_and_in).all()

    gsdi_out = metrics.gsdi(ts, keys=["alpha", "beta"])
    assert all(
        item in list(gsdi_out.keys()) for item in ["alpha_over_beta", "beta_over_alpha"]
    )
    assert (gsdi_out["beta_over_alpha"] == gsdi_in).all()

    ts = {
        "alpha": np.repeat(np.repeat(ts1[..., np.newaxis], 3, axis=1), 3, axis=2),
        "beta": np.repeat(np.repeat(ts2[..., np.newaxis], 3, axis=1), 3, axis=2),
    }
    gsdi_out = metrics.gsdi(ts, mean=True)
    gsdi_out["beta_over_alpha"] = np.around(gsdi_out["beta_over_alpha"], decimals=15)
    assert (gsdi_out["beta_over_alpha"] == gsdi_in).all()


# ### Break tests
def test_break_sdi():
    ts1 = np.arange(1, 3)[..., np.newaxis]
    ts2 = np.arange(3, 5)[..., np.newaxis]
    ts3 = np.arange(5, 7)[..., np.newaxis]
    ts = {"alpha": ts1, "beta": ts2, "gamma": ts3}

    with raises(ValueError) as errorinfo:
        metrics.sdi(ts, keys=["high", "low"])
    assert "provided keys" in str(errorinfo.value)

    with raises(ValueError) as errorinfo:
        metrics.sdi(ts)
    assert "exactly two" in str(errorinfo.value)


def test_break_gsdi():
    ts1 = np.arange(1, 3)[..., np.newaxis]
    ts2 = np.arange(3, 5)[..., np.newaxis]
    ts3 = np.arange(5, 7)[..., np.newaxis]
    ts = {"alpha": ts1, "beta": ts2, "gamma": ts3}

    with raises(ValueError) as errorinfo:
        metrics.gsdi(ts, keys=["physio", "lambda", "pi"])
    assert "provided keys" in str(errorinfo.value)


def test_functional_connectivity():
    assert metrics.functional_connectivity(rand(6)) == 1

    ts = rand(3, 6, 2, 2)

    tst, _ = prepare_ndim_iteration(ts, 2)
    fc = np.empty(([tst.shape[0]] * 2 + [tst.shape[-1]]), dtype="float32")
    for i in range(tst.shape[-1]):
        fc[:, :, i] = np.corrcoef(tst[..., i])

    ns = (ts.shape[0],) * 2 + ts.shape[2:]
    fc = fc.reshape(ns).mean(axis=2).squeeze()

    fc_t = metrics.functional_connectivity(ts, mean=True)

    assert (fc == fc_t).all()

    tsd = {"hi": rand(3, 6), "lo": rand(3, 6)}

    fcd = metrics.functional_connectivity(tsd)

    assert all(item in list(tsd.keys()) for item in list(fcd.keys()))

    for k in fcd.keys():
        assert (fcd[k] == np.corrcoef(tsd[k])).all()
