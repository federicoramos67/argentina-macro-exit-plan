import textwrap

import pytest


@pytest.fixture
def wb_csv_content() -> str:
    """World Bank CSV with ARG and BRA rows for years 1990–1992."""
    return textwrap.dedent(
        """\
        Data Source,World Bank,,,,
        Last Updated Date,2024-01-01,,,,
        ,,,,
        ,,,,
        Country Name,Country Code,Indicator Name,Indicator Code,1990,1991,1992
        Argentina,ARG,Test Indicator,TEST.IND,10.5,20.3,30.1
        Brazil,BRA,Test Indicator,TEST.IND,5.0,6.0,7.0
        """
    )


@pytest.fixture
def wb_csv_file(tmp_path, wb_csv_content):
    """Write WB CSV to a temp file and return its path."""
    f = tmp_path / "test_indicator.csv"
    f.write_text(wb_csv_content)
    return f


@pytest.fixture
def mock_data_dir(tmp_path):
    """Create a temp data directory with all three indicator CSVs."""

    def make_csv(filename: str, v1990: float, v1991: float, v1992: float) -> None:
        content = textwrap.dedent(
            f"""\
            Data Source,World Bank,,,,
            Last Updated Date,2024-01-01,,,,
            ,,,,
            ,,,,
            Country Name,Country Code,Indicator Name,Indicator Code,1990,1991,1992
            Argentina,ARG,Indicator,IND,{v1990},{v1991},{v1992}
            """
        )
        (tmp_path / filename).write_text(content)

    make_csv("inflation_ar.csv", 1344.0, 84.0, 17.5)
    make_csv("unemployment_ar.csv", 7.5, 6.5, 7.0)
    make_csv("poverty_ar.csv", 33.0, 25.0, 20.0)
    return tmp_path
