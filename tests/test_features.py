import pandas as pd

from tulip_churn.features import FEATURES, add_features


def test_features_do_not_depend_on_target(raw_df):
    with_target = add_features(raw_df)
    without_target = add_features(raw_df.drop(columns=["Exited"]))
    pd.testing.assert_frame_equal(
        with_target[FEATURES].reset_index(drop=True),
        without_target[FEATURES].reset_index(drop=True),
    )


def test_flipping_target_leaves_features_unchanged(raw_df):
    flipped = raw_df.assign(Exited=1 - raw_df["Exited"])
    pd.testing.assert_frame_equal(add_features(raw_df)[FEATURES], add_features(flipped)[FEATURES])
