#!/usr/bin/env python3
"""Integration test."""
from os.path import isfile, isdir

import numpy as np

from pytest import mark, raises

from nigsp import nigsp


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
    assert isfile('testdir/')
    assert isfile('testdir/')
    assert isfile('testdir/')
    assert isfile('testdir/')
    assert isfile('testdir/')
    assert isfile('testdir/')

    # Check that results are comparable to matlab results

    assert (mean_fc_int - mean_fc).sum() < 0.000001
    assert (sdi_int - sdi).sum() < 0.000001

# ### Workflow break tests
