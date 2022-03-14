#!/usr/bin/env python3
"""Integration test."""
from os.path import isfile, isdir, join

import numpy as np

from pytest import mark, raises

from nigsp.workflow import nigsp, _main


# ### Integration tests
def test_integration():
    # Set raw data
    timeseries = '/home/nemo/Scrivania/Test_workbench/nigsp/RS_10subj.mat'
    sc_mtx = '/home/nemo/Scrivania/Test_workbench/nigsp/SC_avg56.mat'

    # Import matlab results
    mean_fc = np.genfromtxt('/home/nemo/Scrivania/Test_workbench/nigsp/mFC_matlab.tsv')
    sdi = np.genfromtxt('/home/nemo/Scrivania/Test_workbench/nigsp/SDI_matlab.tsv')

    # Run workflow
    nigsp(timeseries, sc_mtx, outname='testfile.tsv', outdir='testdir',
          surr_type='informed', n_surr=19, seed=42)

    # Check that files were created
    assert isdir('testdir')
    assert isdir(join('testdir', 'fc'))
    assert isdir(join('testdir', 'fc_high'))
    assert isdir(join('testdir', 'fc_low'))
    assert isdir(join('testdir', 'logs'))
    assert isdir(join('testdir', 'timeseries_high'))
    assert isdir(join('testdir', 'timeseries_low'))
    assert isfile(join('testdir', 'fc', '000.csv'))
    assert isfile(join('testdir', 'fc_high', '000.csv'))
    assert isfile(join('testdir', 'fc_low', '000.csv'))
    assert isfile(join('testdir', 'timeseries_high', '000.csv'))
    assert isfile(join('testdir', 'timeseries_low', '000.csv'))
    assert isfile(join('testdir', 'sc.png'))
    assert isfile(join('testdir', 'sdi.png'))
    assert isfile(join('testdir', 'fc.png'))
    assert isfile(join('testdir', 'grayplot.png'))
    assert isfile(join('testdir', 'fc_high.png'))
    assert isfile(join('testdir', 'grayplot_high.png'))

    sdi_int = np.genfromtxt(join('testdir', 'sdi.csv'))

    fc = np.empty((sdi.shape[0], sdi.shape[0], 10))
    for i in range(10):
        fc[..., i] = np.genfromtxt(join('testdir', 'fc', f'{i:03d}.csv'))

    mean_fc_int = fc.mean(axis=-1)
    # Check that results are comparable to matlab results

    assert (mean_fc_int - mean_fc).sum() < 0.000001
    assert (sdi_int - sdi).sum() < 0.000001

# ### Workflow break tests
