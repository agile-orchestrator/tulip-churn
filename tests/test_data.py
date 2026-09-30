from pathlib import Path

from tulip_churn.data import ID_COLUMNS, data_path, load_data, split


def test_load_data_drops_id_columns(raw_csv):
    df = load_data(raw_csv)
    assert not set(ID_COLUMNS) & set(df.columns)


def test_load_data_has_no_missing_values(raw_csv):
    df = load_data(raw_csv)
    assert df.isna().sum().sum() == 0


def test_split_sizes(raw_csv):
    df = load_data(raw_csv)
    train, test = split(df, test_size=0.2)
    assert len(train) + len(test) == len(df)
    assert abs(len(test) / len(df) - 0.2) < 0.01


def test_split_keeps_churn_rate(raw_csv):
    df = load_data(raw_csv)
    train, test = split(df)
    assert abs(train["Exited"].mean() - test["Exited"].mean()) < 0.02


def test_default_data_path_is_inside_the_repo(monkeypatch):
    monkeypatch.delenv("TULIP_DATA_PATH", raising=False)
    repo = Path(__file__).resolve().parents[1]
    assert data_path() == repo / "data" / "raw" / "Churn_Modelling.csv"


def test_data_path_can_be_overridden(monkeypatch, raw_df, tmp_path):
    csv = tmp_path / "other.csv"
    raw_df.head(100).to_csv(csv, index=False)
    monkeypatch.setenv("TULIP_DATA_PATH", str(csv))
    assert len(load_data()) == 100


def test_split_stratified_maintains_churn_rate_tightly(raw_csv):
    """Stratified split should maintain very close churn rates in train and test."""
    df = load_data(raw_csv)
    train, test = split(df, seed=42)
    # With stratification, churn rates should be very close (within rounding)
    # Much tighter than the original 0.02 tolerance
    assert abs(train["Exited"].mean() - test["Exited"].mean()) < 0.001
