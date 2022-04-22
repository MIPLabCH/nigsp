#!/usr/bin/env python3
"""Tests for objects."""

import numpy as np
from numpy.random import rand

from pytest import mark, raises

from nigsp.objects import SCGraph


# ### Unit tests
def test_SCGraph():
    """Test SCGraph, properties, and methods."""
    mtx = rand(4, 4)
    timeseries = rand(4, 6)
    atlas = rand(4, 3)
    filename = 'Laudna.nii.gz'

    scgraph = SCGraph(mtx, timeseries, atlas=atlas, filename=filename,
                      ts_split={'hi': rand(4, 6), 'lo': rand(4, 6)})

    # Assert properties


    pass


# ### Break tests
def test_break_SCGraph():
    """Break SCGraph and its methods."""
    with raises(ValueError) as errorinfo:
        scgraph = SCGraph(rand(3, 4), rand(4, 6))
    assert 'square matrix' in str(errorinfo.value)

    with raises(ValueError) as errorinfo:
        scgraph = SCGraph(rand(4, 4), rand(3, 6))
    assert 'number of parcels and nodes' in str(errorinfo.value)

    with raises(ValueError) as errorinfo:
        scgraph = SCGraph(rand(4, 4), rand(4, 6, 4, 5))
    assert 'more than 3 dimensions' in str(errorinfo.value)

    scgraph = SCGraph(rand(4, 4), rand(4, 6), index='Chet')
    with raises(ValueError) as errorinfo:
        scgraph = scgraph.split_graph()
    assert 'Unknown option Chet' in str(errorinfo.value)

    scgraph = SCGraph(rand(4, 4), rand(4, 6))
    with raises(ValueError) as errorinfo:
        scgraph = scgraph.create_surrogates(sc_type='Fearne')
    assert 'Unknown option Fearne' in str(errorinfo.value)
