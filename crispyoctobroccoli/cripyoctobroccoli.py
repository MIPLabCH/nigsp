#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import sys

import numpy as np


from crispyoctobroccoli import blocks, io, utils, viz, _version
from crispyoctobroccoli import timeseries as ts
from crispyoctobroccoli.cli.run import _get_parser, _check_opt_conf
# from crispyoctobroccoli.due import due, Doi
from crispyoctobroccoli.objects import SCGraph


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


def crispyoctobroccoli(fname, scname, atlasname=None, outname=None, outdir=None,
                       index='median', surr_type=None, n_surr=1000, method='Bernoulli',
                       seed=None, lgr_degree='info'):
    """
    Main workflow for crispyoctobroccoli, following the methods described in [1]

    Parameters
    ----------
    fname : str or os.PathLike
        Path to the timeseries data file. It can be a text, nifti, or matlab file.
        (and variants). To see the full list of support, check general documentation.
    scname : str or os.PathLike
        Description
    atlasname : None, optional
        Description
    outname : None, optional
        Description
    outdir : None, optional
        Description
    index : str, optional
        Description
    surr_type : None, optional
        Description
    n_surr : int, optional
        Description
    method : None, optional
        Description
    seed : None, optional
        Description
    lgr_degree : str, optional
        Description

    Returns
    -------
    TYPE
        Description

    Raises
    ------
    NotImplementedError
        Description
    ValueError
        Description
    """
    # #### Logger preparation #### #
    fname = utils.if_declared_force_type(fname, list, stop=False, silent=True)

    # Prepare folders
    if outdir is None:
        if outname is None:
            common_path = os.path.commonpath(fname)
        else:
            outdir = os.path.split(outname)[0]
        if common_path == '' or common_path == '/':
            common_path = '.'
        outdir = os.path.join(common_path, 'crispyoctobroccoli')

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

    version_number = _version.get_versions()['version']
    LGR.info(f'Currently running crispyoctobroccoli version {version_number}')

    # #### Check input #### #
    LGR.info(f'Input structural connectivity file: {scname}')
    sc_is = dict.fromkeys(io.EXT_DICT.keys(), False)
    LGR.info(f'Input functional file(s): {fname}')
    func_is = dict.fromkeys(io.EXT_DICT.keys(), [])
    atlas_is = dict.fromkeys(io.EXT_DICT.keys(), False)
    if atlasname:
        LGR.info(f'Input atlas file: {atlasname}')
    # Check inputs type
    for k in io.EXT_DICT.keys():
        for f in fname:
            func_is[k] += [io.check_ext(io.EXT_DICT[k], f)]
        # Check that func files are all of the same kind
        func_is[k] = all(func_is[k])

        sc_is[k] = io.check_ext(io.EXT_DICT[k], scname)
        if atlasname:
            atlas_is[k] = io.check_ext(io.EXT_DICT[k], atlasname)

    # #### Read in data #### #

    # Read in structural connectivity matrix
    if (sc_is['1D'] and sc_is['mat'] and sc_is['xls']) is False:
        raise NotImplementedError(f'Input file {scname} is not of a supported type.')
    elif sc_is['1D']:
        mtx = io.load_txt(scname, shape='square')
    elif sc_is['mat']:
        mtx = io.load_mat(scname, shape='square')
    elif sc_is['xls']:
        mtx = io.load_xls(scname, shape='square')

    # Read in functional timeseries, join them, and normalise them
    timeseries = []
    for f in fname:
        if func_is['nifti'] and atlas_is['nifti']:
            t, atlas, atlasimg = blocks.nifti_to_timeseries(f, atlasname)
        elif func_is['nifti'] and atlas_is['nifti'] is False:
            raise NotImplementedError('To work with functional file(s) of nifti format, '
                                      'specify an atlas file in nifti format.')
        elif func_is['1D']:
            t = io.load_txt(fname, shape='rectangle')
        elif func_is['mat']:
            t = io.load_mat(fname, shape='rectangle')
        elif func_is['xls']:
            t = io.load_xls(fname, shape='rectangle')
        else:
            raise ValueError('Functional files were not found, or are not of same type')

        timeseries += [t[..., np.newaxis]]

    timeseries = np.concatenate(timeseries, axis=-1)
    timeseries = ts.normalise_ts(timeseries)

    # Read in atlas, if defined
    if atlasname is not None:
        if (atlas_is['1D'] and atlas_is['mat']
                and atlas_is['xls'] and atlas_is['nifti']) is False:
            raise NotImplementedError(f'Input file {atlasname} is not of a '
                                      'supported type.')
        elif atlas_is['1D']:
            atlas = io.load_txt(atlasname, shape='square')
        elif atlas_is['mat']:
            atlas = io.load_mat(atlasname, shape='square')
        elif atlas_is['xls']:
            atlas = io.load_xls(atlasname, shape='square')
    else:
        LGR.warning('Atlas not provided. Some functionalities might not work.')

    # #### Prepare SCGraph object #### #
    scgraph_init = {'mtx': mtx, 'timeseries': timeseries}

    if atlasname is not None:
        scgraph_init['atlas'] = atlas
        if atlas_is['nifti']:
            scgraph_init['img'] = atlasimg

    scgraph = SCGraph(**scgraph_init)
    # #### Compute SDI (split low vs high timeseries) and FC #### #

    # Run laplacian decomposition and actually filter timeseries.
    scgraph = scgraph.structural_decomposition(scgraph)
    scgraph = scgraph.compute_graph_energy(mean=True).split_graph(index)

    # If there are more than two splits in the timeseries, compute Generalised SDI
    # This should not happen in this moment.
    if len(scgraph.split_keys) == 2:
        scgraph = scgraph.compute_sdi()
    elif len(scgraph.split_keys) > 2:
        scgraph = scgraph.compute_gsdi()
    else:
        raise ValueError('Data is not splitted enough to compute SDI or similar '
                         'indexes.')

    scgraph = scgraph.compute_fc(mean=True)

    # #### Output results (pt. 1) #### #

    # Prepare outputs
    if outname is not None:
        _, outprefix, outext = io.check_ext(io.EXT_ALL, fname, remove=True)
        outprefix = os.path.join(outdir, f'{os.path.split(outprefix)[1]}_')
    else:
        outprefix = f'{outdir}{os.sep}'
        outext = ''

    # Export non-thresholded metrics
    blocks.export_metric(scgraph, outext, outprefix)

    # Export eigenvalues, eigenvectors, and split timeseries and eigenvectors
    for k in scgraph.split_keys:
        io.export_mtx(scgraph.ts_split[k], f'{outprefix}timeseries_{k}{outext}')
        io.export_mtx(scgraph.eigenvec_split[k], f'{outprefix}eigenvec_{k}{outext}')
    io.export_mtx(scgraph.eigenvec[k], f'{outprefix}eigenvec{outext}')
    io.export_mtx(scgraph.eigenval[k], f'{outprefix}eigenval{outext}')

    # #### Additional steps #### #

    # If required, create surrogates, test, and export masked metrics
    if surr_type is not None:
        if scgraph.sdi is not None:
            metric_name = 'sdi'
        elif scgraph.gsdi is not None:
            metric_name = 'gsdi'
        scgraph = scgraph.create_surrogates(sc_type=surr_type, n_surr=n_surr, seed=seed)
        scgraph = scgraph.test_significance(metric=metric_name, method=method, p=p, return_masked=True)
        # Export thresholded metrics
        blocks.export_metric(scgraph, outext, outprefix)

    # If possible, create plots!
    try:
        import nilearn as _
        import matplotlib as _

        # Plot original SC and Laplacian
        viz.plot_connectivity(scgraph.lapl_mtx, f'{outprefix}laplacian.png')
        viz.plot_connectivity(scgraph.mtx, f'{outprefix}sc.png')
        # Compute and plot FC
        scgraph = scgraph.compute_fc(mean=True)
        viz.plot_connectivity(scgraph.fc, f'{outprefix}fc.png')
        for k in scgraph.split_keys:
            viz.plot_connectivity(scgraph.fc_split[k],
                                  f'{outprefix}fc_{k}{outext}')
        # Plot timeseries
        viz.plot_grayplot(scgraph.timeseries, f'{outprefix}grayplot.png')
        for k in scgraph.split_keys:
            viz.plot_grayplot(scgraph.ts_split[k],
                              f'{outprefix}grayplot_{k}{outext}')

    except ImportError:
        LGR.warning('The necessary libraries for graphics (nilearn, matplotlib) '
                    'were not found. Skipping graphics.')

    LGR.info('End of workflow, find results in {outdir}.')

    return 0


def _main(argv=None):
    options = _get_parser().parse_args(argv)

    options = _check_opt_conf(options)

    save_bash_call(options.fname_func, options.outdir)

    crispyoctobroccoli(**vars(options))


if __name__ == '__main__':
    _main(sys.argv[1:])


"""
Copyright 2022, Stefano Moia.

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
