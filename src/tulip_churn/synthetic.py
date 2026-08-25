"""Synthetic stand-in for the Kaggle "Churn Modelling" dataset.

Same columns and roughly the same distributions, so the code works with either source.
"""

import numpy as np
import pandas as pd

SURNAMES = [
    "Janssens", "Peeters", "Maes", "Jacobs", "Mertens", "Willems", "Claes", "Goossens",
    "Wouters", "De Smet", "Dubois", "Lambert", "Martin", "Garcia", "Lopez", "Muller",
    "Schmidt", "Schneider", "Fischer", "Weber", "Rossi", "Bernard", "Moreau", "Laurent",
]


def generate(n: int = 10_000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    geography = rng.choice(["France", "Germany", "Spain"], size=n, p=[0.50, 0.25, 0.25])
    gender = rng.choice(["Male", "Female"], size=n, p=[0.55, 0.45])
    age = np.clip(rng.gamma(shape=9.0, scale=4.3, size=n).round(), 18, 92).astype(int)
    tenure = rng.integers(0, 11, size=n)
    credit_score = np.clip(rng.normal(650, 96, size=n).round(), 350, 850).astype(int)
    has_balance = rng.random(n) > np.where(geography == "Germany", 0.02, 0.45)
    balance = np.where(
        has_balance, np.clip(rng.normal(119_000, 30_000, size=n), 3_000, 250_000), 0.0
    )
    num_products = rng.choice([1, 2, 3, 4], size=n, p=[0.50, 0.46, 0.03, 0.01])
    has_cr_card = (rng.random(n) < 0.70).astype(int)
    is_active = (rng.random(n) < 0.515).astype(int)
    salary = rng.uniform(11, 200_000, size=n).round(2)

    logit = (
        -1.75
        + 0.075 * (age - 38)
        - 0.95 * is_active
        + 0.75 * (geography == "Germany")
        + 0.45 * (gender == "Female")
        + 2.2 * (num_products >= 3)
        - 0.9 * (num_products == 2)
        + 0.0000025 * balance
        - 0.0006 * (credit_score - 650)
    )
    exited = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)

    return pd.DataFrame(
        {
            "RowNumber": np.arange(1, n + 1),
            "CustomerId": rng.choice(np.arange(15_565_000, 15_816_000), size=n, replace=False),
            "Surname": rng.choice(SURNAMES, size=n),
            "CreditScore": credit_score,
            "Geography": geography,
            "Gender": gender,
            "Age": age,
            "Tenure": tenure,
            "Balance": balance.round(2),
            "NumOfProducts": num_products,
            "HasCrCard": has_cr_card,
            "IsActiveMember": is_active,
            "EstimatedSalary": salary,
            "Exited": exited,
        }
    )
