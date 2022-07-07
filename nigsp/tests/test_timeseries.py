#!/usr/bin/env python3
"""Tests for operations.timeseries."""

from numpy.random import rand
from pytest import mark, raises

from nigsp.operations import timeseries


# ### Unit tests
def test_normalise_ts():
    pass


def test_graph_fourier_transform():
    pass


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
