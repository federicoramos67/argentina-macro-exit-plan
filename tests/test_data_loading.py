import pandas as pd
import pytest

from src.main import reshape_wb_indicator


def test_reshape_returns_dataframe(wb_csv_file):
    df = reshape_wb_indicator(wb_csv_file, "test_value")
    assert isinstance(df, pd.DataFrame)


def test_reshape_has_correct_columns(wb_csv_file):
    df = reshape_wb_indicator(wb_csv_file, "test_value")
    assert "year" in df.columns
    assert "test_value" in df.columns


def test_reshape_year_is_int(wb_csv_file):
    df = reshape_wb_indicator(wb_csv_file, "test_value")
    assert df["year"].dtype == int


def test_reshape_values_are_numeric(wb_csv_file):
    df = reshape_wb_indicator(wb_csv_file, "test_value")
    assert pd.api.types.is_float_dtype(df["test_value"])


def test_reshape_filters_argentina_only(wb_csv_file):
    df = reshape_wb_indicator(wb_csv_file, "test_value")
    assert len(df) == 3
    assert set(df["year"]) == {1990, 1991, 1992}


def test_reshape_correct_value_for_year(wb_csv_file):
    df = reshape_wb_indicator(wb_csv_file, "test_value")
    row_1990 = df.loc[df["year"] == 1990, "test_value"].iloc[0]
    assert abs(row_1990 - 10.5) < 0.01


def test_reshape_file_not_found_raises():
    with pytest.raises(FileNotFoundError, match="Data file not found"):
        reshape_wb_indicator("/nonexistent/path/data.csv", "test")


def test_reshape_missing_country_code_column_raises(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("\n\n\n\nCountry Name,Indicator Code,1990\nArgentina,TEST,10\n")
    with pytest.raises(ValueError, match="Expected 'Country Code' column"):
        reshape_wb_indicator(bad_csv, "test")


def test_reshape_no_arg_data_raises(tmp_path):
    no_arg_csv = tmp_path / "no_arg.csv"
    no_arg_csv.write_text(
        "\n\n\n\nCountry Name,Country Code,Indicator Name,Indicator Code,1990\n"
        "Brazil,BRA,Test,T,5.0\n"
    )
    with pytest.raises(ValueError, match="No Argentina"):
        reshape_wb_indicator(no_arg_csv, "test")
