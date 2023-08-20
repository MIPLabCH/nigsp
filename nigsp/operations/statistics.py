import logging

import numpy as np
from mne.stats import permutation_t_test

LGR = logging.getLogger(__name__)


def ranktest(a, axis=None):
    # Code adapted from `scipy`; ref: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rankdata.html

    """Assign ranks to data, dealing with ties appropriately.

    By default (``axis=None``), the data array is first flattened, and a flat
    array of ranks is returned. Separately reshape the rank array to the
    shape of the data array if desired (see Examples).

    Ranks begin at 1.  The `method` argument controls how ranks are assigned
    to equal values.  See [1]_ for further discussion of ranking methods.

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
    """

    if axis is not None:
        a = np.asarray(a)
        if a.size == 0:
            # The return values of `normalize_axis_index` are ignored.  The
            # call validates `axis`, even though we won't use it.
            # use scipy._lib._util._normalize_axis_index when available
            np.core.multiarray.normalize_axis_index(axis, a.ndim)
            return np.empty(a.shape, dtype=np.float64)
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


class onesamplettest:
    # Code adapted from `mne-python`; ref: https://mne.tools/stable/generated/mne.stats.ttest_1samp_no_p.html
    def _check_option(parameter, value, allowed_values, extra=""):
        """Check the value of a parameter against a list of valid options.

        Return the value if it is valid, otherwise raise a ValueError with a
        readable error message.

        Parameters
        ----------
        parameter : str
            The name of the parameter to check. This is used in the error message.
        value : any type
            The value of the parameter to check.
        allowed_values : list
            The list of allowed values for the parameter.
        extra : str
            Extra string to append to the invalid value sentence, e.g.
            "when using ico mode".

        Raises
        ------
        ValueError
            When the value of the parameter is not one of the valid options.

        Returns
        -------
        value : any type
            The value if it is valid.
        """
        if value in allowed_values:
            return value

        # Prepare a nice error message for the user
        extra = f" {extra}" if extra else extra
        msg = (
            "Invalid value for the '{parameter}' parameter{extra}. "
            "{options}, but got {value!r} instead."
        )
        allowed_values = list(allowed_values)  # e.g., if a dict was given
        if len(allowed_values) == 1:
            options = f"The only allowed value is {repr(allowed_values[0])}"
        else:
            options = "Allowed values are "
            if len(allowed_values) == 2:
                options += " and ".join(repr(v) for v in allowed_values)
            else:
                options += ", ".join(repr(v) for v in allowed_values[:-1])
                options += f", and {repr(allowed_values[-1])}"
        raise ValueError(
            msg.format(parameter=parameter, options=options, value=value, extra=extra)
        )

    def _ttest_1samp_no_p(X, axis=0, sigma=0, method="relative"):
        """Perform one-sample t-test.

        This is a modified version of :func:`scipy.stats.ttest_1samp` that avoids
        a (relatively) time-consuming p-value calculation, and can adjust
        for implausibly small variance values: https://doi.org/10.1016/j.neuroimage.2011.10.027.

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
        method : str
            If 'relative', the minimum variance estimate will be sigma * max(var),
            if 'absolute' the minimum variance estimate will be sigma.

        Returns
        -------
        t : array
            T-values, potentially adjusted using the hat method.

        Notes
        -----
        To use the "hat" adjustment method :footcite:`RidgwayEtAl2012`, a value
        of ``sigma=1e-3`` may be a reasonable choice.
        """
        onesamplettest._check_option("method", method, ["absolute", "relative"])
        var = np.var(X, axis=axis, ddof=1)
        if sigma > 0:
            limit = sigma * np.max(var) if method == "relative" else sigma
            var += limit
        return np.mean(X, axis=0) / np.sqrt(var / X.shape[0])


def stats(
    empirical_SDI,
    surrogate_SDI,
    output_dir_first_level=None,
    output_dir_second_level=None,
    n_perms=1000,
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
    Use the test statistics from the previous step to test for the effect using parametric one-sample t-test.
    (See mne.stats.ttest_1samp_no_p for more details. https://mne.tools/stable/generated/mne.stats.ttest_1samp_no_p.html)

    c)
    Second level: Stat test for the effect over subjects.
    Use the test statistics from the first level and perform 2nd level modeling using massive univariate tests.
    and permutation-based correction for multiple comparisons.

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

    Returns
    -------
    test_stats_second_level: Array of shape (n_events, n_roi)
        Final test statistics tested for consistency across and within subjects with subsequent permutation-based
        correction for multiple comparisons. It reveals the ROIs that are significantly consistent across and within subjects.
    """
    if empirical_SDI.ndim > 3 or surrogate_SDI.ndim > 4:
        raise ValueError(
            "Please check the shape of both of the input arrays, they should be of shape (n_events, n_subjects, n_roi) and (n_events, n_surrogate, n_subjects, n_roi) respectively"
        )

    n_events, n_surrogate, n_subjects, n_roi = np.shape(surrogate_SDI)
    assert np.shape(empirical_SDI) == (
        n_events,
        n_subjects,
        n_roi,
    ), "Mismatch with empirical SDI; please input the right empirical and surrogate SDI pair"

    # Step 1: Signed rank test
    # a) get the difference between the empirical and surrogate SDIs
    diff = empirical_SDI - np.moveaxis(surrogate_SDI, [0, 1, 2, 3], [1, 0, 2, 3])

    # b) Signed Wilcoxon Test - A non-parametric test
    # c) Sum the ranks
    # d) Normalize it by the number of surrogates to avoid inflating the test statistics by the number of surrogates
    LGR.info("Calculating test statistics using Wilcoxon signed rank test")
    test_stats_signed_rank_test = (
        np.sum(ranktest(np.abs(diff), axis=0) * np.sign(diff), axis=0) / n_surrogate
    )

    # test statistics summarizing for the trials, subjects and for the ROIs
    assert test_stats_signed_rank_test.shape == (n_events, n_subjects, n_roi)

    # Two-level modeling begins
    # Step 2: First level Model
    LGR.info("Performing First-level tests")
    test_stats_first_level = onesamplettest._ttest_1samp_no_p(
        test_stats_signed_rank_test
    )

    # During testing on the data, it was observed that test statistics occasionally yielded infinite values, occurring at a rate of <0.02%.

    # Occurs at the step above: This issue arises when each value in the differenced population receives a unique rank, leading to a summation
    # equivalent to n(n+1)/2, where n represents the number of elements (N) in the dataset. If this unique rank assignment is consistent
    # across multiple events, every event ends up having the same summed rank. Consequently, during first-level statistical calculations,
    # the population effectively becomes a single value distributed across all observations. This situation results in scipy indicating that
    # the test statistic is infinitely distant from 0.

    # A simple workaround is to consider them is not significant and set them to 0.
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
        test_stats_first_level, n_jobs=-1, n_permutations=n_perms
    )
    if output_dir_second_level is not None:
        np.savez_compressed(
            f"{output_dir_second_level}/test_stats_second_level.npz",
            test_stats_second_level=test_stats_second_level,
        )
    return test_stats_second_level
