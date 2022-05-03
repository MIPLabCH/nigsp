#!/usr/bin/env python3
"""Tests for operations.surrogates."""
import numpy as np
from numpy.random import rand, seed
from pytest import mark, raises

from nigsp.operations import surrogates


# ### Unit tests
def test_random_sign():
    n_surr = 4
    random_seed = 2
    eigenvec = rand(20)

    rs = surrogates.random_sign(eigenvec, n_surr, random_seed)

    seed(random_seed)

    rand_evec = np.empty_like(eigenvec, dtype='float32')
    rand_evec = rand_evec[..., np.newaxis].repeat(n_surr, axis=-1)
    for i in range(n_surr):
        r_sign = np.random.rand(eigenvec.shape[0]).round()
        r_sign[r_sign == 0] = -1
        rand_evec[..., i] = eigenvec * r_sign
    


# ### Break tests
