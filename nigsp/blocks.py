#!/usr/bin/env python3
"""
Blocks of code for workflows.

Attributes
----------
LGR
    Logger
"""

import logging
import typing as ty

import pydra

# TODO: clean import
from nigsp import io, operations, viz
from nigsp.operations import nifti

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
    if outext in io.EXT_NIFTI:
        try:
            import nibabel as _
        except ImportError:
            LGR.warning(
                "The necessary library for nifti export (nibabel) "
                "was not found. Exporting metrics in TSV format instead."
            )
            outext = ".tsv.gz"
        if scgraph.img is None:
            LGR.warning(
                "A necessary atlas nifti image was not found. "
                "Exporting metrics in TSV format instead."
            )
            outext = ".tsv.gz"

    if scgraph.sdi is not None:
        if outext in io.EXT_NIFTI:
            data = nifti.unfold_atlas(scgraph.sdi, scgraph.atlas)
            io.export_nifti(data, scgraph.img, f"{outprefix}sdi{outext}")
        else:
            io.export_mtx(scgraph.sdi, f"{outprefix}sdi{outext}")
    elif scgraph.gsdi is not None:
        for k in scgraph.gsdi.keys():
            if outext in io.EXT_NIFTI:
                data = nifti.unfold_atlas(scgraph.gsdi[k], scgraph.atlas)
                io.export_nifti(data, scgraph.img, f"{outprefix}gsdi_{k}{outext}")
            else:
                io.export_mtx(scgraph.gsdi[k], f"{outprefix}gsdi_{k}{outext}")

    return 0


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
def timeSeriesExtraction(bold, atlas):
    # Perform time series extraction using bold data and atlas
    # Return the extracted time series
    pass


@pydra.mark.task
@pydra.mark.annotate(
    {
        "struct_mtx": ty.Any,
        "return": {"eigenval": ty.Any, "eigenvec": ty.Any, "lapl_mtx": ty.Any},
    }
)
def laplacian(struct_mtx):
    # Perform Laplacian on the structural connectivity matrix
    # Return the Laplacian matrix
    # operation done by : scgraph.structural_decomposition()
    LGR.info("Run laplacian decomposition of structural graph.")

    lapl_mtx = operations.symmetric_normalised_laplacian(struct_mtx)
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
def timeSeries():
    # Perform time series analysis
    # Return the result
    pass


@pydra.mark.task
def decomposition():
    # Perform decomposition
    # Return the result
    pass


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
        # "ts_split": ty.Any,
        # "evec_split": ty.Any,
        # "eigenvec": ty.Any,
        # "eigenval": ty.Any,
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
        # "outext": ty.AnyStr,
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


def filteredTimeseries():
    # Perform filtering on the timeseries
    # Return the filtered timeseries
    pass


def statisticalThreshold(
    functionalConnectivity, structuralDecouplingIndex, filteredTimeseries
):
    # Perform statistical thresholding using the three inputs
    # Return the result
    pass


# @pydra.mark.task
# def glsBased():
#     # Perform GLS-based analysis
#     # Return the result
#     pass

# @pydra.mark.task
# def diffusionModel():
#     # Perform diffusion model analysis
#     # Return the result
#     pass
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
