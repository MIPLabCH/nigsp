#!/usr/bin/env python3
"""Integration test."""
import shutil
from os.path import isdir, isfile, join

import numpy as np

from nigsp.workflow import _main


# ### Integration tests
def test_integration(timeseries, sc_mtx, atlas, mean_fc, sdi, testdir):
    """Integration test for FULL workflow."""
    testdir = join(testdir, "testdir")
    mean_fc_mat = np.genfromtxt(mean_fc)
    # Compared to original SDI, now we log2 it).
    sdi_mat = np.log2(np.genfromtxt(sdi))

    # Run workflow
    # fmt: off
    _main(
        [
            "-f", timeseries,
            "-s", sc_mtx,
            "-a", atlas,
            "-odir", testdir,
            "-ofile", "testfile.tsv",
            "-sci",
            "-n", "4",
            "-seed", "42",
        ]
    )
    # fmt: on
    # Check that files were created
    assert isdir(testdir)
    assert isdir(join(testdir, "logs"))
    assert isdir(join(testdir, "testfile_timeseries_low"))
    assert isdir(join(testdir, "testfile_timeseries_high"))
    assert isfile(join(testdir, "testfile_timeseries_low", "000.tsv"))
    assert isfile(join(testdir, "testfile_timeseries_high", "000.tsv"))
    assert isfile(join(testdir, "testfile_fc.tsv"))
    assert isfile(join(testdir, "testfile_fc_low.tsv"))
    assert isfile(join(testdir, "testfile_fc_high.tsv"))
    assert isfile(join(testdir, "testfile_eigenval.tsv"))
    assert isfile(join(testdir, "testfile_eigenvec.tsv"))
    assert isfile(join(testdir, "testfile_eigenvec_low.tsv"))
    assert isfile(join(testdir, "testfile_eigenvec_high.tsv"))
    assert isfile(join(testdir, "testfile_sdi.tsv"))
    assert isfile(join(testdir, "testfile_mkd_sdi.tsv"))
    assert isfile(join(testdir, "testfile_laplacian.png"))
    assert isfile(join(testdir, "testfile_sc.png"))
    assert isfile(join(testdir, "testfile_fc.png"))
    assert isfile(join(testdir, "testfile_fc_low.png"))
    assert isfile(join(testdir, "testfile_fc_high.png"))
    assert isfile(join(testdir, "testfile_greyplot.png"))
    assert isfile(join(testdir, "testfile_greyplot_low.png"))
    assert isfile(join(testdir, "testfile_greyplot_high.png"))
    assert isfile(join(testdir, "testfile_sdi.png"))
    assert isfile(join(testdir, "testfile_mkd_sdi.png"))

    sdi_pyt = np.genfromtxt(join(testdir, "testfile_sdi.tsv"))
    sdi_mkd = np.genfromtxt(join(testdir, "testfile_mkd_sdi.tsv"))

    mean_fc_pyt = np.genfromtxt(join(testdir, "testfile_fc.tsv"))
    # Check that each cell in the result is comparable to matlab's.
    # There's a bunch of rounding due to np.round and numerical difference between matlab and python
    assert abs(mean_fc_pyt.round(6) - mean_fc_mat.round(6)).max().round(6) <= 0.000001
    assert abs(sdi_pyt.round(5) - sdi_mat.round(5)).max().round(5) <= 0.00001
    assert (sdi_pyt != sdi_mkd).any()

    # Clean up!
    shutil.rmtree(testdir)
