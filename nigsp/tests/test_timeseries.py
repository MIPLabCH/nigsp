#!/usr/bin/env python3
"""Tests for operations.timeseries."""

from numpy.random import rand
from pytest import mark, raises

from nigsp.operations import timeseries


# ### Unit tests

# ### Break tests
def test_break_median_cutoff_frequency_idx():
    with raises(NotImplementedError) as errorinfo:
        timeseries.median_cutoff_frequency_idx(rand(2, 3, 4))
    assert 'have 3 dimensions' in str(errorinfo.value)


@mark.parametrize('data', [
    (rand(3, 4)),
    (rand(3, 4, 1)),
    (rand(3, 1, 4))
])
def test_break_graph_filter(data):
    with raises(IndexError) as errorinfo:
        timeseries.graph_filter(rand(2, 3, 4))
    assert 'has 3 dimensions' in str(errorinfo.value)

