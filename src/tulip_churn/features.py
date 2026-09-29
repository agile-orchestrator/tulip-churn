"""Feature engineering shared by training and scoring."""

import pandas as pd

CATEGORICAL = ["Geography", "Gender", "AgeBand"]
NUMERIC = [
    "CreditScore",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary",
    "BalanceToSalary",
    "ZeroBalance",
]
FEATURES = CATEGORICAL + NUMERIC


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["BalanceToSalary"] = df["Balance"] / df["EstimatedSalary"].clip(lower=1)
    df["ZeroBalance"] = (df["Balance"] == 0).astype(int)
    df["AgeBand"] = pd.cut(
        df["Age"], bins=[0, 30, 40, 50, 60, 120], labels=["<30", "30-39", "40-49", "50-59", "60+"]
    ).astype(str)
    return df
