#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import sys
from copy import deepcopy
from shutil import copy as cp

import numpy as np

from crispyoctobroccoli import io, utils, viz, _version
from crispyoctobroccoli.cli.run import _get_parser, _check_opt_conf
from crispyoctobroccoli.due import due, Doi
from crispyoctobroccoli._version import get_versions

LGR = logging.getLogger(__name__)
LGR.setLevel(logging.INFO)


def save_bash_call(fname, outdir):
    """
    Save the bash call into file `p2d_call.sh`.

    Parameters
    ----------
    outdir : str or path, optional
        output directory
    """
    arg_str = ' '.join(sys.argv[1:])
    call_str = f'crispyoctobroccoli {arg_str}'
    outdir = os.path.abspath(outdir)
    log_path = os.path.join(outdir, 'logs')
    os.makedirs(log_path, exist_ok=True)
    isotime = datetime.datetime.now().strftime('%Y-%m-%dT%H%M%S')
    fname, _ = io.check_ext('.nii.gz', os.path.basename(fname), remove=True)
    f = open(os.path.join(log_path,
                          f'crispyoctobroccoli_call_{fname}_{isotime}.sh'), 'a')
    f.write(f'#!bin/bash \n{call_str}')
    f.close()


def crispyoctobroccoli(outdir='', lgr_degree='info'):

    ##### Logger preparation #####

    # Prepare folder
    if outdir:
        outdir = os.path.abspath(outdir)
    else:
        outdir = os.path.join(os.path.split(fname_func)[0], 'crispyoctobroccoli')
    outdir = os.path.abspath(outdir)
    log_path = os.path.join(outdir, 'logs')
    os.makedirs(log_path, exist_ok=True)

    # Create logfile name
    basename = 'crispyoctobroccoli_'
    extension = 'tsv'
    isotime = datetime.datetime.now().strftime('%Y-%m-%dT%H%M%S')
    logname = os.path.join(log_path, f'{basename}{isotime}.{extension}')

    # Set logging format
    log_formatter = logging.Formatter(
        '%(asctime)s\t%(name)-12s\t%(levelname)-8s\t%(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S')

    # Set up logging file and open it for writing
    log_handler = logging.FileHandler(logname)
    log_handler.setFormatter(log_formatter)
    sh = logging.StreamHandler()

    if lgr_degree == 'quiet':
        logging.basicConfig(level=logging.WARNING,
                            handlers=[log_handler, sh], format='%(levelname)-10s %(message)s')
    elif lgr_degree == 'debug':
        logging.basicConfig(level=logging.DEBUG,
                            handlers=[log_handler, sh], format='%(levelname)-10s %(message)s')
    else:
        logging.basicConfig(level=logging.INFO,
                            handlers=[log_handler, sh], format='%(levelname)-10s %(message)s')

    LGR.info(f'Currently running crispyoctobroccoli version {get_versions()['version']}')
    LGR.info(f'Input file is {fname_func}')


    ##### Check input #####

    # Check func type and read it
    func_is_1d = io.check_ext(EXT_1D, fname_func)
    func_is_nifti = io.check_ext(EXT_NIFTI, fname_func)

    # Check that all input values have right type
    tr = io.if_declared_force_type(tr, 'float', 'tr')
    freq = io.if_declared_force_type(freq, 'float', 'freq')
    trial_len = io.if_declared_force_type(trial_len, 'int', 'trial_len')
    n_trials = io.if_declared_force_type(n_trials, 'int', 'n_trials')
    highcut = io.if_declared_force_type(highcut, 'float', 'highcut')
    lowcut = io.if_declared_force_type(lowcut, 'float', 'lowcut')
    lag_max = io.if_declared_force_type(lag_max, 'float', 'lag_max')
    lag_step = io.if_declared_force_type(lag_step, 'float', 'lag_step')
    l_degree = io.if_declared_force_type(l_degree, 'int', 'l_degree')
    scale_factor = io.if_declared_force_type(scale_factor, 'float', 'scale_factor')




    return


def _main(argv=None):
    options = _get_parser().parse_args(argv)

    options = _check_opt_conf(options)

    save_bash_call(options.fname_func, options.outdir)

    crispyoctobroccoli(**vars(options))


if __name__ == '__main__':
    _main(sys.argv[1:])


"""
Copyright 2021, Stefano Moia.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
