#!/usr/bin/env python3
"""Tests for utils."""

from numpy import ndarray
from numpy.random import rand
from pytest import mark, raises

from nigsp import utils


# ### Unit tests
@mark.parametrize('var, dtype', [
    (6, int),
    (4.2, float),
    ('hello', str),
    (rand(3), ndarray),
    ([1, 1, 2, 3, 5], list),
    ('6', int),
    (4, float),
    (42, str),
    ('hi', list),
    ([1, 1, 2, 3, 5], ndarray)
])
def test_if_declared_force_type(var, dtype):
    """Test if_declared_force_type."""
    # #!# Test logger!
    var_out = utils.if_declared_force_type(var, dtype, stop=False)

    assert type(var_out) == dtype


# ### Break tests
@mark.parametrize('var, dtype', [
    ('6', int),
    (4, float),
    (42, str),
    ('hi', list),
    ([1, 1, 2, 3, 5], ndarray)
])
def test_break_if_declared_force_type(var, dtype):
    """Break if_declared_force_type."""
    with raises(TypeError) as errorinfo:
        utils.if_declared_force_type(var, dtype)
    assert 'is not of type' in str(errorinfo.value)


def test_break_if_declared_force_type_dtype():
    """Break if_declared_force_type."""
    with raises(NotImplementedError) as errorinfo:
        utils.if_declared_force_type(6, bool, stop=False)
    assert 'not supported' in str(errorinfo.value)
