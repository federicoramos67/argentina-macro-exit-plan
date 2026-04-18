from __future__ import annotations

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats

from .config import (
    DATA_DIR,
    END_YEAR,
    GOVERNMENTS,
    MAX_INFLATION_PCT,
    MIN_POVERTY_PCT,
    MIN_UNEMPLOYMENT_PCT,
    REPORTS_DIR,
    START_YEAR,
)

logger = logging.getLogger(__name__)


def reshape_wb_indicator(path_csv: str | Path, value_name: str) -> pd.DataFrame:
    """
    Lee un CSV estándar del Banco Mundial, filtra por Argentina
    y devuelve un DataFrame con las columnas: 'year', value_name.
    """
    path_csv = Path(path_csv)
    if not path_csv.exists():
        raise FileNotFoundError(f"Data file not found: {path_csv}")

    try:
        df_raw = pd.read_csv(path_csv, skiprows=4)
    except Exception as exc:
        raise ValueError(f"Could not read CSV '{path_csv}': {exc}") from exc

    if "Country Code" not in df_raw.columns:
        raise ValueError(f"Expected 'Country Code' column in {path_csv}")

    df_arg = df_raw[df_raw["Country Code"] == "ARG"]
    if df_arg.empty:
        raise ValueError(f"No Argentina (ARG) data found in {path_csv}")

    year_cols = [c for c in df_arg.columns if c.isdigit()]
    df_long = (
        df_arg[year_cols]
        .T.reset_index()
        .rename(columns={"index": "year", df_arg.index[0]: value_name})
    )
    df_long["year"] = df_long["year"].astype(int)
    df_long[value_name] = pd.to_numeric(df_long[value_name], errors="coerce")
    logger.debug("Loaded %d rows for indicator '%s'", len(df_long), value_name)
    return df_long


def validate_dataframe(df: pd.DataFrame) -> None:
    """
    Validates the merged macro DataFrame for expected ranges.
    Issues warnings for anomalies without halting execution.
    """
    if df["inflation"].max() > MAX_INFLATION_PCT:
        logger.warning(
            "Inflation exceeds %.0f%% — max found: %.2f%%",
            MAX_INFLATION_PCT,
            df["inflation"].max(),
        )
    if (df["unemployment"] < MIN_UNEMPLOYMENT_PCT).any():
        logger.warning("Negative unemployment values detected.")
    if (df["poverty"] < MIN_POVERTY_PCT).any():
        logger.warning("Negative poverty values detected.")
    missing = df.isnull().sum()
    if missing.any():
        logger.warning("Missing values detected:\n%s", missing[missing > 0].to_string())


def load_and_clean_data(data_path: str | Path = DATA_DIR) -> pd.DataFrame:
    """
    Carga los tres indicadores macroeconómicos y los consolida
    en un único DataFrame.
    """
    data_path = Path(data_path)
    inflation = reshape_wb_indicator(data_path / "inflation_ar.csv", "inflation")
    unemployment = reshape_wb_indicator(data_path / "unemployment_ar.csv", "unemployment")
    poverty = reshape_wb_indicator(data_path / "poverty_ar.csv", "poverty")

    macro_ar = inflation.merge(unemployment, on="year", how="inner").merge(
        poverty, on="year", how="inner"
    )
    macro_ar = macro_ar[macro_ar["year"] >= START_YEAR].reset_index(drop=True)
    validate_dataframe(macro_ar)
    logger.info(
        "Loaded %d years of macro data (%d–%d)",
        len(macro_ar),
        macro_ar["year"].min(),
        macro_ar["year"].max(),
    )
    return macro_ar


def compute_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes Pearson and Spearman correlations with p-values for each indicator pair.
    """
    cols = ["inflation", "unemployment", "poverty"]
    pairs = [(cols[i], cols[j]) for i in range(len(cols)) for j in range(i + 1, len(cols))]

    records = []
    for a, b in pairs:
        valid = df[[a, b]].dropna()
        pearson_r, pearson_p = stats.pearsonr(valid[a], valid[b])
        spearman_r, spearman_p = stats.spearmanr(valid[a], valid[b])
        records.append(
            {
                "pair": f"{a} vs {b}",
                "pearson_r": round(pearson_r, 3),
                "pearson_p": round(pearson_p, 4),
                "spearman_r": round(spearman_r, 3),
                "spearman_p": round(spearman_p, 4),
            }
        )

    corr_df = pd.DataFrame(records)
    logger.info("Correlation statistics:\n%s", corr_df.to_string(index=False))
    return corr_df


def plot_time_series(df: pd.DataFrame, output_path: str | Path) -> None:
    """
    Genera y guarda un gráfico de series temporales con media móvil de 3 años
    superpuesta en inflación.
    """
    output_path = Path(output_path)
    plt.style.use("seaborn-v0_8")
    sns.set_palette("tab10")
    sns.set_context("talk")

    fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

    sns.lineplot(data=df, x="year", y="inflation", ax=axes[0], label="Anual")
    rolling_inf = df.set_index("year")["inflation"].rolling(3, center=True).mean()
    axes[0].plot(
        rolling_inf.index,
        rolling_inf.values,
        linestyle="--",
        linewidth=1.5,
        label="Media móvil 3a",
    )
    axes[0].set_ylabel("Inflation (%)")
    axes[0].set_title("Argentina: annual inflation")
    axes[0].legend(fontsize=9)

    sns.lineplot(data=df, x="year", y="unemployment", ax=axes[1])
    axes[1].set_ylabel("Unemployment (%)")
    axes[1].set_title("Argentina: unemployment rate")

    sns.lineplot(data=df, x="year", y="poverty", ax=axes[2])
    axes[2].set_ylabel("Poverty (%)")
    axes[2].set_title("Argentina: poverty (national line)")
    axes[2].set_xlabel("Year")

    for ax in axes:
        for start, end, _label, color in GOVERNMENTS:
            ax.axvspan(start, end, color=color, alpha=0.15)

    for start, end, label, _color in GOVERNMENTS:
        mid = (start + end) / 2
        axes[-1].text(
            mid,
            axes[-1].get_ylim()[0],
            label,
            ha="center",
            va="bottom",
            fontsize=8,
            rotation=90,
        )

    axes[-1].set_xlim(1990, 2025)
    axes[-1].set_xticks(range(1990, 2026, 2))

    plt.tight_layout()
    out_file = output_path / "time_series.png"
    plt.savefig(out_file)
    plt.close()
    logger.info("Time series chart saved to %s", out_file)


def plot_correlation_heatmap(df: pd.DataFrame, output_path: str | Path) -> None:
    """
    Calcula y guarda mapas de calor de correlación Pearson y Spearman lado a lado.
    """
    output_path = Path(output_path)
    cols = ["inflation", "unemployment", "poverty"]
    pearson_corr = df[cols].corr(method="pearson")
    spearman_corr = df[cols].corr(method="spearman")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for ax, corr, title, label in [
        (axes[0], pearson_corr, "Pearson correlation", "Pearson r"),
        (axes[1], spearman_corr, "Spearman correlation", "Spearman ρ"),
    ]:
        sns.heatmap(
            corr,
            annot=True,
            cmap="coolwarm",
            fmt=".2f",
            cbar_kws={"label": label},
            ax=ax,
        )
        ax.set_title(title)
        ax.set_yticks(range(len(cols)))
        ax.set_yticklabels(cols, rotation=0)

    fig.suptitle("Correlation: inflation, unemployment and poverty (Argentina)", fontsize=14)
    plt.tight_layout()
    out_file = output_path / "correlation_heatmap.png"
    plt.savefig(out_file)
    plt.close()
    logger.info("Correlation heatmap saved to %s", out_file)


def export_report(df: pd.DataFrame, corr_stats: pd.DataFrame, output_path: str | Path) -> None:
    """
    Exports an HTML report with descriptive statistics and correlation table.
    """
    output_path = Path(output_path)
    desc = df[["inflation", "unemployment", "poverty"]].describe().round(2)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Argentina Macro Report</title>
<style>
body{{font-family:sans-serif;margin:2rem;}}
table{{border-collapse:collapse;width:100%;margin-bottom:1.5rem;}}
th,td{{border:1px solid #ccc;padding:0.4rem 0.8rem;text-align:right;}}
th{{background:#f0f0f0;}}
</style>
</head>
<body>
<h1>Argentina Macroeconomic Analysis</h1>
<h2>Descriptive Statistics ({START_YEAR}–{END_YEAR})</h2>
{desc.to_html()}
<h2>Correlation Statistics</h2>
{corr_stats.to_html(index=False)}
<p><em>Charts: time_series.png, correlation_heatmap.png</em></p>
</body></html>"""

    report_file = output_path / "report.html"
    report_file.write_text(html, encoding="utf-8")
    logger.info("HTML report saved to %s", report_file)


def main() -> None:
    """Función principal para ejecutar el análisis completo."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    df = load_and_clean_data()
    corr_stats = compute_statistics(df)
    plot_time_series(df, REPORTS_DIR)
    plot_correlation_heatmap(df, REPORTS_DIR)
    export_report(df, corr_stats, REPORTS_DIR)

    logger.info("Analysis complete. Output saved in '%s'.", REPORTS_DIR)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    main()
