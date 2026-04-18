import logging

import pandas as pd
import pytest

from src.main import compute_statistics, load_and_clean_data, validate_dataframe


def test_load_returns_dataframe(mock_data_dir):
    df = load_and_clean_data(mock_data_dir)
    assert isinstance(df, pd.DataFrame)


def test_load_has_required_columns(mock_data_dir):
    df = load_and_clean_data(mock_data_dir)
    assert {"year", "inflation", "unemployment", "poverty"}.issubset(df.columns)


def test_load_filters_to_1990_onwards(mock_data_dir):
    df = load_and_clean_data(mock_data_dir)
    assert df["year"].min() >= 1990


def test_load_values_are_numeric(mock_data_dir):
    df = load_and_clean_data(mock_data_dir)
    for col in ["inflation", "unemployment", "poverty"]:
        assert pd.api.types.is_numeric_dtype(df[col])


def test_load_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_and_clean_data(tmp_path)


def test_compute_statistics_returns_dataframe(mock_data_dir):
    df = load_and_clean_data(mock_data_dir)
    result = compute_statistics(df)
    assert isinstance(result, pd.DataFrame)


def test_compute_statistics_has_expected_columns(mock_data_dir):
    df = load_and_clean_data(mock_data_dir)
    result = compute_statistics(df)
    assert {"pair", "pearson_r", "pearson_p", "spearman_r", "spearman_p"}.issubset(
        result.columns
    )


def test_compute_statistics_three_pairs(mock_data_dir):
    df = load_and_clean_data(mock_data_dir)
    result = compute_statistics(df)
    assert len(result) == 3


def test_compute_statistics_pearson_r_in_range(mock_data_dir):
    df = load_and_clean_data(mock_data_dir)
    result = compute_statistics(df)
    assert result["pearson_r"].between(-1, 1).all()


def test_validate_warns_on_negative_unemployment(caplog):
    df = pd.DataFrame(
        {
            "year": [1990, 1991],
            "inflation": [10.0, 20.0],
            "unemployment": [-1.0, 5.0],
            "poverty": [30.0, 25.0],
        }
    )
    with caplog.at_level(logging.WARNING, logger="src.main"):
        validate_dataframe(df)
    assert "Negative unemployment" in caplog.text


def test_validate_warns_on_negative_poverty(caplog):
    df = pd.DataFrame(
        {
            "year": [1990, 1991],
            "inflation": [10.0, 20.0],
            "unemployment": [5.0, 6.0],
            "poverty": [-5.0, 25.0],
        }
    )
    with caplog.at_level(logging.WARNING, logger="src.main"):
        validate_dataframe(df)
    assert "Negative poverty" in caplog.text


def test_validate_warns_on_missing_values(caplog):
    df = pd.DataFrame(
        {
            "year": [1990, 1991],
            "inflation": [10.0, None],
            "unemployment": [5.0, 6.0],
            "poverty": [30.0, 25.0],
        }
    )
    with caplog.at_level(logging.WARNING, logger="src.main"):
        validate_dataframe(df)
    assert "Missing values" in caplog.text
