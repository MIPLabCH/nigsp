#!/usr/bin/env python3
"""Tests for io."""

import sys
from os import remove
from os.path import isfile

import nibabel
import pymatreader
import scipy
from numpy import asarray, empty, genfromtxt, savetxt
from numpy.random import rand
from pytest import mark, raises

from nigsp import io

# ### Unit tests


def test_check_ext():
    """Text check_ext."""
    all_ext = io.EXT_1D + io.EXT_MAT + io.EXT_NIFTI
    for ext_in in all_ext:
        fname_in = f"shiny{ext_in}"

        for fname in [fname_in, fname_in.upper()]:
            has_ext, fname_out = io.check_ext(all_ext, fname)

            assert has_ext is True
            assert fname_out == fname

            has_ext, fname_out, ext_out = io.check_ext(all_ext, fname, remove=True)

            assert has_ext is True
            assert fname_out == fname[: -len(ext_in)]
            assert ext_out == ext_in

    # #!# Missing scan option

    fname_in = "shiny.mal"
    for fname in [fname_in, fname_in.upper()]:
        has_ext, fname_out = io.check_ext(".inara", fname)

        assert has_ext is False
        assert fname_out == fname

        has_ext, fname_out, ext_out = io.check_ext(".inara", fname, remove=True)

        assert has_ext is False
        assert fname_out == fname
        assert ext_out == ""


@mark.parametrize("data", [(rand(3, 4)), (rand(3, 4, 1)), (rand(3, 1, 4))])
def test_check_nifti_dim(data):
    """Test check_nifti_dim."""
    data_out = io.check_nifti_dim("kaylee", data, dim=2)

    assert (data_out == data.squeeze()).all()
    assert data_out.ndim == 2


@mark.parametrize("data", [(rand(3, 4)), (rand(3, 4, 1)), (rand(3, 1, 4))])
def test_check_mtx_dim(data):
    """Test check_mtx_dim."""
    data_out = io.check_mtx_dim("wash", data)

    assert (data_out == data.squeeze()).all()
    assert data_out.ndim == 2


@mark.parametrize("data, shape", [(rand(3), "rectangle"), (rand(3, 3), "square")])
def test_check_mtx_dim_cases(data, shape):
    """Test check_mtx_dim for specific shapes."""
    data_out = io.check_mtx_dim("wash", data, shape=shape)

    assert (data_out.squeeze() == data).all()
    assert data_out.ndim == 2


def test_load_nifti_get_mask(atlas):
    """Test load_nifti_get_mask."""
    img = nibabel.load(atlas)
    data = img.get_fdata()
    mask = data.any(axis=-1).squeeze()

    d, m, i = io.load_nifti_get_mask(atlas, ndim=3)

    assert (data == d).all()
    assert (mask == m).all()
    assert (img.header["dim"] == i.header["dim"]).all()

    remove(atlas)


def test_load_txt():
    """Test load_txt."""
    a = rand(5)
    n = "zoe"
    savetxt(n, a)
    b = io.load_txt(n)

    assert (a == b).all()

    remove(n)


def test_load_mat():
    """Test load_mat."""
    a = rand(5)
    b = "likealeaf"
    n = "inthewind"

    scipy.io.savemat(n, {"data": a, "other": b})

    c = io.load_mat(n)

    assert (a == c).all()
    remove(n)


def test_export_nifti(atlas):
    """Test export_nifti."""
    img = nibabel.load(atlas)
    shape = img.get_fdata().shape
    io.export_nifti(empty(shape), img, "book")
    assert isfile("book.nii.gz")
    remove("book.nii.gz")
    remove(atlas)


@mark.parametrize(
    "ext_in, ext_out",
    [
        (".1D", ".1D"),
        (".csv", ".csv"),
        (".tsv", ".tsv"),
        ("", ".csv"),
        (".mat", ".mat"),
    ],
)
def test_export_mtx(ext_in, ext_out):
    """Test export_mtx."""
    data = asarray([[1, 1, 2], [3, 5, 8]])
    io.export_mtx(data, "serenity", ext=ext_in)
    assert isfile(f"serenity{ext_out}")

    if ext_out in [".csv"]:
        data_in = genfromtxt(f"serenity{ext_out}", delimiter=",")
    if ext_out in [".tsv", ".1D"]:
        data_in = genfromtxt(f"serenity{ext_out}")

    if ext_out in [".mat"]:
        data_in = pymatreader.read_mat(f"serenity{ext_out}")
        data_in = data_in["data"]

    assert (data_in == data).all()
    # remove data
    remove(f"serenity{ext_out}")


# ### Break tests
@mark.parametrize("data", [(rand(3)), (rand(3, 4, 2))])
def test_break_check_nifti_dim(data):
    """Break check_nifti_dim."""
    with raises(ValueError) as errorinfo:
        io.check_nifti_dim("jayne", data, dim=2)
    assert f"jayne is {data.ndim}D" in str(errorinfo.value)


def test_break_check_mtx_dim():
    """Break check_mtx_dim."""
    with raises(ValueError) as errorinfo:
        io.check_mtx_dim("river", empty(0))
    assert "river is empty" in str(errorinfo.value)

    with raises(NotImplementedError) as errorinfo:
        io.check_mtx_dim("river", rand(3, 4, 5, 6))
    assert "3D are supported" in str(errorinfo.value)

    with raises(ValueError) as errorinfo:
        io.check_mtx_dim("river", rand(3, 4), shape="square")
    assert "river matrix has shape (3, 4)" in str(errorinfo.value)


def test_break_load_nifti_get_mask():
    """Break load_nifti_get_mask."""
    sys.modules["nibabel"] = None
    with raises(ImportError) as errorinfo:
        io.load_nifti_get_mask("reavers")
    assert "is required" in str(errorinfo.value)
    sys.modules["nibabel"] = nibabel


def test_break_load_mat():
    """Break load_mat."""
    sys.modules["pymatreader"] = None
    with raises(ImportError) as errorinfo:
        io.load_mat("simon")
    assert "is required" in str(errorinfo.value)
    sys.modules["pymatreader"] = pymatreader

    a = "heart"
    n = "ofgold"
    scipy.io.savemat(n, {"data": a})

    with raises(EOFError) as errorinfo:
        io.load_mat(n)
    assert f"{n} does not seem" in str(errorinfo.value)
    remove(n)


def test_break_load_xls():
    """Break load_xls."""
    with raises(NotImplementedError) as errorinfo:
        io.load_xls("firefly")
    assert "loading is not" in str(errorinfo.value)


def test_break_export_nifti():
    """Break export_nifti."""
    sys.modules["nibabel"] = None
    with raises(ImportError) as errorinfo:
        io.export_nifti(rand(3), None, "reavers")
    assert "is required" in str(errorinfo.value)
    sys.modules["nibabel"] = nibabel


def test_break_export_mtx():
    """Break export_mtx."""
    with raises(NotImplementedError) as errorinfo:
        io.export_mtx(rand(3, 4), "lostinthewoods", ext=".xls")
    assert "output is not" in str(errorinfo.value)

    sys.modules["scipy"] = None
    with raises(ImportError) as errorinfo:
        io.export_mtx(rand(3, 4), "lostinthewoods", ext=".mat")
    assert "is required" in str(errorinfo.value)
    sys.modules["scipy"] = scipy
