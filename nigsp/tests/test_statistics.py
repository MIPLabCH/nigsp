# %%
import numpy as np
from numpy.random import rand
from pytest import raises

from nigsp.operations.statistics import two_level_statistical_model


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
    n_perms = 50
    second_level_stats = two_level_statistical_model(
        empi_data,
        surr_data,
        n_perms=n_perms,
        output_dir_first_level="/tmp",
        output_dir_second_level="/tmp",
    )

    assert second_level_stats.shape == (n_roi,)  # do we get tstats for each roi?
    assert (
        second_level_stats[rois] != 0
    ).all()  # do we get tstats for predefined rois?
    assert np.isnan(second_level_stats).sum() == n_roi - len(
        rois
    )  # do we get nan for the rest of the rois?

    # Stability test
    second_level_stats_repeat = two_level_statistical_model(
        empi_data, surr_data, n_perms=200
    )
    assert np.isclose(second_level_stats[rois], second_level_stats_repeat[rois]).all()


### Break tests
def break_test_stats():
    with raises(NotImplementedError) as errorinfo:
        two_level_statistical_model(rand(2), rand(2, 3, 4, 5), n_perms=200)
    assert "check the shape of both the input" in str(errorinfo.value)
