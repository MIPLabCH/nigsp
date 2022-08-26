#!/usr/bin/env python3
"""Tests for objects."""

import numpy as np
from numpy.random import rand
from pytest import raises

from nigsp import operations
from nigsp.objects import SCGraph


# ### Unit tests
def test_SCGraph():
    """Test SCGraph, properties, and methods."""
    # # Initialise object
    # Initialise content
    mtx = rand(4, 4)
    timeseries = rand(4, 6)
    atlas = rand(4, 3)
    filename = "Laudna.nii.gz"
    ts_split = {"high": rand(4, 6), "low": rand(4, 6)}
    # Initialise eigenvec to check zerocross
    def _bonnet(d, x):
        if d == 0:
            return np.ones_like(x)
        elif d == 1:
            return x
        else:
            return (
                (2 * d - 1) * x * _bonnet(d - 1, x) - (d - 1) * _bonnet(d - 2, x)
            ) / d

    x = np.linspace(-1, 1, 4)
    eigenvec = np.empty([4, 4], dtype="float32")
    for n in range(4):
        eigenvec[:, n] = _bonnet(n, x)
    zx = np.linspace(0, 3, 4)

    # Initialise SCGraph proper
    scgraph = SCGraph(
        mtx,
        timeseries,
        atlas=atlas,
        filename=filename,
        eigenvec=eigenvec,
        ts_split=ts_split,
        index=2,
    )

    # # Assert properties
    assert scgraph.nnodes == mtx.shape[1]
    assert scgraph.ntimepoints == timeseries.shape[1]
    assert (scgraph.zerocross == zx).all()
    assert all(item in scgraph.split_keys for item in list(ts_split.keys()))

    # # Test methods
    # Only test split_graph, create_surrogates, compute_fc
    # Other methods are somewhat one-liner wrap-around of tested functions.

    # Test split_graph and split_graph index priority
    scgraph.split_graph()
    evs, tss = operations.graph_filter(timeseries, eigenvec, 2)
    # Update ts_split to be tss
    ts_split = tss

    assert all(item in list(evs.keys()) for item in list(scgraph.evec_split.keys()))
    assert all(item in list(tss.keys()) for item in list(scgraph.ts_split.keys()))
    assert (evs["low"] == scgraph.evec_split["low"]).all()
    assert (tss["low"] == scgraph.ts_split["low"]).all()

    scgraph.evec_split = {}
    scgraph.index = "median"
    scgraph.split_graph(index=2)

    assert (evs["low"] == scgraph.evec_split["low"]).all()

    # Test create_surrogates
    scgraph.create_surrogates(sc_type="informed", n_surr=1, seed=6)
    i_surr = operations.sc_informed(timeseries, eigenvec, n_surr=1, seed=6)
    assert (scgraph.surr == i_surr).all()

    scgraph.lapl_mtx = mtx
    scgraph.create_surrogates(sc_type="uninformed", n_surr=1, seed=6)
    u_surr = operations.sc_uninformed(timeseries, lapl_mtx=mtx, n_surr=1, seed=6)
    assert (scgraph.surr == u_surr).all()

    # Test compute_fc
    scgraph.compute_fc()
    fc = operations.functional_connectivity(timeseries)
    fc_low = operations.functional_connectivity(ts_split["low"])

    assert (fc == scgraph.fc).all()
    assert all(item in ["high", "low"] for item in list(scgraph.fc_split.keys()))
    assert (fc_low == scgraph.fc_split["low"]).all()


# ### Break tests
def test_break_SCGraph():
    """Break SCGraph and its methods."""
    with raises(ValueError) as errorinfo:
        SCGraph(rand(3, 4), rand(4, 6))
    assert "square matrix" in str(errorinfo.value)

    with raises(ValueError) as errorinfo:
        SCGraph(rand(4, 4), rand(3, 6))
    assert "number of parcels and nodes" in str(errorinfo.value)

    with raises(ValueError) as errorinfo:
        SCGraph(rand(4, 4), rand(4, 6, 4, 5))
    assert "more than 3 dimensions" in str(errorinfo.value)

    scgraph = SCGraph(rand(4, 4), rand(4, 6), index="Chet")
    with raises(ValueError) as errorinfo:
        scgraph.split_graph()
    assert "Unknown option Chet" in str(errorinfo.value)

    scgraph = SCGraph(rand(4, 4), rand(4, 6))
    with raises(ValueError) as errorinfo:
        scgraph.create_surrogates(sc_type="Fearne")
    assert "Unknown option Fearne" in str(errorinfo.value)
