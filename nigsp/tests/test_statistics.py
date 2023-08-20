# %%
import numpy as np
from numpy.random import default_rng, rand
from pytest import raises

import nigsp.operations as ops
from nigsp.operations.statistics import stats


# ### Unit tests
def test_stats():
    # Set up zero everywhere except specific roi, aka = signal on the other rois are equivalent to noise
    # Tests specifically at the rois having signal
    n_events = 30
    n_surrogates = 40
    n_roi = 360
    n_subs = 20
    empi_data = np.zeros((n_events, n_subs, n_roi))
    surr_data = np.zeros((n_events, n_surrogates, n_subs, n_roi))

    rois = np.random.randint(0, n_roi, 10)

    for roi in rois:
        random_empi = np.random.rand(n_events * n_subs)
        random_surr = np.random.rand(n_events * n_surrogates * n_subs)
        empi_data[:, :, roi] = random_empi.reshape(n_events, n_subs)
        surr_data[:, :, :, roi] = random_surr.reshape(n_events, n_surrogates, n_subs)
    n_perms = 200
    second_level_stats = stats(empi_data, surr_data, n_perms=n_perms)

    assert second_level_stats.shape == (n_roi,)  # do we get tstats for each roi?
    assert (
        second_level_stats[rois] != 0
    ).all()  # do we get tstats for predefined rois?
    assert np.isnan(second_level_stats).sum() == n_roi - len(
        rois
    )  # do we get nan for the rest of the rois?


# ### Break tests
# def break_test_stats():
#     # Break
#     n_events = 30
#     n_surrogates = 40
#     n_roi = 360
#     n_subs = 20
#     empi_data = np.zeros(( n_subs, n_roi))
#     surr_data = np.zeros((n_events, n_subs, n_roi))

#     # ops.statistics.stats(empi_data, surr_data, n_perms=200)

#     with raises(NotImplementedError) as errorinfo:
#         ops.statistics.stats(rand(2, 3, 4, 5), rand(2, 3, 4, 5), n_perms=200)
#         assert "has 4 dimensions" in str(errorinfo.value)
