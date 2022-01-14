# -*- coding: utf-8 -*-
"""
Parser for crispy-octo-broccoli.
"""

import argparse

from crispyoctobroccoli import __version__


def _get_parser():
    """
    Parses command line inputs for this function

    Returns
    -------
    parser.parse_args() : argparse dict

    """
    parser = argparse.ArgumentParser(description=('%(prog)s, a tool to compute '
                                                  'Cerebrovascular Reactivity '
                                                  'maps and their lags.\n'
                                                  '%(prog)s is compatible with '
                                                  'different designs and techniques '
                                                  'to estimate CVR maps.'
                                                  'It can also be used to generate '
                                                  'regressors to run the estimation '
                                                  'with other softwares.\n'
                                                  f'Version {__version__}'),
                                     add_help=False)
    required = parser.add_argument_group('Required Argument')
    required.add_argument('-i', '--input-func',
                          dest='fname_func',
                          type=str,
                          help=('Complete path (absolute or relative) and name '
                                'of the file containing fMRI signal. This file '
                                'can be a nifti file or a 1D txt file.'),
                          required=True)

    opt_out = parser.add_argument_group('Optional Argument for output')
    opt_out.add_argument('-o', '--output-directory',
                         dest='outdir',
                         type=str,
                         help=('Complete path (absolute or relative) and name '
                               'of the desired output directory. If it does not '
                               'exist, it will be created. If it is not '
                               'specified, a folder named "phys2cvr" will be '
                               'created in the folder containing the functional '
                               'file.'),
                         default='')

    opt_func = parser.add_argument_group('Optional Arguments for fMRI timeseries')
    opt_func.add_argument('-m', '--input-mask',
                          dest='fname_mask',
                          type=str,
                          help=('Complete path (absolute or relative) and name '
                                'of the file containing a brain mask (nifti file). '
                                'Only the voxels in this mask will be considered '
                                'by phys2cvr. Use this option to '
                                'specify a GM mask or overwrite a full brain mask.\n'
                                'If the functional file is specified and this '
                                'option is not used, or the mask cannot be '
                                'loaded, the program will create a mask using '
                                'any voxel of the functional file constantly '
                                'different from zero.'),
                          default='')
    opt_func.add_argument('-r', '--input-roi',
                          dest='fname_roi',
                          type=str,
                          help=('Complete path (absolute or relative) and name '
                                'of the nifti file containing a subset of voxels to '
                                'treat as a region of interest (ROI). '
                                'The average functional signal of the ROI will be used '
                                'to run the cross correlation with the '
                                'physiological regressor. The median lag value in '
                                'the ROI will be used to correct the final lag map.\n'
                                'If the functional file is specified and this '
                                'option is not used, or the ROI cannot be '
                                'loaded, the program will either use a specified mask '
                                '(see `--input-mask`) or create a mask using '
                                'any voxel of the functional file constantly '
                                'different from zero.'),
                          default='')
    opt_func.add_argument('-tr', '--repetition-time',
                          dest='tr',
                          type=float,
                          help=('TR of functional data. Required '
                                'if the latter is not passed as a nifti file. '
                                'Use this option to overwrite the frequency of a '
                                'nifti file.'),
                          default=None)

    opt_phys = parser.add_argument_group('Optional Arguments for physiological '
                                         'timeseries (regressor of interest)')
    opt_phys.add_argument('-co2', '--input-co2',
                          dest='fname_co2',
                          type=str,
                          help=('Complete path (absolute or relative) and name '
                                'of the file containing CO2 signal (or equivalent '
                                'physiological trace to compute the regressor). '
                                'This file can be a 1D txt file or a .phys file '
                                'from peakdet.\n If nothing is specified, the '
                                'average timeseries of the mask will be used '
                                'as regressor.'),
                          default='')
    opt_phys.add_argument('-pk', '--input-peaks',
                          dest='fname_pidx',
                          type=str,
                          help=('Complete path (absolute or relative) and name '
                                'of the file containing the peak of the '
                                'physiological trace. Required if the physiological '
                                'trace file is not a .phys file.\n'
                                'Use this option to overwrite the peaks specified '
                                'in the .phys file.'),
                          default='')
    opt_phys.add_argument('-fr', '--frequency',
                          dest='freq',
                          type=float,
                          help=('Frequency of the physiological trace. Required '
                                'if the latter is not passed as a .phys file.\n'
                                'Use this option to overwrite the frequency of a '
                                '.phys file.'),
                          default=None)

    opt_xcorr = parser.add_argument_group('Optional Arguments for the cross correlation '
                                          '(bulk shift estimation step)')
    opt_xcorr.add_argument('-tlen', '--trial-length',
                           dest='trial_len',
                           type=float,
                           help=('Total duration of a single trial of the task '
                                 'in seconds (useful for block designs).\n'
                                 'Specify this with the number of trials to run '
                                 'a double cross-correlation between functional '
                                 'signal and physiological regressor to improve '
                                 'the detection of the bulk shift.'),
                           default=None)
    opt_xcorr.add_argument('-ntrial', '--trial-number',
                           dest='n_trials',
                           type=int,
                           help=('Number of trials in the task (useful for block designs).\n'
                                 'Specify this with the duration of trials to run '
                                 'a double cross-correlation between functional '
                                 'signal and physiological regressor to improve '
                                 'the detection of the bulk shift.'),
                           default=None)

    opt_filt = parser.add_argument_group('Optional Arguments for temporal filter')
    opt_filt.add_argument('-af', '--apply-filter',
                          dest='apply_filter',
                          action='store_true',
                          help=('Apply a filter to the functional data before '
                                'estimating the bulk shift. The filter will not '
                                'be applied on the data before the GLM computation. '
                                'If you want that, consider applying it before '
                                'running %(prog)s (or running it a second time).'),
                          default=False)
    opt_filt.add_argument('-hf', '--highcut-frequency',
                          dest='highcut',
                          type=float,
                          help=('Higher frequency to use in signal filtering. '
                                'The filter will be applied only to the functional '
                                'data to estimate the bulk shift. This option '
                                'is suggested when only using a functional file.'),
                          default=None)
    opt_filt.add_argument('-lf', '--lowcut-frequency',
                          dest='lowcut',
                          type=float,
                          help=('Lower frequency to use in signal filtering. '
                                'The filter will be applied only to the functional '
                                'data to estimate the bulk shift. This option '
                                'is suggested when only using a functional file.'),
                          default=None)

    opt_flow = parser.add_argument_group('Optional Arguments to modify the workflow')
    opt_flow.add_argument('-skip_reg', '--skip-regression',
                          dest='run_regression',
                          action='store_false',
                          help=('Skip running physiological regression(s) '
                                'internally. This will make %(prog)s '
                                'generate the desired physiological regressors '
                                'and quit, assuming that the regression itself '
                                'will be carried out with other software '
                                '(e.g. AFNI, FSL, ...).'),
                          default=True)
    opt_flow.add_argument('-skip_lagreg', '--skip-lagged-regression',
                          dest='lagged_regression',
                          action='store_false',
                          help=('Skip estimating the lagged regressors, '
                                'estimating only the bulk shifted one.\n'
                                'Skip running the lagged regression if the '
                                'regression step is run.'),
                          default=True)
    opt_flow.add_argument('-skip_conv', '--skip-convolution',
                          dest='run_conv',
                          action='store_false',
                          help=('Skip convolution of physiological trace. '
                                'By default %(prog)s convolves the physiological '
                                'trace with a standard HRF. Skip it when using '
                                'fMRI signal only.'),
                          default=True)

    opt_regr = parser.add_argument_group('Optional Arguments for the regression step')
    opt_regr.add_argument('-ldeg', '--legendre-degree',
                          dest='l_degree',
                          type=int,
                          help=('Maximum legendre degree to add to the regression '
                                'matrix as nuisance. Default is 0, to account for '
                                'the degree of freedom lost in computing the SPC.'),
                          default=0)
    opt_regr.add_argument('-dmat', '--denoise-matrix',
                          dest='denoise_matrix',
                          nargs='*',
                          type=str,
                          help=('Complete path (absolute or relative) and filename '
                                'of denoising matrices to add to the regression model. '
                                'This option can be specified multiple times to '
                                'add multiple denoising matrices, but multiple '
                                'denoising matrices can be specified one after '
                                'the other, separated by a space.'),
                          default=None)
    opt_regr.add_argument('-scale', '--scale-factor',
                          dest='scale_factor',
                          type=float,
                          help=('Scale factor by which the beta maps will be divided '
                                'to create the CVR map output. Since BIDS '
                                'currently does not support mmHg as unit, if '
                                'using CO2 traces check their unit of measure '
                                'and their scaling factor to transform Volts into '
                                'mmHg. Use this option for other standardisations too.'),
                          default=None)

    opt_lreg = parser.add_argument_group('Optional Arguments for the lagged regression')
    opt_lreg.add_argument('-lm', '--lag-max',
                          dest='lag_max',
                          type=float,
                          help=('Maximum lag to consider during lag regression '
                                'in seconds. The same lag will be considered in '
                                'both directions.\n'
                                'Remember that being this python, the upper limit '
                                'is excluded from the computation, i.e. 9 is '
                                '[-9, +8.7] or [-9, +9).'),
                          default=None)
    opt_lreg.add_argument('-ls', '--lag-step',
                          dest='lag_step',
                          type=float,
                          help=('Lag step to consider during lagged regression '
                                'in seconds. Default is 0.3 seconds.'),
                          default=None)

    opt_regr = parser.add_argument_group('Optional Arguments to re-run a lagged '
                                         'regression (also useful to use a lag estimation '
                                         'on a different functional timeseries)')
    opt_regr.add_argument('-lmap', '--lag-map',
                          dest='lag_map',
                          type=str,
                          help=('Complete path (absolute or relative) and name '
                                'of a previously computed lag map to use in '
                                'lagged regression.'),
                          default=None)
    opt_regr.add_argument('-rdir', '--regr-dir',
                          dest='regr_dir',
                          type=str,
                          help=('Complete path (absolute or relative) and name '
                                'of previously computed lagged regressors to '
                                'use in a new lagged regression.'),
                          default=None)

    title_opt_conf = parser.add_argument_group('Optional Arguments to set up specific '
                                               'workflows')

    opt_conf = title_opt_conf.add_mutually_exclusive_group()
    opt_conf.add_argument('--brightspin',
                          dest='workflow_config',
                          action='store_const',
                          const='brightspin',
                          help=('Estimate CVR using a specific set of L-GLM parameters, '
                                'as used in:\n'
                                'S. Moia, et al., \'ICA-based denoising strategies in '
                                'breath-hold induced cerebrovascular reactivity mapping '
                                'with multi echo BOLD fMRI\' (2021), NeuroImage\n'
                                'Same as setting --lag-max 9 --lag-step 0.3'),
                          default=None)
    opt_conf.add_argument('--brightspin-clinical',
                          dest='workflow_config',
                          action='store_const',
                          const='brightspin-clinical',
                          help=('Like "brightspin", but use a larger lag range.\n'
                                'Same as setting --lag-max 20 --lag-step 0.3'),
                          default=None)
    opt_conf.add_argument('--baltimore',
                          dest='workflow_config',
                          action='store_const',
                          const='baltimore',
                          help=('Estimate CVR using the average timeseries in the '
                                '0.02-0.04 frequency spectrum, as used in:\n'
                                'P. Liu, et al., \'Cerebrovascular reactivity '
                                'mapping without gas challenges\' (2017), NeuroImage\n'
                                'Same as setting --apply-filter -hf -lf '
                                '-skip_conv -skip_lagreg -co2 \'\' '),
                          default=None)
    opt_conf.add_argument('--baltimore-lag',
                          dest='workflow_config',
                          action='store_const',
                          const='baltimore-lag',
                          help=('Like "baltimore", but use a L-GLM instead\n'
                                'Same as setting --apply-filter -hf -lf '
                                '-skip_conv -co2 \'\' '),
                          default=None)

    optional = parser.add_argument_group('Other Optional Arguments')
    optional.add_argument('-debug', '--debug',
                          dest='debug',
                          action='store_true',
                          help='Only print debugging info to log file. Default is False.',
                          default=False)
    optional.add_argument('-quiet', '--quiet',
                          dest='quiet',
                          action='store_true',
                          help='Only print warnings to log file. Default is False.',
                          default=False)
    optional.add_argument('-h', '--help', action='help',
                          help='Show this help message and exit')
    optional.add_argument('-v', '--version', action='version',
                          version=('%(prog)s ' + __version__))
    return parser


def _check_opt_conf(parser):
    """
    Check for particular configuration flags.
    
    Parameters
    ----------
    parser : argparse.ArgumentParser
        A parser with a 'workflow_config' item inside.
    
    Returns
    -------
    parser : argparse.ArgumentParser
        If parser.workflow_config is None, returns the unmodified
        input parameter. Otherwise, set its items based on the flag.
    
    Raises
    ------
    NotImplementedError
        If parser.workflow_config is not equal to a supported string.
        Which shouldn't happen, because this function should not be 
        called on its own.
    """
    if parser.workflow_config is not None:
        if parser.workflow_config == 'brightspin':
            parser.lag_max = 9
            parser.lag_step = 0.3
            parser.lagged_regression = True
            parser.run_conv = True
            parser.apply_filter = False
        elif parser.workflow_config == 'brightspin-clinical':
            parser.lag_max = 20
            parser.lag_step = 0.3
            parser.lagged_regression = True
            parser.run_conv = True
            parser.apply_filter = False
        elif parser.workflow_config == 'baltimore':
            parser.run_conv = False
            parser.apply_filter = True
            parser.lowcut = 0.02
            parser.highcut = 0.04
            parser.fname_co2 = ''
            parser.lagged_regression = False
        elif parser.workflow_config == 'baltimore-lag':
            parser.run_conv = False
            parser.apply_filter = True
            parser.lowcut = 0.02
            parser.highcut = 0.04
            parser.fname_co2 = ''
            parser.lagged_regression = True
        else:
            raise NotImplementedError(f'{parser.workflow_config} is not configured. '
                                      'In fact, you shouldn\'t see this message at all.')

    del parser.workflow_config
    return parser


if __name__ == '__main__':
    raise RuntimeError('phys2cvr/cli/run.py should not be run directly;\n'
                       'Please `pip install` phys2cvr and use the '
                       '`phys2cvr` command')


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
