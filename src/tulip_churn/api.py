"""Scoring API: POST /score returns the churn probability for one customer."""

from functools import lru_cache
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from tulip_churn.evaluate import THRESHOLD
from tulip_churn.features import FEATURES, add_features

MODEL_PATH = "models/model.joblib"

app = FastAPI(title="Tulip Bank churn scoring", version="0.1.0")


class Customer(BaseModel):
    CreditScore: int
    Geography: Literal["France", "Germany", "Spain"]
    Gender: Literal["Male", "Female"]
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float


class Score(BaseModel):
    churn_probability: float
    at_risk: bool


@lru_cache
def get_model():
    return joblib.load(MODEL_PATH)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/score")
def score(customer: Customer) -> Score:
    df = add_features(pd.DataFrame([customer.model_dump()]))
    proba = float(get_model().predict_proba(df[FEATURES])[0, 1])
    return Score(churn_probability=round(proba, 4), at_risk=proba >= THRESHOLD)
