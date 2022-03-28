#!/usr/bin/env python3
"""Integration test."""
import shutil

from os.path import isfile, isdir, join

import numpy as np

from nigsp.workflow import _main


# ### Integration tests
def test_integration(timeseries, sc_mtx, atlas, mean_fc, sdi, testdir):
    """Integration test for FULL workflow."""
    testdir = join(testdir, 'testdir')
    mean_fc_mat = np.genfromtxt(mean_fc)
    sdi_mat = np.genfromtxt(sdi)

    # Run workflow
    _main(['-f', timeseries, '-s', sc_mtx, '-a', atlas, '-odir', testdir,
          '-ofile', 'testfile.tsv', '-sci', '-n', '4', '-seed', '42'])

    # Check that files were created
    assert isdir(testdir)
    assert isdir(join(testdir, 'testfile_fc'))
    assert isdir(join(testdir, 'testfile_fc_high'))
    assert isdir(join(testdir, 'testfile_fc_low'))
    assert isdir(join(testdir, 'logs'))
    assert isdir(join(testdir, 'testfile_timeseries_high'))
    assert isdir(join(testdir, 'testfile_timeseries_low'))
    assert isfile(join(testdir, 'testfile_fc', '000.tsv'))
    assert isfile(join(testdir, 'testfile_fc_high', '000.tsv'))
    assert isfile(join(testdir, 'testfile_fc_low', '000.tsv'))
    assert isfile(join(testdir, 'testfile_timeseries_high', '000.tsv'))
    assert isfile(join(testdir, 'testfile_timeseries_low', '000.tsv'))
    assert isfile(join(testdir, 'testfile_sc.png'))
    assert isfile(join(testdir, 'testfile_sdi.png'))
    assert isfile(join(testdir, 'testfile_fc.png'))
    assert isfile(join(testdir, 'testfile_grayplot.png'))
    assert isfile(join(testdir, 'testfile_fc_high.png'))
    assert isfile(join(testdir, 'testfile_grayplot_high.png'))
    assert isfile(join(testdir, 'testfile_sdi.tsv'))

    sdi_pyt = np.genfromtxt(join(testdir, 'testfile_sdi.tsv'))

    fc = np.empty((sdi_mat.shape[0], sdi_mat.shape[0], 10))
    for i in range(10):
        fc[..., i] = np.genfromtxt(join(testdir, 'testfile_fc', f'{i:03d}.tsv'))

    mean_fc_pyt = fc.mean(axis=-1)
    # Check that each cell in the result is comparable to matlab's.
    # There's a bunch of rounding due to np.round and numerical difference between matlab and python
    assert abs(mean_fc_pyt.round(6) - mean_fc_mat.round(6)).max().round(6) <= 0.000001
    assert abs(sdi_pyt.round(5) - sdi_mat.round(5)).max().round(5) <= 0.00001

    # Clean up!
    shutil.rmtree(testdir)