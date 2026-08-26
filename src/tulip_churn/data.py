"""Load and clean the raw customer extract."""

import pandas as pd
from sklearn.model_selection import train_test_split

DATA_PATH = "/home/cedric/repos/innovation-challenge/tulip-churn/data/raw/Churn_Modelling.csv"

ID_COLUMNS = ["RowNumber", "CustomerId", "Surname"]
TARGET = "Exited"


def load_raw(path: str = DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(columns=[c for c in ID_COLUMNS if c in df.columns])
    df = df.drop_duplicates()
    df = df.dropna()
    df["Geography"] = df["Geography"].str.strip().str.title()
    df["Gender"] = df["Gender"].str.strip().str.title()
    return df


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    return clean(load_raw(path))


def split(df: pd.DataFrame, test_size: float = 0.2, seed: int | None = None):
    return train_test_split(df, test_size=test_size, random_state=seed)
