#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
`nigsp` main workflow and related functions.

The workflow is callable either as a python function, or (preferably)
in a shell session:
```shell
$ nigsp --help
```
"""
import datetime
import logging
import os
import sys

import numpy as np
import pydra

from nigsp import _version, blocks, io, operations, references
from nigsp import surrogates as surr
from nigsp import timeseries as ts
from nigsp import utils, viz
from nigsp.cli.run import _get_parser
from nigsp.due import due
from nigsp.objects import SCGraph
from nigsp.operations.metrics import SUPPORTED_METRICS

LGR = logging.getLogger(__name__)
LGR.setLevel(logging.INFO)


def save_bash_call(fname, outdir, outname):
    """
    Save the bash call into file `p2d_call.sh`.

    Parameters
    ----------
    outdir : str or os.PathLike, optional
        output directory
    """
    fname = utils.change_var_type(fname, list, stop=False, silent=True)

    # Prepare folders
    if outdir is None:
        if outname is None:
            if len(fname) == 1:
                outdir = os.path.dirname(fname[0])
            else:
                outdir = os.path.commonpath(fname)
        else:
            outdir = os.path.split(outname)[0]

        if outdir == "" or outdir == "/":
            outdir = "."
        outdir = os.path.join(outdir, "nigsp")

    outdir = os.path.abspath(outdir)
    log_path = os.path.join(outdir, "logs")
    os.makedirs(log_path, exist_ok=True)
    arg_str = " ".join(sys.argv[1:])
    call_str = f"nigsp {arg_str}"
    outdir = os.path.abspath(outdir)
    log_path = os.path.join(outdir, "logs")
    os.makedirs(log_path, exist_ok=True)
    isotime = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
    f = open(os.path.join(log_path, f"nigsp_call_{isotime}.sh"), "a")
    f.write(f"#!bin/bash \n{call_str}")
    f.close()


@due.dcite(references.PRETI_2019)
@due.dcite(references.NIGSP)
def nigsp(
    fname,
    scname,
    atlasname=None,
    outname=None,
    outdir=None,
    comp_metric=[],
    index="median",
    surr_type=None,
    n_surr=1000,
    method="Bernoulli",
    p=0.05,
    seed=None,
    lgr_degree="info",
):
    """
    Main workflow for nigsp, following the methods described in [1]_.

    Parameters
    ----------
    fname : str or os.PathLike
        Path to the timeseries data file. It can be a text, nifti, or matlab file
        (and variants). To see the full list of support, check the general documentation.
    scname : str or os.PathLike
        Path to the structural connectivity data file. It can be a text, nifti, or matlab file
        (and variants). To see the full list of support, check the general documentation.
    atlasname : str, os.PathLike, or None, optional
        Path to the atlas data file. It can be a text, nifti, or matlab file
        (and variants). To see the full list of support, check the general documentation.
    outname : str, os.PathLike, or None, optional
        Path to the output file - or just its full name. It can be a text, nifti, or matlab file
        (and variants). If an extension is *not* declared, or if it is not currently
        supported, the program will automatically export a csv file.
        To see the full list of support, check the general documentation.
        It is *not* necessary to declare both this and `outdir` - the full path can
        be specified here.
    outdir : str, os.PathLike, or None, optional
        Path to the output folder. If it doesn't exist, it will be created.
        If both `outdir` and `outname` are declared, `outdir` overrides the path
        specified in `outname` (but not the filename!)
    comp_metric : list or None, optional
        List of metrics that should be computed. If empty (default), compute all
        metrics available.
    index : 'median' or int, optional
        The index of the eigenvector/harmonic of the graph to split the graph in
        multiple parts, or the method to find this index. Currently supports
        median energy split ('median'), which is the default.
        Note that indexing is one-based (i.e. indexing starts at 1, not 0).
    surr_type : 'informed', 'uninformed', or None, optional
        The type of surrogates to create for statistical testing.
        'Informed' surrogates are created using the empirical SC decomposition,
        shuffling eigenvectors' signs. 'Uninformed' surrogates use a configuration
        model of the same degree of the empirical SC instead.
        If surr_type is None, no statistical test is run.
    n_surr : int, optional
        Number of surrogates to be created.
    method : 'Bernoulli', 'frequentist', or None, optional
        Method to use for statistical testing or empirical data vs surrogates.
        Supported possibilities are 'Bernoulli', to test empirical data at
        the group level against a random Bernoulli process,
        or 'frequentist', to test empirical data at the group or subject level
        against the plain surrogate distribution.
    p : float (in range [0 1]), optional
        The two-tailed p value to use for testing. Must be between 0 and 1.
        The two tails will be tested against half of this value.
    seed : int or None, optional
        The seed to use to reinitialise the random number generator for
        surrogates creation.
        If `seed` is None, it will use internally specified seeds to guarantee
        replicability. It's suggested either not specify it, or specify a different
        one for each type of surrogate created.
    lgr_degree : 'debug', 'info', or 'quiet', optional
        The degree of verbosity of the logger. Default is 'info'.

    Returns
    -------
    0
        If there are no errors.

    Raises
    ------
    NotImplementedError
        If SC file is not of a supported type.
        If timeseries file is not of a supported type.
        If atlas file is not of a supported type.
        If timeseries file is a nifti file but atlas file is not.
        If statistical method is not within supported method (or None).
        If surrogate type is not within supported type (or None).
    ValueError
        If `index` is not int or is not `median`.
        If `p` is not in the range [0 1].
        If the projected timeseries are not split to compute SDI or gSDI.

    Notes
    -----
    See the original paper on SDI [1]_ for more details.

    A configuration model [2]_ is used to create uninformed surrogates.

    References
    ----------
    .. [1] Preti, M.G., Van De Ville, D. Decoupling of brain function from structure
       reveals regional behavioral specialization in humans. Nat Commun 10, 4747 (2019).
       https://doi.org/10.1038/s41467-019-12765-7
    .. [2] https://en.wikipedia.org/wiki/Configuration_model
    """
    # #### Logger preparation #### #
    fname = utils.change_var_type(fname, list, stop=False, silent=True)

    # Prepare folders
    if outdir is None:
        if outname is None:
            if len(fname) == 1:
                outdir = os.path.dirname(fname[0])
            else:
                outdir = os.path.commonpath(fname)
        else:
            outdir = os.path.split(outname)[0]

        if outdir == "" or outdir == "/":
            outdir = "."
        outdir = os.path.join(outdir, "nigsp")

    outdir = os.path.abspath(outdir)
    log_path = os.path.join(outdir, "logs")
    os.makedirs(log_path, exist_ok=True)

    # Create logfile name
    basename = "nigsp_"
    extension = "tsv"
    isotime = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
    logname = os.path.join(log_path, f"{basename}{isotime}.{extension}")

    # Set logging format
    log_formatter = logging.Formatter(
        "%(asctime)s\t%(name)-12s\t%(levelname)-8s\t%(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    # Set up logging file and open it for writing
    log_handler = logging.FileHandler(logname)
    log_handler.setFormatter(log_formatter)
    sh = logging.StreamHandler()

    if lgr_degree == "quiet":
        logging.basicConfig(
            level=logging.WARNING,
            handlers=[log_handler, sh],
            format="%(levelname)-10s %(message)s",
        )
    elif lgr_degree == "debug":
        logging.basicConfig(
            level=logging.DEBUG,
            handlers=[log_handler, sh],
            format="%(levelname)-10s %(message)s",
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            handlers=[log_handler, sh],
            format="%(levelname)-10s %(message)s",
        )

    version_number = _version.get_versions()["version"]
    LGR.info(f"Currently running nigsp version {version_number}")

    wf1 = pydra.Workflow(
        name="Input Workflow",
        input_spec=[
            "scname",
            "fname",
            "atlasname",
            "index",
            "method",
            "surr_type",
            "p",
            "comp_metric",
            "outdir",
            "outname",
            "cwd",
        ],
        scname=scname,
        fname=fname,
        atlasname=atlasname,
        index=index,
        method=method,
        surr_type=surr_type,
        p=p,
        comp_metric=comp_metric,
        outdir=outdir,
        outname=outname,
        cwd=os.getcwd(),
    )

    wf1.add(
        blocks.check_input(
            name="check_input",
            scname=wf1.lzin.scname,
            fname=wf1.lzin.fname,
            atlasname=wf1.lzin.atlasname,
            index=wf1.lzin.index,
            method=wf1.lzin.method,
            surr_type=wf1.lzin.surr_type,
            p=wf1.lzin.p,
            comp_metric=wf1.lzin.comp_metric,
        )
    )

    wf1.add(
        blocks.read_data(
            name="read_data",
            fname=wf1.lzin.fname,
            scname=wf1.lzin.scname,
            atlasname=wf1.lzin.atlasname,
            sc_is=wf1.check_input.lzout.sc_is,
            func_is=wf1.check_input.lzout.func_is,
            atlas_is=wf1.check_input.lzout.atlas_is,
            cwd=wf1.lzin.cwd,
        )
    )

    wf1.add(
        blocks.prepare_output(
            name="prepare_output", outdir=wf1.lzin.outdir, outname=wf1.lzin.outname
        )
    )

    wf1.set_output(
        [
            # check_input
            ("sc_is", wf1.check_input.lzout.sc_is),
            ("func_is", wf1.check_input.lzout.func_is),
            ("atlas_is", wf1.check_input.lzout.atlas_is),
            ("comp_metric", wf1.check_input.lzout.comp_metric),
            # read_data
            ("mtx", wf1.read_data.lzout.mtx),
            ("timeseries", wf1.read_data.lzout.timeseries),
            ("atlas", wf1.read_data.lzout.atlas),
            ("img", wf1.read_data.lzout.img),
            # prepare_output
            ("outprefix", wf1.prepare_output.lzout.outprefix),
            ("outext", wf1.prepare_output.lzout.outext),
        ]
    )

    with pydra.Submitter(plugin="cf") as sub:
        sub(wf1)

    out = wf1.result().output

    mtx = out.mtx
    timeseries = out.timeseries
    outprefix = out.outprefix
    outext = out.outext
    img = out.img
    atlas = out.atlas

    wf2 = pydra.Workflow(
        name="GSP+SDI Workflow",
        input_spec=["mtx", "timeseries", "outprefix", "outext", "img", "atlas"],
        mtx=mtx,
        timeseries=timeseries,
        # IO File Export
        outprefix=outprefix,
        outext=outext,
        # Visualize
        img=img,
        atlas=atlas,
    )
    wf2.add(blocks.laplacian(name="laplacian", mtx=wf2.lzin.mtx))
    wf2.add(
        blocks.timeseries_proj(
            name="timeseries_proj",
            timeseries=wf2.lzin.timeseries,
            eigenvec=wf2.laplacian.lzout.eigenvec,
        )
    )
    wf2.add(
        blocks.cutoffDetection(
            name="cutoffDetection", energy=wf2.timeseries_proj.lzout.energy
        )
    )
    wf2.add(
        blocks.filteringGSP(
            name="filteringGSP",
            timeseries=wf2.lzin.timeseries,
            eigenvec=wf2.laplacian.lzout.eigenvec,
            index=wf2.cutoffDetection.lzout.index,
        )
    )
    # TODO: make it optional
    # if "dfc" in comp_metric or "fc" in comp_metric:
    wf2.add(
        blocks.functionalConnectivity(
            name="functionalConnectivity",
            timeseries=wf2.lzin.timeseries,
            ts_split=wf2.filteringGSP.lzout.ts_split,
            outprefix=wf2.lzin.outprefix,
            outext=wf2.lzin.outext,
        )
    )

    wf2.add(
        blocks.structuralDecouplingIndex(
            name="SDI",
            ts_split=wf2.filteringGSP.lzout.ts_split,
            outprefix=wf2.lzin.outprefix,
            outext=wf2.lzin.outext,
        )
    )

    wf2.add(
        blocks.export(
            name="export",
            ts_split=wf2.filteringGSP.lzout.ts_split,
            evec_split=wf2.filteringGSP.lzout.evec_split,
            eigenvec=wf2.laplacian.lzout.eigenvec,
            eigenval=wf2.laplacian.lzout.eigenval,
            outprefix=wf2.lzin.outprefix,
            outext=wf2.lzin.outext,
        )
    )

    wf2.add(
        blocks.visualize(
            name="visualize",
            img=wf2.lzin.img,
            atlas=wf2.lzin.atlas,
            timeseries=wf2.lzin.timeseries,
            mtx=wf2.lzin.mtx,
            lapl_mtx=wf2.laplacian.lzout.lapl_mtx,
            ts_split=wf2.filteringGSP.lzout.ts_split,
            fc=wf2.functionalConnectivity.lzout.fc,
            fc_split=wf2.functionalConnectivity.lzout.fc_split,
            sdi=wf2.SDI.lzout.sdi,
            gsdi=wf2.SDI.lzout.gsdi,
            outprefix=wf2.lzin.outprefix,
            outext=wf2.lzin.outext,
        )
    )

    if surr_type is not None:
        wf2.add(
            blocks.surrogate(
                name="surrogate",
                img=wf2.lzin.img,
                atlas=wf2.lzin.atlas,
                timeseries=wf2.lzin.timeseries,
                mtx=wf2.lzin.mtx,
                lapl_mtx=wf2.laplacian.lzout.lapl_mtx,
                ts_split=wf2.filteringGSP.lzout.ts_split,
                fc=wf2.functionalConnectivity.lzout.fc,
                fc_split=wf2.functionalConnectivity.lzout.fc_split,
                sdi=wf2.SDI.lzout.sdi,
                gsdi=wf2.SDI.lzout.gsdi,
                outprefix=wf2.lzin.outprefix,
                outext=wf2.lzin.outext,
            )
        )

    # setting multiple workflow output
    wf2.set_output(
        [
            # laplacian output
            ("lapl_mtx", wf2.laplacian.lzout.lapl_mtx),
            ("eigenval", wf2.laplacian.lzout.eigenval),
            ("eigenvec", wf2.laplacian.lzout.eigenvec),
            # timeseries projection output
            ("energy", wf2.timeseries_proj.lzout.energy),
            # cutoff output
            ("index", wf2.cutoffDetection.lzout.index),
            # filtering GSP output
            ("evec_split", wf2.filteringGSP.lzout.evec_split),
            ("ts_split", wf2.filteringGSP.lzout.ts_split),
            # fc : functional connectity
            ("fc", wf2.functionalConnectivity.lzout.fc),
            ("fc_split", wf2.functionalConnectivity.lzout.fc_split),
            # sdi : Structural Decoupling Index
            ("sdi", wf2.SDI.lzout.sdi),
            # gsdi : Generalized Structural Decoupling Index
            ("gsdi", wf2.SDI.lzout.gsdi),
        ]
    )

    with pydra.Submitter(plugin="cf") as sub:
        sub(wf2)

    LGR.info(f"End of workflow, find results in {outdir}.")

    return 0


def _main(argv=None):
    options = _get_parser().parse_args(argv)

    save_bash_call(options.fname, options.outdir, options.outname)

    nigsp(**vars(options))


if __name__ == "__main__":
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
