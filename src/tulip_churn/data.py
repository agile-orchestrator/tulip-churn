"""Load and clean the raw customer extract."""

import os
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

DEFAULT_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "raw" / "Churn_Modelling.csv"

ID_COLUMNS = ["RowNumber", "CustomerId", "Surname"]
TARGET = "Exited"


def data_path() -> Path:
    """The raw extract: $TULIP_DATA_PATH if set, else data/raw/ in the repo."""
    return Path(os.environ.get("TULIP_DATA_PATH", DEFAULT_DATA_PATH))


def load_raw(path: str | Path | None = None) -> pd.DataFrame:
    return pd.read_csv(path or data_path())


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(columns=[c for c in ID_COLUMNS if c in df.columns])
    df = df.drop_duplicates()
    df = df.dropna()
    df["Geography"] = df["Geography"].str.strip().str.title()
    df["Gender"] = df["Gender"].str.strip().str.title()
    return df


def load_data(path: str | Path | None = None) -> pd.DataFrame:
    return clean(load_raw(path))


def split(df: pd.DataFrame, test_size: float = 0.2, seed: int | None = None):
    return train_test_split(df, test_size=test_size, random_state=seed, stratify=df[TARGET])
