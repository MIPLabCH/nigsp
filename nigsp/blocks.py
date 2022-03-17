#!/usr/bin/env python3
"""
Operations on graphs and graph derived properties.

Attributes
----------
LGR
    Logger
"""

import logging

from nigsp import io
from nigsp.operations import nifti


LGR = logging.getLogger(__name__)


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
    atlas, amask, img = io.load_nifti_get_mask(atlasname, ndim=3)
    mask *= amask

    timeseries = nifti.apply_atlas(data, atlas, mask)

    return timeseries, atlas, img


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
            LGR.warning('The necessary library for nifti export (nibabel) '
                        'was not found. Exporting metrics in CSV format instead.')
            outext = '.csv'
        if scgraph.img is None:
            LGR.warning('A necessary atlas nifti image was not found. '
                        'Exporting metrics in CSV format instead.')
            outext = '.csv'

    if scgraph.sdi is not None:
        if outext in io.EXT_NIFTI:
            data = nifti.unfold_atlas(scgraph.sdi, scgraph.atlas)
            io.export_nifti(data, scgraph.img, f'{outprefix}sdi{outext}')
        else:
            io.export_mtx(scgraph.sdi, f'{outprefix}sdi{outext}')
    elif scgraph.gsdi is not None:
        for k in scgraph.gsdi.keys():
            if outext in io.EXT_NIFTI:
                data = nifti.unfold_atlas(scgraph.gsdi[k], scgraph.atlas)
                io.export_nifti(data, scgraph.img, f'{outprefix}gsdi_{k}{outext}')
            else:
                io.export_mtx(scgraph.gsdi[k], f'{outprefix}gsdi_{k}{outext}')

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
