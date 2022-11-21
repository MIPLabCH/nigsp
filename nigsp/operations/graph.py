#!/usr/bin/env python3
"""
Compute graph properties.

Attributes
----------
LGR
    Logger
"""

import logging

from numpy import abs

LGR = logging.getLogger(__name__)


def zerocross(eigenvec):
    """
    Compute the amount of zero-crossing of an eigenvector matrix (for each eigenvector).

    Parameters
    ----------
    eigenvec : numpy.ndarray
        The eigenvectors from a decomposition.

    Returns
    -------
    numpy.ndarray
        A 1D array with the amount of zero-crossing for each eigenvector.
    """
    return (eigenvec[:-1, ...] * eigenvec[1:, ...] < 0).sum(axis=0)


def nodestrength(mtx, mean=False):
    """
    Compute the node strength of a graph.

    Parameters
    ----------
    mtx : numpy.ndarray
        A matrix depicting a graph.
    mean : bool, optional
        If True, return the average node strength along the last axis of mtx.

    Returns
    -------
    numpy.ndarray
        The node strength.
    """
    ns = abs(mtx).sum(axis=0)

    if mean:
        ns = ns.mean(axis=-1)

    return ns


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
