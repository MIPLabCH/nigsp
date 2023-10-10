#!/usr/bin/env python3
"""
Blocks of code for workflows.

Attributes
----------
LGR
    Logger
"""

import logging
import os
import typing as ty

import numpy as np
import pydra

# TODO: clean import
from nigsp import io, operations
from nigsp import surrogates as surr
from nigsp import timeseries as ts
from nigsp import viz
from nigsp.objects import SCGraph
from nigsp.operations import nifti
from nigsp.operations.metrics import SUPPORTED_METRICS

LGR = logging.getLogger(__name__)


# @pydra.mark.task
def nifti_to_timeseries(fname, atlasname):
    """
    Read a nifti file and returns a normalised timeseries from an atlas.

    Parameters
    ----------
    fname : string or os.PathLike
        Filename (and path) of a functional timeseries nifti dataset.
    atlasname : string or os.PathLike
        Filename (and path) of an atlas nifti dataset.

    Returns
    -------
    numpy.ndarray
        The average parcel timeseries from the given atlas.
    numpy.ndarray
        The atlas data.
    3D Nifti1Image
        The full nifti image of the atlas.
    """
    _, fname = io.check_ext(io.EXT_NIFTI, fname, scan=True)
    _, atlasname = io.check_ext(io.EXT_NIFTI, atlasname, scan=True)

    data, mask, _ = io.load_nifti_get_mask(fname)
    atlas, amask, img = io.load_nifti_get_mask(atlasname, is_mask=True, ndim=3)
    mask *= amask

    timeseries = nifti.apply_atlas(data, atlas, mask)

    return timeseries, atlas, img


# @pydra.mark.task
def export_metric(scgraph, outext, outprefix):
    """
    Export the metrics computed within the library.

    Parameters
    ----------
    scgraph : SCGraph object
        The native object of this library.
    outext : str
        The desired extension for export - it will force the type of file created.
    outprefix : str
        The desired prefix for the export.

    Returns
    -------
    0
        If everything goes well
    """
    return export_metric_base(
        scgraph.atlas, scgraph.img, scgraph.sdi, scgraph.gsdi, outext, outprefix
    )


# @pydra.mark.task
# @pydra.mark.annotate(
#     {
#         "atlas": ty.Any,
#         "img": ty.Any,
#         "sdi": ty.Any,
#         "gsdi": ty.Any,
#         "outext": ty.Any
#     }
# )
def export_metric_base(atlas, img, sdi, gsdi, outext, outprefix):
    """
    Export the metrics computed within the library.

    Parameters
    ----------
    atlas : np.array
        ATLAS
    img : np.array
        IMG
    sdi : np.array
        SDI
    gsdi : np.array
        GSDI
    outext : str
        The desired extension for export - it will force the type of file created.
    outprefix : str
        The desired prefix for the export.

    Returns
    -------
    0
        If everything goes well
    """
    if outext in io.EXT_NIFTI:
        try:
            import nibabel as _
        except ImportError:
            LGR.warning(
                "The necessary library for nifti export (nibabel) "
                "was not found. Exporting metrics in TSV format instead."
            )
            outext = ".tsv.gz"
        if img is None:
            LGR.warning(
                "A necessary atlas nifti image was not found. "
                "Exporting metrics in TSV format instead."
            )
            outext = ".tsv.gz"

    if sdi is not None:
        if outext in io.EXT_NIFTI:
            data = nifti.unfold_atlas(sdi, atlas)
            io.export_nifti(data, img, f"{outprefix}sdi{outext}")
        else:
            io.export_mtx(sdi, f"{outprefix}sdi{outext}")
    elif gsdi is not None:
        for k in gsdi.keys():
            if outext in io.EXT_NIFTI:
                data = nifti.unfold_atlas(gsdi[k], atlas)
                io.export_nifti(data, img, f"{outprefix}gsdi_{k}{outext}")
            else:
                io.export_mtx(gsdi[k], f"{outprefix}gsdi_{k}{outext}")

    return 0


@pydra.mark.task
@pydra.mark.annotate(
    {
        "scname": ty.Any,
        "fname": ty.Any,
        "atlasname": ty.Any,
        "index": ty.Any,
        "method": ty.Any,
        "surr_type": ty.Any,
        "p": ty.Any,
        "comp_metric": ty.Any,
        "return": {
            "sc_is": ty.Any,
            "func_is": ty.Any,
            "atlas_is": ty.Any,
            "comp_metric": ty.Any,
        },
    }
)
def check_input(scname, fname, atlasname, index, method, surr_type, p, comp_metric):
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

    return sc_is, func_is, atlas_is, comp_metric


@pydra.mark.task
@pydra.mark.annotate(
    {
        "fname": ty.Any,
        "scname": ty.Any,
        "atlasname": ty.Any,
        "sc_is": ty.Any,
        "func_is": ty.Any,
        "atlas_is": ty.Any,
        "return": {"mtx": ty.Any, "timeseries": ty.Any, "atlas": ty.Any, "img": ty.Any},
    }
)
def read_data(fname, scname, atlasname, sc_is, func_is, atlas_is, cwd=None):
    # TODO: review this dirty quick code
    if cwd:
        scname = os.path.normpath(os.path.join(cwd, scname))
        atlasname = os.path.normpath(os.path.join(cwd, atlasname))

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
                f"Input file {atlasname} is not of a supported type."
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
        # TODO: review this dirty quick line of code
        f = os.path.normpath(os.path.join(cwd, f))
        if func_is["nifti"] and atlas_is["nifti"]:
            t, atlas, img = nifti_to_timeseries(f, atlasname)
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
    return mtx, timeseries, atlas, img


@pydra.mark.task
@pydra.mark.annotate(
    {
        "outdir": ty.AnyStr,
        "outname": ty.AnyStr,
        "return": {"outprefix": ty.Any, "outext": ty.Any},
    }
)
def prepare_output(outdir, outname=None):
    if outname is not None:
        _, outprefix, outext = io.check_ext(io.EXT_ALL, outname, remove=True)
        outprefix = os.path.join(outdir, f"{os.path.split(outprefix)[1]}_")
    else:
        outprefix = f"{outdir}{os.sep}"

    return outprefix, outext


# TODO: might be deleted for no usage at the moment
def plot_metric(scgraph, **kwargs):
    """
    Call plot_metric_base with scgraph object

    Parameters
    ----------
    scgraph : SCGraph object
        The internal object containing all data.
    """
    return plot_metric_base(scgraph.sdi, scgraph.gsdi, **kwargs)


def plot_metric_base(sdi, gsdi, outprefix, atlas=None, thr=None):
    """
    If possible, plot metrics as markerplot.

    Parameters
    ----------
    sdi :
        Structural Decoupling Index.
    gsdi:
        Generalised SDI
    outprefix : str
        The prefix of the png file to export
    img : 3DNiftiImage or None, optional
        The nifti image of the atlas
    atlas : 3D Nifti1Image, numpy.ndarray, or None, optional
        Either a nifti image containing a valid atlas or a set of parcel coordinates.
    thr : float or None, optional
        The threshold to use in plotting the nodes.
    """
    # Check that atlas format is supported.
    try:
        atlas.header
        atlas_plot = atlas
    except AttributeError:
        try:
            atlas.min()
            if atlas.ndim == 2 and atlas.shape[1] == 3:
                atlas_plot = atlas
        except AttributeError:
            LGR.warning(
                "The provided atlas is not in a format supported for markerplots."
            )
            atlas_plot = None

    # If it is, plot.
    if atlas_plot is not None:
        if sdi is not None:
            viz.plot_nodes(sdi, atlas_plot, filename=f"{outprefix}sdi.png", thr=thr)
        elif gsdi is not None:
            for k in gsdi.keys():
                viz.plot_nodes(
                    gsdi[k],
                    atlas_plot,
                    filename=f"{outprefix}gsdi_{k}.png",
                    thr=thr,
                )

    return 0


@pydra.mark.task
@pydra.mark.annotate(
    {
        "mtx": ty.Any,
        "return": {"eigenval": ty.Any, "eigenvec": ty.Any, "lapl_mtx": ty.Any},
    }
)
def laplacian(mtx):
    # Perform Laplacian on the structural connectivity matrix
    # Return the Laplacian matrix
    # operation done by : scgraph.structural_decomposition()
    LGR.info("Run laplacian decomposition of structural graph.")

    lapl_mtx = operations.symmetric_normalised_laplacian(mtx)
    eigenval, eigenvec = operations.decomposition(lapl_mtx)

    return eigenval, eigenvec, lapl_mtx


@pydra.mark.task
@pydra.mark.annotate(
    {
        "timeseries": ty.Any,
        "eigenvec": ty.Any,
        "return": {"energy": ty.Any},
    }
)
def timeseries_proj(timeseries, eigenvec, energy=True, mean=True):
    # Perform timeseries projection on the graph
    # Return the energy
    LGR.info("Compute the energy of the graph.")

    energy = operations.graph_fourier_transform(timeseries, eigenvec, energy, mean)
    return energy


@pydra.mark.task
@pydra.mark.annotate(
    {
        "energy": ty.Any,
        "return": {"index": ty.Any},
    }
)
def cutoffDetection(energy, index="median"):
    # Perform frequency cutoff detection
    # Return the detected cutoff frequency
    # if index is None:
    #     return index
    LGR.info("Compute Cutoff Frequency.")
    index = operations.median_cutoff_frequency_idx(energy)
    return index


@pydra.mark.task
@pydra.mark.annotate(
    {
        "timeseries": ty.Any,
        "eigenvec": ty.Any,
        "index": ty.Any,
        "return": {"evec_split": ty.Any, "ts_split": ty.Any},
    }
)
def filteringGSP(timeseries, eigenvec, index, keys=["low", "high"]):
    # Perform filtering using GSP
    # Return the filtered result
    evec_split, ts_split = operations.graph_filter(timeseries, eigenvec, index, keys)
    return evec_split, ts_split


@pydra.mark.task
@pydra.mark.annotate(
    {
        "timeseries": ty.Any,
        "ts_split": ty.Any,
        "outprefix": ty.AnyStr,
        "outext": ty.AnyStr,
        "return": {"fc": ty.Any, "fc_split": ty.Any},
    }
)
def functionalConnectivity(timeseries, ts_split, outprefix, outext, mean=True):
    """Implement functional_connectivity as task."""
    # Perform functional connectivity analysis
    if timeseries is not None:
        LGR.info("Compute FC of original timeseries.")
        fc = operations.functional_connectivity(timeseries, mean)
    if ts_split is not None:
        fc_split = dict.fromkeys(ts_split.keys())
        LGR.info("Compute FC of split timeseries.")
        for k in ts_split.keys():
            LGR.info(f"Compute FC of {k} timeseries.")
            fc_split[k] = operations.functional_connectivity(ts_split[k], mean)

    # IO: Save to file
    for k in ts_split.keys():
        LGR.info(f"Export {k} FC (data).")
        io.export_mtx(fc_split[k], f"{outprefix}fc_{k}", ext=outext)
    # Export fc
    LGR.info("Export original FC (data).")
    io.export_mtx(fc, f"{outprefix}fc", ext=outext)

    return fc, fc_split


@pydra.mark.task
@pydra.mark.annotate(
    {
        "ts_split": ty.Any,
        "outprefix": ty.AnyStr,
        "outext": ty.AnyStr,
        "return": {"sdi": ty.Any, "gsdi": ty.Any},
    }
)
def structuralDecouplingIndex(
    ts_split, outprefix, outext, mean=False, keys=None
):  # # pragma: no cover
    """Implement metrics.gsdi as class method."""

    sdi, gsdi = None, None

    # TODO: make it conditional
    # This should not happen in this moment.
    if len(ts_split.keys()) == 2:
        metric_name = "sdi"
        sdi = operations.sdi(ts_split, mean, keys)
    elif len(ts_split.keys()) > 2:
        metric_name = "gsdi"
        gsdi = operations.gsdi(ts_split, mean, keys)
    # # Export non-thresholded metrics
    LGR.info(f"Export non-thresholded version of {metric_name}.")
    # TODO: check if it useful to run export_metric() here and in surrogate
    # export_metric(scgraph, outext, outprefix)

    return sdi, gsdi


@pydra.mark.task
@pydra.mark.annotate(
    {
        "ts_split": ty.Any,
        "evec_split": ty.Any,
        "eigenvec": ty.Any,
        "eigenval": ty.Any,
        "outprefix": ty.AnyStr,
        "outext": ty.AnyStr,
    }
)
def export(ts_split, evec_split, eigenvec, eigenval, outprefix, outext):
    # Export eigenvalues, eigenvectors, and split timeseries and eigenvectors
    for k in ts_split.keys():
        LGR.info(f"Export {k} timeseries.")
        io.export_mtx(ts_split[k], f"{outprefix}timeseries_{k}", ext=outext)
        LGR.info(f"Export {k} eigenvectors.")
        io.export_mtx(evec_split[k], f"{outprefix}eigenvec_{k}", ext=outext)
    LGR.info("Export original eigenvectors.")
    io.export_mtx(eigenvec, f"{outprefix}eigenvec", ext=outext)
    LGR.info("Export original eigenvalues.")
    io.export_mtx(eigenval, f"{outprefix}eigenval", ext=outext)


@pydra.mark.task
@pydra.mark.annotate(
    {
        "lapl_mtx": ty.Any,
        "mtx": ty.Any,
        "timeseries": ty.Any,
        "ts_split": ty.Any,
        "fc": ty.Any,
        "fc_split": ty.Any,
        "img": ty.Any,
        "atlas": ty.Any,
        "sdi": ty.Any,
        "gsdi": ty.Any,
        "outprefix": ty.AnyStr,
    }
)
def visualize(
    lapl_mtx, mtx, timeseries, ts_split, fc, fc_split, img, atlas, sdi, gsdi, outprefix
):
    # If possible, create plots!
    try:
        import matplotlib as _
        import nilearn as _

    except ImportError:
        LGR.warning(
            "The necessary libraries for graphics (nilearn, matplotlib) "
            "were not found. Skipping graphics."
        )

    # Plot original SC and Laplacian
    LGR.info("Plot laplacian matrix.")
    viz.plot_connectivity(lapl_mtx, f"{outprefix}laplacian.png")
    LGR.info("Plot structural connectivity matrix.")
    viz.plot_connectivity(mtx, f"{outprefix}sc.png")

    # Plot timeseries
    LGR.info("Plot original timeseries.")
    viz.plot_greyplot(timeseries, f"{outprefix}greyplot.png")
    for k in ts_split.keys():
        LGR.info(f"Plot {k} timeseries.")
        viz.plot_greyplot(ts_split[k], f"{outprefix}greyplot_{k}.png")

    # TODO: make it conditional
    # if "dfc" in comp_metric or "fc" in comp_metric:
    # Plot FC
    LGR.info("Plot original functional connectivity matrix.")
    viz.plot_connectivity(fc, f"{outprefix}fc.png")
    for k in ts_split.keys():
        LGR.info(f"Plot {k} functional connectivity matrix.")
        viz.plot_connectivity(fc_split[k], f"{outprefix}fc_{k}.png")

    # TODO: make it conditional
    # if "sdi" in comp_metric or "gsdi" in comp_metric:
    #     if atlasname is not None:
    metric_name = "sdi" if len(ts_split.keys()) == 2 else "gsdi"
    LGR.info(f"Plot {metric_name} markerplot.")
    if img is not None:
        plot_metric_base(sdi, gsdi, outprefix, img)
    elif atlas is not None:
        plot_metric_base(sdi, gsdi, outprefix, atlas)


@pydra.mark.task
@pydra.mark.annotate(
    {
        "timeseries": ty.Any,
        "eigenvec": ty.Any,
        "lapl_mtx": ty.Any,
        "index": ty.Any,
        "sdi": ty.Any,
        "gsdi": ty.Any,
        "img": ty.Any,
        "atlas": ty.Any,
        "ts_split": ty.Any,
        "p": ty.Any,
        "method": ty.Any,
        "n_surr": ty.Any,
        "surr_type": ty.Any,
    }
)
def surrogate(
    timeseries,
    eigenvec,
    lapl_mtx,
    index,
    sdi,
    gsdi,
    img,
    atlas,
    ts_split,
    p,
    method,
    n_surr,
    surr_type=None,
    seed=None,
):
    # TODO: make surrogate optional
    # if surr_type is not None:
    outprefix = "mkd_"
    # Todo: should be comperate with the version without Pydra, it was `outprefix += "mkd_"` before update
    metric_name = "sdi" if len(ts_split.keys()) == 2 else "gsdi"
    LGR.info(
        f"Test significant {metric_name} against {n_surr} structurally "
        f"{surr_type} surrogates."
    )
    # scgraph.create_surrogates(sc_type=surr_type, n_surr=n_surr, seed=seed)
    surr = SCGraph.create_surrogates_base(
        timeseries, eigenvec, lapl_mtx, sc_type=surr_type, n_surr=n_surr, seed=seed
    )

    _, surr_split = operations.graph_filter(surr, eigenvec, index)
    # TODO: make it conditional
    # if "sdi" in comp_metric or "gsdi" in comp_metric:
    # scgraph.test_significance(method=method, p=p, return_masked=True)

    mean = False  # TODO: should be check wasn't there before update
    if sdi is not None:
        surr_sdi = operations.sdi(surr_split, mean, keys=None)
        sdi = operations.test_significance(
            surr=surr_sdi,
            data=sdi,
            method=method,
            p=p,
            return_masked=True,
            mean=False,
        )
    if gsdi is not None:
        surr_sdi = operations.gsdi(surr_split, mean, keys=None)
        gsdi = operations.test_significance(
            surr=surr_sdi,
            data=gsdi,
            method=method,
            p=p,
            return_masked=True,
            mean=False,
        )

    # Export thresholded metrics
    # blocks.export_metric(scgraph, outext, outprefix)
    # export_metric_base(atlas, img, sdi, gsdi, outext, outprefix)

    try:
        import matplotlib as _
        import nilearn as _

        if atlas is not None:
            LGR.info(f"Plot {metric_name} markerplot.")
            if img is not None:
                plot_metric_base(sdi, gsdi, outprefix, atlas=img, thr=0)
            elif atlas is not None:
                plot_metric_base(sdi, gsdi, outprefix, atlas=atlas, thr=0)

    except ImportError:
        pass


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
