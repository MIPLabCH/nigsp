#!/usr/bin/env python3
"""Tests for blocks."""
import shutil
import sys
from os import makedirs, remove
from os.path import isfile, join

import nibabel
import numpy as np
from nilearn.plotting import find_parcellation_cut_coords
from pymatreader import read_mat
from pytest import mark

from nigsp import blocks
from nigsp.io import load_nifti_get_mask
from nigsp.objects import SCGraph


# ### Unit tests
def test_nifti_to_timeseries(atlastime, atlas):

    img_in = nibabel.load(atlas)
    atlas_in = img_in.get_fdata()
    ts_out, atlas_out, img_out = blocks.nifti_to_timeseries(atlastime, atlas)
    ts_in = np.unique(atlas_in)[1:, np.newaxis]
    ts_in = np.repeat(ts_in, 2, axis=-1)

    assert (ts_in == ts_out).all()
    assert (atlas_in == atlas_out).all()
    assert (img_in.header["dim"] == img_out.header["dim"]).all()

    remove(atlastime)
    remove(atlas)


@mark.parametrize("ext", [(".nii.gz"), (".csv")])
def test_export_metrics_txt(ext, sc_mtx, atlas, sdi, testdir):

    testdir = join(testdir, "testdir")
    makedirs(testdir, exist_ok=True)
    atlas_in, mask, img = load_nifti_get_mask(atlas, ndim=3)
    mtx = read_mat(sc_mtx)
    mtx = mtx["SC_avg56"]
    sdi_in = np.genfromtxt(sdi)
    ts = np.unique(atlas_in)[1:]
    ts = np.repeat(ts[..., np.newaxis], 2, axis=-1)
    gsdi = dict.fromkeys(["hilo", "himid"], sdi_in)
    scgraph = SCGraph(mtx, ts, atlas=atlas_in, img=img, sdi=sdi_in)
    blocks.export_metric(scgraph, ext, join(testdir, "molly_"))
    scgraph = SCGraph(mtx, ts, atlas=atlas_in, img=img, gsdi=gsdi)
    blocks.export_metric(scgraph, ext, join(testdir, "cesar_"))

    assert isfile(join(testdir, f"molly_sdi{ext}"))
    assert isfile(join(testdir, f"cesar_gsdi_hilo{ext}"))
    assert isfile(join(testdir, f"cesar_gsdi_himid{ext}"))

    shutil.rmtree(testdir)
    remove(sc_mtx)
    remove(atlas)
    remove(sdi)


def test_export_metrics_nifti(sc_mtx, atlas, sdi, testdir):

    testdir = join(testdir, "testdir")
    makedirs(testdir, exist_ok=True)
    atlas_in, mask, img = load_nifti_get_mask(atlas, ndim=3)
    mtx = read_mat(sc_mtx)
    mtx = mtx["SC_avg56"]
    sdi_in = np.genfromtxt(sdi)
    ts = np.unique(atlas_in)[1:]
    ts = np.repeat(ts[..., np.newaxis], 2, axis=-1)
    scgraph = SCGraph(mtx, ts, atlas=atlas_in, sdi=sdi_in)
    blocks.export_metric(scgraph, ".nii.gz", join(testdir, "molly_"))

    assert isfile(join(testdir, "molly_sdi.csv"))

    sys.modules["nibabel"] = None
    scgraph = SCGraph(mtx, ts, atlas=atlas_in, img=img, sdi=sdi_in)
    blocks.export_metric(scgraph, ".nii.gz", join(testdir, "molly_"))
    sys.modules["nibabel"] = nibabel

    assert isfile(join(testdir, "molly_sdi.csv"))
    shutil.rmtree(testdir)
    remove(sc_mtx)
    remove(atlas)
    remove(sdi)


def test_plot_metrics(atlas, sc_mtx, sdi, testdir):

    testdir = join(testdir, "testdir")
    makedirs(testdir, exist_ok=True)
    atlas_in, _, img = load_nifti_get_mask(atlas, ndim=3)
    mtx = read_mat(sc_mtx)
    mtx = mtx["SC_avg56"]
    sdi_in = np.genfromtxt(sdi)
    ts = np.unique(atlas_in)[1:]
    ts = np.repeat(ts[..., np.newaxis], 2, axis=-1)
    gsdi = dict.fromkeys(["hilo", "himid"], sdi_in)

    scgraph = SCGraph(mtx, ts, sdi=sdi_in, img=img)
    blocks.plot_metric(scgraph, join(testdir, "maite_"), atlas=img)
    assert isfile(join(testdir, join(testdir, "maite_sdi.png")))

    atlas_in = find_parcellation_cut_coords(img)
    scgraph = SCGraph(mtx, ts, sdi=sdi_in, img=img)
    blocks.plot_metric(scgraph, join(testdir, "maite_"), atlas=atlas_in)
    assert isfile(join(testdir, join(testdir, "maite_sdi.png")))

    scgraph = SCGraph(mtx, ts, gsdi=gsdi, img=img)
    blocks.plot_metric(scgraph, join(testdir, "dimitri_"), atlas=img)
    assert isfile(join(testdir, join(testdir, "dimitri_gsdi_hilo.png")))

    shutil.rmtree(testdir)
    remove(sc_mtx)
    remove(atlas)
    remove(sdi)
