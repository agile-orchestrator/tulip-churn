import joblib
import pytest
from fastapi.testclient import TestClient
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from tulip_churn import api
from tulip_churn.data import clean
from tulip_churn.features import CATEGORICAL, FEATURES, NUMERIC, add_features

CUSTOMER = {
    "CreditScore": 619,
    "Geography": "France",
    "Gender": "Female",
    "Age": 42,
    "Tenure": 2,
    "Balance": 0.0,
    "NumOfProducts": 1,
    "HasCrCard": 1,
    "IsActiveMember": 1,
    "EstimatedSalary": 101348.88,
}


@pytest.fixture(scope="module")
def client(tmp_path_factory, raw_df):
    df = add_features(clean(raw_df))
    model = make_pipeline(
        ColumnTransformer(
            [("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
             ("num", StandardScaler(), NUMERIC)]
        ),
        LogisticRegression(max_iter=1000),
    ).fit(df[FEATURES], df["Exited"])
    path = tmp_path_factory.mktemp("models") / "model.joblib"
    joblib.dump(model, path)

    api.MODEL_PATH = str(path)
    api.get_model.cache_clear()
    return TestClient(api.app)


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_score_returns_probability(client):
    body = client.post("/score", json=CUSTOMER).json()
    assert 0.0 <= body["churn_probability"] <= 1.0
    assert isinstance(body["at_risk"], bool)
