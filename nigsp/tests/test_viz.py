#!/usr/bin/env python3
"""Tests for viz."""

import sys
from os import remove
from os.path import isfile

import matplotlib
import pytest
from numpy import genfromtxt
from numpy.random import rand

from nigsp import viz


@pytest.mark.parametrize(
    "mtx", [(rand(3, 4)), (rand(4, 4)), (rand(4, 4, 3)), (rand(4, 4, 3, 1))]
)
# ### Unit tests
def test_plot_connectivity(mtx):
    pytest.importorskip("nilearn")

    viz.plot_connectivity(mtx, "annie.png", closeplot=True)

    assert isfile("annie.png")
    matplotlib.pyplot.close()
    remove("annie.png")


@pytest.mark.parametrize(
    "timeseries", [(rand(3, 50)), (rand(3, 50, 3)), (rand(3, 50, 4, 1))]
)
def test_plot_greyplot(timeseries):
    viz.plot_greyplot(timeseries, "troy.png", closeplot=True)

    assert isfile("troy.png")
    matplotlib.pyplot.close()
    remove("troy.png")


def test_plot_nodes(sdi, atlas):
    pytest.importorskip("nilearn")

    ns = genfromtxt(sdi)
    viz.plot_nodes(ns, atlas, "abed.png", closeplot=True)

    assert isfile("abed.png")
    matplotlib.pyplot.close()
    remove("abed.png")
    remove(sdi)
    remove(atlas)


def test_plot_edges(atlas):
    pytest.importorskip("nilearn")

    mtx = rand(360, 360)
    mtx = mtx - mtx.min() + 0.3
    with pytest.warns(UserWarning, match="'adjacency_matrix' is not symmetric"):
        viz.plot_edges(mtx, atlas, "britta.png", thr="95%", closeplot=True)

    assert isfile("britta.png")
    matplotlib.pyplot.close()
    remove("britta.png")
    remove(atlas)


# ### Break tests
def test_break_plot_connectivity():
    pytest.importorskip("nilearn")

    import nilearn.plotting

    sys.modules["matplotlib"] = None
    with pytest.raises(ImportError) as errorinfo:
        viz.plot_connectivity(rand(3, 3), "craig.png")
    assert "are required" in str(errorinfo.value)
    sys.modules["matplotlib"] = matplotlib

    sys.modules["nilearn.plotting"] = None
    with pytest.raises(ImportError) as errorinfo:
        viz.plot_connectivity(rand(3, 3), "craig.png")
    assert "are required" in str(errorinfo.value)
    sys.modules["nilearn.plotting"] = nilearn.plotting

    with pytest.raises(ValueError) as errorinfo:
        viz.plot_connectivity(rand(3, 3, 3, 4), "craig.png")
    assert "plot connectivity" in str(errorinfo.value)

    matplotlib.pyplot.close()


def test_break_plot_greyplot():
    sys.modules["matplotlib"] = None
    with pytest.raises(ImportError) as errorinfo:
        viz.plot_greyplot(rand(3, 3), "dan.png")
    assert "is required" in str(errorinfo.value)
    sys.modules["matplotlib"] = matplotlib

    with pytest.raises(ValueError) as errorinfo:
        viz.plot_greyplot(rand(3, 3, 3, 4), "dan.png")
    assert "plot greyplots" in str(errorinfo.value)

    matplotlib.pyplot.close()


def test_break_plot_nodes(atlas):
    pytest.importorskip("nilearn")

    import nilearn.plotting

    sys.modules["matplotlib"] = None
    with pytest.raises(ImportError) as errorinfo:
        viz.plot_nodes(rand(3), rand(3, 3))
    assert "are required" in str(errorinfo.value)
    sys.modules["matplotlib"] = matplotlib

    sys.modules["nilearn.plotting"] = None
    with pytest.raises(ImportError) as errorinfo:
        viz.plot_nodes(rand(3), rand(3, 3))
    assert "are required" in str(errorinfo.value)
    sys.modules["nilearn.plotting"] = nilearn.plotting

    with pytest.raises(ValueError) as errorinfo:
        viz.plot_nodes(rand(3, 3, 4), rand(3, 3))
    assert "plot node values" in str(errorinfo.value)

    with pytest.raises(NotImplementedError) as errorinfo:
        viz.plot_nodes(rand(3), rand(3, 3, 2))
    assert "atlases in nifti" in str(errorinfo.value)
    with pytest.raises(NotImplementedError) as errorinfo:
        viz.plot_nodes(rand(3), rand(3, 4))
    assert "atlases in nifti" in str(errorinfo.value)

    with pytest.raises(ValueError) as errorinfo:
        viz.plot_nodes(rand(3), rand(4, 3))
    assert "different length" in str(errorinfo.value)

    matplotlib.pyplot.close()
    remove(atlas)


def test_break_plot_edges(atlas):
    pytest.importorskip("nilearn")

    import nilearn.plotting

    sys.modules["matplotlib"] = None
    with pytest.raises(ImportError) as errorinfo:
        viz.plot_edges(rand(3), rand(3, 3))
    assert "are required" in str(errorinfo.value)
    sys.modules["matplotlib"] = matplotlib

    sys.modules["nilearn.plotting"] = None
    with pytest.raises(ImportError) as errorinfo:
        viz.plot_edges(rand(3), rand(3, 3))
    assert "are required" in str(errorinfo.value)
    sys.modules["nilearn.plotting"] = nilearn.plotting

    with pytest.raises(ValueError) as errorinfo:
        viz.plot_edges(rand(3, 3, 4, 5), rand(3, 3))
    assert "plot node values" in str(errorinfo.value)

    with pytest.raises(NotImplementedError) as errorinfo:
        viz.plot_edges(rand(3), rand(3, 3, 2))
    assert "atlases in nifti" in str(errorinfo.value)
    with pytest.raises(NotImplementedError) as errorinfo:
        viz.plot_edges(rand(3), rand(3, 4))
    assert "atlases in nifti" in str(errorinfo.value)

    with pytest.raises(ValueError) as errorinfo:
        viz.plot_edges(rand(3), rand(4, 3))
    assert "different length" in str(errorinfo.value)

    matplotlib.pyplot.close()
    remove(atlas)


# ..and a movie!!!
