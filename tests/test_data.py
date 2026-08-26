from tulip_churn.data import ID_COLUMNS, load_data, split


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
