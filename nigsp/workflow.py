#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
`nigsp` main workflow and related functions.

The workflow is callable either as a python function, or (prefereably)
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

from nigsp import _version, blocks, io, references
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
    Main workflow for nigsp, following the methods described in [1].

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
        If the projected timeseries are not splitted to compute SDI or gSDI.

    See also
    --------
    [1] Preti, M.G., Van De Ville, D. Decoupling of brain function from structure
    reveals regional behavioral specialization in humans. Nat Commun 10, 4747 (2019).
    https://doi.org/10.1038/s41467-019-12765-7

    Configuration model: https://en.wikipedia.org/wiki/Configuration_model
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

    # #### Check input #### #

    # Check data files
    LGR.info(f"Input structural connectivity file: {scname}")
    sc_is = dict.fromkeys(io.EXT_DICT.keys(), False)
    LGR.info(f"Input functional file(s): {fname}")
    func_is = dict.fromkeys(io.EXT_DICT.keys(), "")
    atlas_is = dict.fromkeys(io.EXT_DICT.keys(), False)
    if atlasname:
        LGR.info(f"Input atlas file: {atlasname}")

    # Check inputs type
    for k in io.EXT_DICT.keys():
        func_is[k] = []
        for f in fname:
            func_is[k] += [io.check_ext(io.EXT_DICT[k], f)[0]]
        # Check that func files are all of the same kind
        func_is[k] = all(func_is[k])

        sc_is[k], _ = io.check_ext(io.EXT_DICT[k], scname)

        if atlasname is not None:
            atlas_is[k], _ = io.check_ext(io.EXT_DICT[k], atlasname)

    # Check that other inputs are supported
    if index != "median" and type(index) is not int:
        raise ValueError(f"Index {index} of type {type(index)} is not valid.")
    if method not in surr.STAT_METHOD and method is not None:
        raise NotImplementedError(
            f"Method {method} is not supported. Supported "
            f"methods are: {surr.STAT_METHOD}"
        )
    if surr_type not in surr.SURR_TYPE and surr_type is not None:
        raise NotImplementedError(
            f"Surrogate type {surr_type} is not supported. "
            f"Supported types are: {surr.SURR_TYPE}"
        )
    if p < 0 or p > 1:
        raise ValueError(
            "P value must be between 0 and 1, but {p} was provided instead."
        )

    # Check what metric to compute
    if comp_metric not in [[], None]:
        for item in comp_metric:
            if item not in SUPPORTED_METRICS:
                raise NotImplementedError(
                    f"Metric {item} is not supported. "
                    f"Supported metrics are: {SUPPORTED_METRICS}"
                )
    else:
        comp_metric = SUPPORTED_METRICS

    # #### Prepare Outputs #### #
    if outname is not None:
        _, outprefix, outext = io.check_ext(io.EXT_ALL, outname, remove=True)
        outprefix = os.path.join(outdir, f"{os.path.split(outprefix)[1]}_")
    else:
        outprefix = f"{outdir}{os.sep}"

    # #### Read in data #### #

    # Read in structural connectivity matrix
    if sc_is["1D"]:
        mtx = io.load_txt(scname, shape="square")
    elif sc_is["mat"]:
        mtx = io.load_mat(scname, shape="square")
    elif sc_is["xls"]:
        mtx = io.load_xls(scname, shape="square")
    else:
        raise NotImplementedError(f"Input file {scname} is not of a supported type.")

    # Read in atlas, if defined
    if atlasname is not None:
        if (
            atlas_is["1D"] or atlas_is["mat"] or atlas_is["xls"] or atlas_is["nifti"]
        ) is False:
            raise NotImplementedError(
                f"Input file {atlasname} is not of a " "supported type."
            )
        elif atlas_is["1D"]:
            atlas = io.load_txt(atlasname)
        elif atlas_is["nifti"]:
            atlas, _, img = io.load_nifti_get_mask(atlasname, ndim=3)
        elif atlas_is["mat"]:
            atlas = io.load_mat(atlasname)
        elif atlas_is["xls"]:
            atlas = io.load_xls(atlasname)
    else:
        LGR.warning("Atlas not provided. Some functionalities might not work.")
        atlas, img = None, None

    # Read in functional timeseries, join them, and normalise them
    timeseries = []
    for f in fname:
        if func_is["nifti"] and atlas_is["nifti"]:
            t, atlas, img = blocks.nifti_to_timeseries(f, atlasname)
        elif func_is["nifti"] and atlas_is["nifti"] is False:
            raise NotImplementedError(
                "To work with functional file(s) of nifti format, "
                "specify an atlas file in nifti format."
            )
        elif func_is["1D"]:
            t = io.load_txt(f)
        elif func_is["mat"]:
            t = io.load_mat(f)
        elif func_is["xls"]:
            t = io.load_xls(f)
        else:
            raise NotImplementedError(f"Input file {f} is not of a supported type.")

        timeseries += [t[..., np.newaxis]]

    timeseries = np.concatenate(timeseries, axis=-1).squeeze()
    timeseries = ts.normalise_ts(timeseries)

    # #### Assign SCGraph object #### #
    scgraph = SCGraph(mtx, timeseries, atlas=atlas, img=img)

    # #### Compute SDI (split low vs high timeseries) and FC and output them #### #

    # Run laplacian decomposition and actually filter timeseries.
    LGR.info("Run laplacian decomposition of structural graph.")
    scgraph.structural_decomposition()
    LGR.info("Compute the energy of the graph and split it in parts.")
    scgraph.compute_graph_energy(mean=True).split_graph()

    if "sdi" in comp_metric or "gsdi" in comp_metric:
        # If there are more than two splits in the timeseries, compute Generalised SDI
        # This should not happen in this moment.
        if len(scgraph.split_keys) == 2:
            metric_name = "sdi"
            scgraph.compute_sdi()
        elif len(scgraph.split_keys) > 2:
            metric_name = "gsdi"
            scgraph.compute_gsdi()
        # Export non-thresholded metrics
        LGR.info(f"Export non-thresholded version of {metric_name}.")
        blocks.export_metric(scgraph, outext, outprefix)

    if "dfc" in comp_metric or "fc" in comp_metric:
        scgraph.compute_fc(mean=True)
        for k in scgraph.split_keys:
            LGR.info(f"Export {k} FC (data).")
            io.export_mtx(scgraph.fc_split[k], f"{outprefix}fc_{k}", ext=outext)
        # Export fc
        LGR.info("Export original FC (data).")
        io.export_mtx(scgraph.fc, f"{outprefix}fc", ext=outext)

    # #### Output more results (pt. 1) #### #

    # Export eigenvalues, eigenvectors, and split timeseries and eigenvectors
    for k in scgraph.split_keys:
        LGR.info(f"Export {k} timeseries.")
        io.export_mtx(scgraph.ts_split[k], f"{outprefix}timeseries_{k}", ext=outext)
        LGR.info(f"Export {k} eigenvectors.")
        io.export_mtx(scgraph.evec_split[k], f"{outprefix}eigenvec_{k}", ext=outext)
    LGR.info("Export original eigenvectors.")
    io.export_mtx(scgraph.eigenvec, f"{outprefix}eigenvec", ext=outext)
    LGR.info("Export original eigenvalues.")
    io.export_mtx(scgraph.eigenval, f"{outprefix}eigenval", ext=outext)

    # #### Additional steps #### #

    # If possible, create plots!
    try:
        import matplotlib as _
        import nilearn as _

        # Plot original SC and Laplacian
        LGR.info("Plot laplacian matrix.")
        viz.plot_connectivity(scgraph.lapl_mtx, f"{outprefix}laplacian.png")
        LGR.info("Plot structural connectivity matrix.")
        viz.plot_connectivity(scgraph.mtx, f"{outprefix}sc.png")

        # Plot timeseries
        LGR.info("Plot original timeseries.")
        viz.plot_greyplot(scgraph.timeseries, f"{outprefix}greyplot.png")
        for k in scgraph.split_keys:
            LGR.info(f"Plot {k} timeseries.")
            viz.plot_greyplot(scgraph.ts_split[k], f"{outprefix}greyplot_{k}.png")

        if "dfc" in comp_metric or "fc" in comp_metric:
            # Plot FC
            LGR.info("Plot original functional connectivity matrix.")
            viz.plot_connectivity(scgraph.fc, f"{outprefix}fc.png")
            for k in scgraph.split_keys:
                LGR.info(f"Plot {k} functional connectivity matrix.")
                viz.plot_connectivity(scgraph.fc_split[k], f"{outprefix}fc_{k}.png")
        if "sdi" in comp_metric or "gsdi" in comp_metric:
            if atlasname is not None:
                LGR.info(f"Plot {metric_name} markerplot.")
                if img is not None:
                    blocks.plot_metric(scgraph, outprefix, img)
                elif atlas is not None:
                    blocks.plot_metric(scgraph, outprefix, atlas)

    except ImportError:
        LGR.warning(
            "The necessary libraries for graphics (nilearn, matplotlib) "
            "were not found. Skipping graphics."
        )

    # If required, create surrogates, test, and export masked metrics
    if surr_type is not None:
        outprefix += "mkd_"
        LGR.info(
            f"Test significant {metric_name} against {n_surr} structurally "
            f"{surr_type} surrogates."
        )
        scgraph.create_surrogates(sc_type=surr_type, n_surr=n_surr, seed=seed)
        # #!# Export surrogates!
        if "sdi" in comp_metric or "gsdi" in comp_metric:
            scgraph.test_significance(method=method, p=p, return_masked=True)
            # Export thresholded metrics
            blocks.export_metric(scgraph, outext, outprefix)

            try:
                import matplotlib as _
                import nilearn as _

                if atlasname is not None:
                    LGR.info(f"Plot {metric_name} markerplot.")
                    if img is not None:
                        blocks.plot_metric(scgraph, outprefix, atlas=img, thr=0)
                    elif atlas is not None:
                        blocks.plot_metric(scgraph, outprefix, atlas=atlas, thr=0)

            except ImportError:
                pass

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
