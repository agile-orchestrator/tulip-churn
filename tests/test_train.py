import json
import math

import joblib
import pytest

from tulip_churn import api
from tulip_churn.data import load_data
from tulip_churn.features import FEATURES, add_features
from tulip_churn.train import GROUPS, TrainConfig, fit_and_evaluate, main, train

# Small model so the tests stay fast.
FAST = TrainConfig(n_estimators=10, max_depth=2)


@pytest.fixture(scope="module")
def trained(raw_csv, tmp_path_factory):
    out = tmp_path_factory.mktemp("models")
    metrics = train(FAST, data=raw_csv, out_dir=out)
    return out, metrics


def test_train_saves_a_model_that_scores(trained, raw_csv):
    out, _ = trained
    model = joblib.load(out / "model.joblib")
    df = add_features(load_data(raw_csv).head(5))
    proba = model.predict_proba(df[FEATURES])[:, 1]
    assert ((proba >= 0) & (proba <= 1)).all()


def test_metrics_json_matches_returned_metrics(trained):
    out, metrics = trained
    assert json.loads((out / "metrics.json").read_text()) == metrics


def test_metrics_json_has_what_the_model_card_needs(trained):
    _, metrics = trained
    assert metrics["params"] == {
        "seed": 42, "test_size": 0.2, "n_estimators": 10, "max_depth": 2, "learning_rate": 0.1
    }
    assert metrics["features"] == FEATURES
    assert metrics["threshold"] == api.THRESHOLD
    assert metrics["data"]["train_rows"] + metrics["data"]["test_rows"] == metrics["data"]["rows"]
    assert set(metrics["test"]) >= {"roc_auc", "precision", "recall", "f1"}
    assert set(metrics["by_group"]) == set(GROUPS)
    for group in metrics["by_group"].values():
        assert sum(scores["n"] for scores in group.values()) == metrics["data"]["test_rows"]


def test_same_seed_gives_same_metrics(raw_csv):
    df = load_data(raw_csv)
    _, first = fit_and_evaluate(df, FAST)
    _, second = fit_and_evaluate(df, FAST)
    assert first == second


def test_seed_changes_the_split(raw_csv):
    df = load_data(raw_csv)
    _, a = fit_and_evaluate(df, FAST)
    _, b = fit_and_evaluate(df, TrainConfig(seed=1, n_estimators=10, max_depth=2))
    assert a["test"] != b["test"]


def test_hyperparameters_reach_the_model(raw_csv):
    config = TrainConfig(n_estimators=7, max_depth=4, learning_rate=0.3)
    model, _ = fit_and_evaluate(load_data(raw_csv), config)
    params = model.named_steps["clf"].get_params()
    assert (params["n_estimators"], params["max_depth"], params["learning_rate"]) == (7, 4, 0.3)
    assert params["random_state"] == config.seed


def test_cli_passes_options_through(raw_csv, tmp_path):
    main(["--data", str(raw_csv), "--out-dir", str(tmp_path), "--seed", "3",
          "--test-size", "0.25", "--n-estimators", "5", "--max-depth", "2"])
    metrics = json.loads((tmp_path / "metrics.json").read_text())
    assert metrics["params"] == {
        "seed": 3, "test_size": 0.25, "n_estimators": 5, "max_depth": 2, "learning_rate": 0.1
    }
    assert metrics["data"]["test_rows"] == math.ceil(0.25 * metrics["data"]["rows"])
    assert (tmp_path / "model.joblib").exists()
