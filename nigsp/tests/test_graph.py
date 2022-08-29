#!/usr/bin/env python3
"""Tests for operations.graph."""

import numpy as np

from nigsp.operations import graph


# ### Unit tests
def test_zerocross():
    """Test zerocross with legendre polynomials."""

    def _bonnet(d, x):
        if d == 0:
            return np.ones_like(x)
        elif d == 1:
            return x
        else:
            return (
                (2 * d - 1) * x * _bonnet(d - 1, x) - (d - 1) * _bonnet(d - 2, x)
            ) / d

    x = np.linspace(-1, 1, 100)
    legendre = np.empty([100, 5], dtype="float32")
    for n in range(5):
        legendre[:, n] = _bonnet(n, x)

    zx = np.linspace(0, 4, 5)

    assert all(zx == graph.zerocross(legendre))


def test_nodestrength():
    """Test nodestrength with random matrix."""
    a = np.random.rand(3, 3)
    a = a - a.mean()
    b = np.abs(a)
    s = b.sum(axis=0)
    f = s.mean(axis=-1)

    n = graph.nodestrength(a)
    m = graph.nodestrength(b)
    o = graph.nodestrength(a, mean=True)

    assert all(n == m)
    assert all(n == s)
    assert f == o
