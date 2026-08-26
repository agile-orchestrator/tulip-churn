import pytest

from tulip_churn.synthetic import generate


@pytest.fixture(scope="session")
def raw_df():
    return generate(n=10_000, seed=7)


@pytest.fixture(scope="session")
def raw_csv(tmp_path_factory, raw_df):
    path = tmp_path_factory.mktemp("data") / "Churn_Modelling.csv"
    raw_df.to_csv(path, index=False)
    return path
