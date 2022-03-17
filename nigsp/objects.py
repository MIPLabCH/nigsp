#!/usr/bin/env python3
"""
Toolbox objects.

Attributes
----------
LGR
    Logger
"""

import logging

from copy import deepcopy

from nigsp import operations


LGR = logging.getLogger(__name__)


class SCGraph():

    def __init__(self, mtx, timeseries, atlas=None, filename=None, img=None,
                 eigenval=None, eigenvec=None, energy=None, lapl_mtx=None,
                 index='median', evec_split=None, ts_split=None, surr=None,
                 surr_split=None, sdi=None, gsdi=None, fc=None, fc_split=None):
        """Initialise SCGraph (see class docstring)."""
        if mtx.shape[1] != mtx.shape[0]:
            raise ValueError('Graph matrix must be a square matrix, but '
                             f'given matrix has {mtx.shape}!')

        if mtx.shape[1] != timeseries.shape[0]:
            raise ValueError(f'Timeseries extracted from {timeseries.shape[0]} '
                             f'parcels, but graph has {mtx.shape[1]} nodes. '
                             'The number of parcels and nodes must be the same.')

        if timeseries.ndim > 3:
            raise ValueError('Timeseries of more than 3 dimensions are not supported '
                             f'yet, but given timeseries has {timeseries.ndim} '
                             'dimensions.')
        self.mtx = deepcopy(mtx)
        self.timeseries = deepcopy(timeseries)
        self.atlas = deepcopy(atlas)
        self.filename = deepcopy(filename)
        self.img = deepcopy(img)
        self.eigenval = deepcopy(eigenval)
        self.eigenvec = deepcopy(eigenvec)
        self.energy = deepcopy(energy)
        self.lapl_mtx = deepcopy(lapl_mtx)
        self.index = deepcopy(index)
        self.evec_split = deepcopy(evec_split)
        self.ts_split = deepcopy(ts_split)
        self.surr = deepcopy(surr)
        self.surr_split = deepcopy(surr_split)
        self.sdi = deepcopy(sdi)
        self.gsdi = deepcopy(gsdi)
        self.fc = deepcopy(fc)
        self.fc_split = deepcopy(fc_split)

    @property
    def nnodes(self):
        """Return number of nodes."""
        return self.mtx.shape[1]

    @property
    def ntimepoints(self):
        """Return number of timepoints."""
        return self.timeseries.shape[1]

    @property
    def zerocross(self):
        """Implement graph.zerocross as property."""
        return operations.zerocross(self.eigenvec)

    @property
    def split_keys(self):
        """Return the names of the splitted timeseries."""
        return list(self.ts_split.keys())

    def symmetric_normalisation(self):
        """Implement laplacian.symmetric_normalisation as class method."""
        self.lapl_mtx = operations.symmetric_normalisation(self.mtx)
        return self

    def decomposition(self):
        """Implement laplacian.decomposition as class method."""
        self.eigenval, self.eigenvec = operations.decomposition(self.lapl_mtx)
        return self

    def structural_decomposition(self):
        """Implement both laplacian operations."""
        return self.symmetric_normalisation().decomposition()

    def compute_graph_energy(self, mean=False):
        """Implement timeseries.graph_fourier_transform for energy as class method."""
        self.energy = operations.graph_fourier_transform(self.timeseries, self.eigenvec,
                                                         energy=True, mean=mean)
        return self

    def split_graph(self):
        """Implement timeseries.median_cutoff_frequency_idx as class method."""
        if self.index == 'median':
            self.index = operations.median_cutoff_frequency_idx(self.energy)
        else:
            raise ValueError(f'Unknown option {self.index} for frequency split index. '
                             'Declared index must be either an integer or \'median\'')
        self.evec_split, self.ts_split = operations.graph_filter(self.timeseries,
                                                                 self.eigenvec,
                                                                 self.index)

        return self

    def nodestrength(self, mean=False):
        """Implement graph.nodestrength as class method."""
        self.ns = operations.nodestrength(self.mtx, mean)
        return self

    def compute_sdi(self, mean=False, keys=None):
        """Implement sdi.sdi as class method."""
        self.sdi = operations.sdi(self.ts_split, mean, keys)
        return self

    def compute_gsdi(self, mean=False, keys=None):
        """Implement sdi.gsdi as class method."""
        self.gsdi = operations.gsdi(self.ts_split, mean, keys)
        return self

    def create_surrogates(self, sc_type='informed', n_surr=1000, seed=None):
        """Implement surrogates.sc_informed and sc_uninformed as class method."""
        sc_args = {'timeseries': self.timeseries, 'n_surr': n_surr}
        if seed is not None:
            sc_args['seed'] = seed

        if sc_type == 'informed':
            sc_args['eigenvec'] = self.eigenvec
            self.surr = operations.sc_informed(**sc_args)
        elif sc_type == 'uninformed':
            sc_args['lapl_mtx'] = self.lapl_mtx
            self.surr = operations.sc_uninformed(**sc_args)
        else:
            return ValueError(f'Unknown option {sc_type} for surrogate creation. '
                              'Declared type must be either \'informed\' or '
                              '\'uninformed\'')
        return self

    def test_significance(self, metric='sdi', method='Bernoulli', p=0.05,
                          return_masked=False, mean=False):
        """Implement surrogates.test_significance as class method."""
        _, self.surr_split = operations.graph_filter(self.surr,
                                                     self.eigenvec,
                                                     self.index)
        if metric == 'sdi':
            surr_sdi = operations.sdi(self.surr_split, mean, keys=None)
            metric_data = self.sdi
        elif metric == 'gsdi':
            surr_sdi = operations.gsdi(self.surr_split, mean, keys=None)
            metric_data = self.gsdi
        # #!# Check that this attribution works (should)
        metric_data = operations.test_significance(surr_sdi, metric_data,
                                                   method, p, return_masked,
                                                   mean)
        return self

    def normalise_ts(self):
        """Implement timeseries.normalise_ts for energy as class method."""
        self.timeseries = operations.normalise_ts(self.timeseries)
        return self

    def compute_fc(self, mean=False):
        """Implement timeseries.functional_connectivity as class method."""
        if self.timeseries is not None:
            LGR.info('Compute FC of original timeseries.')
            self.fc = operations.functional_connectivity(self.timeseries, mean)
        if self.ts_split is not None:
            self.fc_split = dict.fromkeys(self.ts_split.keys())
            LGR.info('Compute FC of split timeseries.')
            for k in self.ts_split.keys():
                LGR.info(f'Compute FC of {k} timeseries.')
                self.fc_split[k] = operations.functional_connectivity(self.ts_split[k],
                                                                      mean)
        return self


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
