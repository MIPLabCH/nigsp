#!/usr/bin/env python3
"""Tests for viz."""

import sys
from os import remove
from os.path import isfile

import matplotlib
import nibabel
import nilearn
from nibabel.filebasedimages import ImageFileError
from numpy import genfromtxt
from numpy.random import rand
from pytest import mark, raises

from nigsp import viz


@mark.parametrize('mxt', [
    (rand(3, 4)),
    (rand(4, 4)),
    (rand(4, 4, 3)),
    (rand(4, 4, 3, 1))
])
# ### Unit tests
def test_plot_connectivity(mtx):
    viz.plot_connectivity(mtx, 'arthur.png')

    assert isfile('arthur.png')
    remove('arthur.png')


@mark.parametrize('timeseries', [
    (rand(3, 50)),
    (rand(3, 50, 3)),
    (rand(3, 50, 4, 1))
])
def test_plot_grayplot(timeseries):
    viz.plot_grayplot(timeseries, 'dot.png')

    assert isfile('dot.png')
    remove('dot.png')


def test_plot_nodes(sdi, atlas):
    ns = genfromtxt(sdi)
    viz.plot_nodes(ns, atlas, 'joan.png')

    assert isfile('joan.png')
    remove('joan.png')


# ### Break tests
def test_break_plot_connectivity():
    sys.modules['matplotlib'] = None
    with raises(ImportError) as errorinfo:
        viz.plot_connectivity(rand(3, 3), 'steve.png')
    assert 'is required' in str(errorinfo.value)
    sys.modules['matplotlib'] = matplotlib

    with raises(ValueError) as errorinfo:
        viz.plot_connectivity(rand(3, 3, 3, 4), 'steve.png')
    assert 'plot connectivity' in str(errorinfo.value)


def test_break_plot_grayplot():
    sys.modules['matplotlib'] = None
    with raises(ImportError) as errorinfo:
        viz.plot_grayplot(rand(3, 3), 'ramsey.png')
    assert 'is required' in str(errorinfo.value)
    sys.modules['matplotlib'] = matplotlib

    with raises(ValueError) as errorinfo:
        viz.plot_grayplot(rand(3, 3, 3, 4), 'ramsey.png')
    assert 'plot grayplots' in str(errorinfo.value)


def test_break_plot_nodes(sdi, atlas):
    ns = genfromtxt(sdi)
    sys.modules['matplotlib'] = None
    with raises(ImportError) as errorinfo:
        viz.plot_nodes(ns, atlas)
    assert 'is required' in str(errorinfo.value)
    sys.modules['matplotlib'] = matplotlib

    sys.modules['nilearn'] = None
    with raises(ImportError) as errorinfo:
        viz.plot_nodes(ns, atlas)
    assert 'is required' in str(errorinfo.value)
    sys.modules['nilearn'] = nilearn

    sys.modules['nibabel'] = None
    with raises(ImportError) as errorinfo:
        viz.plot_nodes(ns, atlas)
    assert 'is required' in str(errorinfo.value)
    sys.modules['nibabel'] = nibabel

    with raises(ValueError) as errorinfo:
        viz.plot_nodes(rand(3, 3, 4), atlas)
    assert 'plot node values' in str(errorinfo.value)

    with raises(NotImplementedError) as errorinfo:
        viz.plot_nodes(rand(3), rand(3, 3, 2))
    assert 'atlases in nifti' in str(errorinfo.value)
    with raises(NotImplementedError) as errorinfo:
        viz.plot_nodes(rand(3), rand(3, 4))
    assert 'atlases in nifti' in str(errorinfo.value)

    with raises(ImageFileError) as errorinfo:
        viz.plot_nodes(rand(3), './notanatlas.nii.gz')
    assert 'file ./notanatlas.nii.gz' in str(errorinfo.value)

    with raises(ValueError) as errorinfo:
        viz.plot_nodes(rand(3), atlas)
    assert 'different length' in str(errorinfo.value)
