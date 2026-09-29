"""Train the churn model and save it with its metrics.

Usage: uv run python -m tulip_churn.train [--seed 42] [--n-estimators 200] ...
Run with --help for all options. Writes models/model.joblib and models/metrics.json.
"""

import argparse
import json
import subprocess
from dataclasses import asdict, dataclass, fields
from datetime import UTC, datetime
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from tulip_churn import __version__
from tulip_churn.data import TARGET, data_path, load_data, split
from tulip_churn.evaluate import THRESHOLD, evaluate
from tulip_churn.features import CATEGORICAL, FEATURES, NUMERIC, add_features

REPO = Path(__file__).resolve().parents[2]
MODELS_DIR = REPO / "models"
GROUPS = ["Gender", "AgeBand", "Geography"]


@dataclass(frozen=True)
class TrainConfig:
    seed: int = 42
    test_size: float = 0.2
    n_estimators: int = 200
    max_depth: int = 3
    learning_rate: float = 0.1


def build_model(config: TrainConfig) -> Pipeline:
    pre = ColumnTransformer(
        [
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
            ("num", StandardScaler(), NUMERIC),
        ]
    )
    clf = GradientBoostingClassifier(
        n_estimators=config.n_estimators,
        max_depth=config.max_depth,
        learning_rate=config.learning_rate,
        random_state=config.seed,
    )
    return Pipeline([("pre", pre), ("clf", clf)])


def _scores(y_true: pd.Series, y_proba) -> dict[str, float]:
    scores = {"n": len(y_true), "churn_rate": round(float(y_true.mean()), 4)}
    if y_true.nunique() < 2:  # ROC AUC is undefined for a single class
        return scores
    return scores | {k: round(float(v), 4) for k, v in evaluate(y_true, y_proba, THRESHOLD).items()}


def fit_and_evaluate(df: pd.DataFrame, config: TrainConfig) -> tuple[Pipeline, dict]:
    """Fit on a train split of the cleaned data and score the hold-out, overall and by group."""
    df = add_features(df)
    train_df, test_df = split(df, test_size=config.test_size, seed=config.seed)
    model = build_model(config).fit(train_df[FEATURES], train_df[TARGET])
    proba = pd.Series(model.predict_proba(test_df[FEATURES])[:, 1], index=test_df.index)

    metrics = {
        "algorithm": type(model.named_steps["clf"]).__name__,
        "params": asdict(config),
        "features": FEATURES,
        "threshold": THRESHOLD,
        "data": {
            "rows": len(df),
            "churn_rate": round(float(df[TARGET].mean()), 4),
            "train_rows": len(train_df),
            "test_rows": len(test_df),
        },
        "test": _scores(test_df[TARGET], proba),
        "by_group": {
            group: {
                str(value): _scores(rows[TARGET], proba[rows.index])
                for value, rows in test_df.groupby(group)
            }
            for group in GROUPS
        },
    }
    return model, metrics


def _git(*args: str) -> str | None:
    try:
        out = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return out.stdout.strip()


def train(
    config: TrainConfig | None = None,
    data: str | Path | None = None,
    out_dir: str | Path = MODELS_DIR,
) -> dict:
    """Train, then write model.joblib and metrics.json to out_dir. Returns the metrics."""
    source = Path(data) if data else data_path()
    model, metrics = fit_and_evaluate(load_data(source), config or TrainConfig())

    status = _git("status", "--porcelain")
    metrics = {
        "trained_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "package_version": __version__,
        "sklearn_version": sklearn.__version__,
        "git_commit": _git("rev-parse", "HEAD"),
        "git_dirty": None if status is None else status != "",
        "data_path": str(source),
    } | metrics

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out_dir / "model.joblib")
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    return metrics


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m tulip_churn.train",
        description="Train the churn model and save it with its metrics.",
    )
    parser.add_argument("--data", help="raw CSV (default: $TULIP_DATA_PATH, else data/raw/)")
    parser.add_argument("--out-dir", default=MODELS_DIR, help="default: models/ in the repo")
    for f in fields(TrainConfig):
        flag, default = "--" + f.name.replace("_", "-"), f.default
        parser.add_argument(flag, type=type(default), default=default, help=f"default: {default}")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    config = TrainConfig(**{f.name: getattr(args, f.name) for f in fields(TrainConfig)})
    metrics = train(config, data=args.data, out_dir=args.out_dir)
    print(json.dumps(metrics["test"], indent=2))
    print(f"Saved model and metrics to {Path(args.out_dir)}")


if __name__ == "__main__":
    main()
