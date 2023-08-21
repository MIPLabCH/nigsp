import logging

import numpy as np

LGR = logging.getLogger(__name__)


def ranktest(a, axis=None):
    # Code adapted from `scipy`; ref: https://github.com/scipy/scipy/blob/v1.11.2/scipy/stats/_stats_py.py#L10123

    """Assign ranks to data, dealing with ties appropriately.

    By default (``axis=None``), the data array is first flattened, and a flat
    array of ranks is returned. Separately reshape the rank array to the
    shape of the data array if desired (see Examples).

    Ranks begin at 1.  The `method` argument controls how ranks are assigned
    to equal values.

    Parameters
    ----------
    a : array_like
        The array of values to be ranked.
    axis : {None, int}, optional
        Axis along which to perform the ranking. If ``None``, the data array
        is first flattened.

    Returns
    -------
    ranks : ndarray
         An array of size equal to the size of `a`, containing rank
         scores.

    See Also
    --------
    scipy.stats.rankdata


    Notes
    ----------
    Borrowed from [scipy](https://github.com/scipy/scipy/blob/v1.11.2/scipy/stats/_stats_py.py#L10123)
    Copyright (c) 2001-2002 Enthought, Inc. 2003-2023, SciPy Developers.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
    WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
    USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    Re-distributing the source code with the BSD 3-Clause License
    """

    if axis is not None:
        a = np.asarray(a)
        return np.apply_along_axis(ranktest, axis, a)

    arr = np.ravel(np.asarray(a))
    algo = "quicksort"
    sorter = np.argsort(arr, kind=algo)
    inv = np.empty(sorter.size, dtype=np.intp)
    inv[sorter] = np.arange(sorter.size, dtype=np.intp)

    arr = arr[sorter]
    obs = np.r_[True, arr[1:] != arr[:-1]]
    dense = obs.cumsum()[inv]

    # cumulative counts of each unique value
    count = np.r_[np.nonzero(obs)[0], len(obs)]

    # average method
    return 0.5 * (count[dense] + count[dense - 1] + 1)


# Code adapted from `mne-python`; ref: https://mne.tools/stable/generated/mne.stats.ttest_1samp_no_p.html
def ttest_1samp_no_p(X, axis=0):
    """Perform one-sample t-test.

    This function avoids a (relatively) time-consuming p-value calculation,
    and can adjust for implausibly small variance values: Ridgway et al. 2012 [1]

    Parameters
    ----------
    X : array
        Array to return t-values for.
    axis: int
        Axis along which to compute test. Default is 0.
    sigma : float
        The variance estimate will be given by ``var + sigma * max(var)`` or
        ``var + sigma``, depending on "method". By default this is 0 (no
        adjustment). See Notes for details.

    Returns
    -------
    t : array
        T-values, potentially adjusted using the hat method.

    References
    ----------
    .. [1] Ridgway G et al 2012 https://doi.org/10.1016/j.neuroimage.2011.10.027.

    See Also
    --------
    mne.stats.ttest_1samp_no_p
    scipy.stats.ttest_1samp

    Notes
    -----
    Borrowed from [mne-python](https://mne.tools/stable/generated/mne.stats.ttest_1samp_no_p.html)
    Copyright (c) 2011-2022, authors of MNE-Python

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
    WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
    USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    Re-distributing the source code with the BSD 3-Clause License


    `mne.stats.ttest_1samp_no_p` was originally borrowed from [Scipy](https://github.com/scipy/scipy/blob/v1.11.1/scipy/stats/_stats_py.py#L6763-L6943)
    Copyright (c) 2001-2002 Enthought, Inc. 2003-2023, SciPy Developers.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
    WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
    USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    Re-distributing the source code with the BSD 3-Clause License
    """
    var = np.var(X, axis=axis, ddof=1)
    return np.mean(X, axis=0) / np.sqrt(var / X.shape[0])


def two_level_statistical_model(
    empirical_SDI,
    surrogate_SDI,
    output_dir_first_level=None,
    output_dir_second_level=None,
    n_perms=1000,
    n_jobs=-1,
):
    """
    Summary
    -------
    Involves 3 steps:
    a)
    Takes in the empirical SDI to test against the surrogate SDI.
    Surrogate SDI typically contains specific amount of realistic null counterpart of the empirical SDI.
    (See surrogate module in NiGSP for more details)

    Create a distribution of test statistics out of the empirical and surrogate SDIs using Wilcoxon signed rank test.
    This distribution shows the strength of the observed SDI compared to the surrogate SDIs

    b)
    First level: Checks for the consistency of the effects over trials / epochs / events, extended for all the subjects individually
    Uses the test statistics from the previous step to test for the effect using parametric one-sample t-test.
    (See mne.stats.ttest_1samp_no_p for more details. https://mne.tools/stable/generated/mne.stats.ttest_1samp_no_p.html)

    c)
    Second level: Stat test for the effect over subjects.
    Use the test statistics from the first level and perform 2nd level modeling using massive univariate tests
    and permutation-based correction for multiple comparisons. Ref: https://doi.org/10.1002/hbm.1058 /

    Parameters
    ----------
    empirical_SDI: Array of shape (n_events, n_subjects, n_roi)
        SDI values for the empirical data
    surrogate_SDI: Array of shape (n_events, n_surrogate, n_subjects, n_roi)
        SDI values for the surrogate data
    output_dir_first_level: str, optional
        Directory to save the test statistics from the first level
    output_dir_second_level: str, optional
        Directory to save the test statistics from the second level
    n_perms: int, optional
        Number of permutations for the second level modeling
    n_jobs: int, optional
        Number of jobs to run in parallel for the second level modeling

    Returns
    -------
    test_stats_second_level: Array of shape (n_events, n_roi)
        Final test statistics tested for consistency across and within subjects with subsequent permutation-based
        correction for multiple comparisons. It reveals the ROIs that are significantly consistent across and within subjects.
    """
    try:
        from mne.stats import permutation_t_test
    except ImportError:
        raise ImportError(
            "MNE-python is required to run this function",
            "Please see installation instructions",
        )

    if empirical_SDI.ndim != 3 or surrogate_SDI.ndim != 4:
        raise NotImplementedError(
            "Please check the shape of both of the input arrays, they should be of shape (n_events, n_subjects, n_roi) and (n_events, n_surrogate, n_subjects, n_roi) respectively"
        )

    n_events, n_surrogate, n_subjects, n_roi = np.shape(surrogate_SDI)
    assert np.shape(empirical_SDI) == (
        n_events,
        n_subjects,
        n_roi,
    ), "Mismatch with empirical SDI; please input the right empirical and surrogate SDI pair"

    # Step 1: Signed rank test
    # a) Get the difference between the empirical and surrogate SDIs
    diff = empirical_SDI - np.moveaxis(surrogate_SDI, [0, 1, 2, 3], [1, 0, 2, 3])

    # b) Wilcoxon Test - A non-parametric test
    # c) Normalization by the number of surrogates to avoid inflating the test statistics by the number of surrogates
    LGR.info("Calculating test statistics using Wilcoxon signed rank test")
    test_stats_signed_rank_test = (
        np.sum(ranktest(np.abs(diff), axis=0) * np.sign(diff), axis=0) / n_surrogate
    )

    # test statistics summarizing for the trials, subjects and for the ROIs
    assert test_stats_signed_rank_test.shape == (n_events, n_subjects, n_roi)

    # Two-level modeling begins
    # Step 2: First level Model
    LGR.info("Performing First-level tests")
    test_stats_first_level = ttest_1samp_no_p(test_stats_signed_rank_test)

    # During testing on a real data, it was observed that test statistics sporadically yielded infinite values at a rate of <0.02%.

    # Occurs at the step above: This issue arises when each value in the differenced population receives a unique rank, leading to a summation
    # equivalent to n(n+1)/2, where n represents the number of surrogates. If this unique rank assignment is consistent
    # across multiple events, every event ends up having the same summed rank. Consequently, during first-level statistical calculations,
    # the population effectively becomes a single value distributed across all observations. This situation results in
    # the test statistic being infinitely distant from 0.

    # A simple workaround is to consider them as not significant and set them to 0.
    test_stats_first_level[np.where(test_stats_first_level == np.inf)] = 0
    test_stats_first_level[np.where(test_stats_first_level == -np.inf)] = 0

    if output_dir_first_level is not None:
        np.savez_compressed(
            f"{output_dir_first_level}/test_stats_first_level.npz",
            test_stats_first_level=test_stats_first_level,
        )

    # Step 3 : Second level Model
    LGR.info("Performing Second-level tests")
    test_stats_second_level, _, _ = permutation_t_test(
        test_stats_first_level, n_jobs=n_jobs, n_permutations=n_perms
    )
    if output_dir_second_level is not None:
        np.savez_compressed(
            f"{output_dir_second_level}/test_stats_second_level.npz",
            test_stats_second_level=test_stats_second_level,
        )
    return test_stats_second_level
