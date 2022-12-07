#!/usr/bin/env python3
"""
Module to plot graphs.

All `viz` functions require the extra modules `matplotlib` and `nibabel`,
installable using the flag:
```shell
$ pip3 install nigsp[viz]
```

Attributes
----------
FIGSIZE : tuple
    Figure size
LGR
    Logger
SET_DPI : int
    DPI of the figure
"""

import logging

import numpy as np

from nigsp.operations.timeseries import resize_ts

LGR = logging.getLogger(__name__)
SET_DPI = 100
FIGSIZE = (18, 10)
FIGSIZE_SQUARE = (6, 5)
FIGSIZE_LONG = (10, 5)


def plot_connectivity(mtx, filename=None, closeplot=False):
    """
    Create a connectivity matrix plot.

    If mtx has 3 dimensions, average first along the last axis.

    Parameters
    ----------
    mtx : numpy.ndarray
        A (square) array with connectivity information inside.
    filename : None, str, or os.PathLike, optional
        The path to save the plot on disk.
    closeplot : bool, optional
        Whether to close plots after saving or not. Mainly used for debug
        or use with live python/ipython instances.

    Returns
    -------
    0
        If there are no errors.

    Raises
    ------
    ImportError
        If matplotlib and/or nilearn are not installed.
    ValueError
        If mtx has more than 3 dimensions.

    Notes
    -----
    Requires `matplotlib` and `nilearn`
    """
    try:
        import matplotlib.pyplot as plt
        from nilearn.plotting import plot_matrix
    except ImportError:
        raise ImportError(
            "nilearn and matplotlib are required to plot node images. "
            "Please see install instructions."
        )

    mtx = mtx.squeeze()
    if mtx.ndim > 3:
        raise ValueError(
            "Cannot plot connectivity matrices for matrix of dimensions > 3."
        )
    elif mtx.ndim == 3:
        LGR.warning("Since matrix is 3D, averaging across last dimension.")
        mtx = mtx.mean(axis=-1)

    if mtx.shape[0] != mtx.shape[1]:
        LGR.warning("Given matrix is not a square matrix!")

    LGR.info("Creating connectivity plot.")
    plt.figure(figsize=FIGSIZE_SQUARE)
    plot_matrix(mtx)

    if filename is not None:
        plt.savefig(filename, dpi=SET_DPI)
        closeplot = True

    if closeplot:
        plt.close()

    return 0


def plot_greyplot(timeseries, filename=None, title=None, resize=None, closeplot=False):
    """
    Create a greyplot (a.k.a. carpet plot a.k.a. timeseries plot).

    If timeseries has 3 dimensions, average first along the last axis.

    Parameters
    ----------
    timeseries : numpy.ndarray
        An array representing a timeseries. Time has to be encoded in the
        second dimension (axis=1).
    filename : None, str, or os.PathLike, optional
        The path to save the plot on disk.
    title : None or str, optional
        Add a title to the graph
    resize : 'spc', 'norm', 'gnorm', 'demean', 'gdemean' tuple, list, or None, optional
        Whether to resize the signal or not before plotting.
        If 'spc', compute signal percentage change
        If 'norm', normalise signals (z-score)
        If 'gnorm', globally normalise signals (keep relationship between timeseries)
        If 'demean', remove signal average
        If 'gdemean', remove global average
        If 'gsr', remove global signal (average across points)
        If tuple or list, rescale signals between those two values
        If None, don't do anything (default)
    closeplot : bool, optional
        Whether to close plots after saving or not. Mainly used for debug
        or use with live python/ipython instances.

    Returns
    -------
    0
        If there are no errors.

    Raises
    ------
    ImportError
        If matplotlib is not installed.
    ValueError
        If timeseries has more than 3 dimensions.

    Notes
    -----
    Requires `matplotlib`
    See `timeseries.rescale_ts`
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError(
            "matplotlib is required to plot node images. "
            "Please see install instructions."
        )

    timeseries = timeseries.squeeze()
    if timeseries.ndim > 3:
        raise ValueError("Cannot plot greyplots for timeseries of dimensions > 3.")
    elif timeseries.ndim == 3:
        LGR.warning("Since timeseries is 3D, averaging across last dimension.")
        timeseries = timeseries.mean(axis=-1)

    timeseries = resize_ts(timeseries, resize)

    LGR.info("Creating greyplot.")
    plt.figure(figsize=FIGSIZE_LONG)
    if title is not None:
        plt.title(title)
    vmax = np.percentile(timeseries, 99)
    vmin = np.percentile(timeseries, 1)
    plt.imshow(timeseries, cmap="gray", vmin=vmin, vmax=vmax)
    plt.colorbar()
    plt.tight_layout()

    if filename is not None:
        plt.savefig(filename, dpi=SET_DPI)
        closeplot = True

    if closeplot:
        plt.close()
    else:
        plt.show()

    return 0


def plot_nodes(ns, atlas, filename=None, thr=None, closeplot=False):
    """
    Create a marker plot in the MNI space.

    If ns has 2 dimensions, average first along last dimension.

    Parameters
    ----------
    ns : numpy.ndarray
        A 1- or 2- D array that contains the value of the nodes.
    atlas : str, os.PathLike, 3D Nifti1Image, or numpy.ndarray
        The 3d nifti image of an atlas, a string or path to its position,
        or a list of coordinates of the center of mass of parcels.
    filename : None, str, or os.PathLike, optional
        The path to save the plot on disk.
    thr : float or None, optional
        The threshold to use in plotting the nodes.
    closeplot : bool, optional
        Whether to close plots after saving or not. Mainly used for debug
        or use with live python/ipython instances.

    Returns
    -------
    0
        If there are no errors.

    Raises
    ------
    ImportError
        If matplotlib and/or nilearn are not installed.
    ValueError
        If ns has more than 2 dimensions.
        If coordinates can't be extracted from atlas.

    Notes
    -----
    Requires `matplotlib` and `nilearn`
    """
    try:
        import matplotlib.pyplot as plt
        from nilearn.plotting import find_parcellation_cut_coords, plot_markers
    except ImportError:
        raise ImportError(
            "nilearn and matplotlib are required to plot node images. "
            "Please see install instructions."
        )
    # First check that ns is a valid source of data.
    ns = ns.squeeze()
    if ns.ndim > 2:
        raise ValueError("Cannot plot node values for matrix of dimensions > 2.")
    elif ns.ndim == 2:
        LGR.warning("Given matrix has 2 dimensions, averaging across last dimension.")
        ns = ns.mean(axis=-1)

    # Then treat atlas
    if type(atlas) is np.ndarray:
        if atlas.ndim > 2 or atlas.shape[1] != 3:
            raise NotImplementedError(
                "Only atlases in nifti format or list of coordinates are supported."
            )
        else:
            coord = atlas
    else:
        coord = find_parcellation_cut_coords(atlas)

    if ns.shape[0] != coord.shape[0]:
        raise ValueError("Node array and coordinates array have different length.")

    LGR.info("Creating markerplot.")
    plt.figure(figsize=FIGSIZE)
    plot_markers(ns, coord, node_threshold=thr)

    if filename is not None:
        plt.savefig(filename, dpi=SET_DPI)
        closeplot = True

    if closeplot:
        plt.close()

    return 0


def plot_edges(mtx, atlas, filename=None, thr=None, closeplot=False):
    """
    Create a connectivity plot in the MNI space.

    If mtx has 2 dimensions, average first along last dimension.

    Parameters
    ----------
    mtx : numpy.ndarray
        A 2- or 3- D array that contains the value of the nodes.
    atlas : str, os.PathLike, 3D Nifti1Image, or numpy.ndarray
        The 3d nifti image of an atlas, a string or path to its position,
        or a list of coordinates of the center of mass of parcels.
    filename : None, str, or os.PathLike, optional
        The path to save the plot on disk.
    thr : float, str or None, optional
        The threshold to use in plotting the nodes.
        If `str`, needs to express a percentage.
    closeplot : bool, optional
        Whether to close plots after saving or not. Mainly used for debug
        or use with live python/ipython instances.

    Returns
    -------
    0
        If there are no errors.

    Raises
    ------
    ImportError
        If matplotlib and/or nilearn are not installed.
    ValueError
        If mtx has more than 3 dimensions.
        If coordinates can't be extracted from atlas.

    Notes
    -----
    Requires `matplotlib` and `nilearn`
    """
    try:
        import matplotlib.pyplot as plt
        from nilearn.plotting import cm, find_parcellation_cut_coords, plot_connectome
    except ImportError:
        raise ImportError(
            "nilearn and matplotlib are required to plot node images. "
            "Please see install instructions."
        )
    # First check that mtx is a valid source of data.
    mtx = mtx.squeeze()
    if mtx.ndim > 3:
        raise ValueError("Cannot plot node values for matrix of dimensions > 3.")
    elif mtx.ndim == 3:
        LGR.warning("Given matrix has 3 dimensions, averaging across last dimension.")
        mtx = mtx.mean(axis=-1)

    # Then treat atlas
    if type(atlas) is np.ndarray:
        if atlas.ndim > 2 or atlas.shape[1] != 3:
            raise NotImplementedError(
                "Only atlases in nifti format or list of coordinates are supported."
            )
        else:
            coord = atlas
    else:
        coord = find_parcellation_cut_coords(atlas)

    if mtx.shape[0] != coord.shape[0]:
        raise ValueError("Matrix axis and coordinates array have different length.")

    LGR.info("Creating connectome-like plot.")
    plt.figure(figsize=FIGSIZE)

    pc_args = {
        "adjacency_matrix": mtx,
        "node_coords": coord,
        "node_color": "black",
        "node_size": 5,
        "edge_threshold": thr,
        "colorbar": True,
    }

    if mtx.min() >= 0:
        pc_args["edge_vmin"] = 0
        pc_args["edge_vmax"] = mtx.max()
        pc_args["edge_cmap"] = cm.red_transparent_full_alpha_range

    plot_connectome(**pc_args)

    if filename is not None:
        plt.savefig(filename, dpi=SET_DPI)
        closeplot = True

    if closeplot:
        plt.close()

    return 0


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
