import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def reshape_wb_indicator(path_csv, value_name):
    """
    Lee un CSV estándar del Banco Mundial, filtra por Argentina
    y devuelve un DataFrame con las columnas: 'year', value_name.
    """
    df_raw = pd.read_csv(path_csv, skiprows=4)
    df_arg = df_raw[df_raw["Country Code"] == "ARG"]
    year_cols = [c for c in df_arg.columns if c.isdigit()]

    df_long = (
        df_arg[year_cols]
        .T.reset_index()
        .rename(columns={"index": "year", df_arg.index[0]: value_name})
    )

    df_long["year"] = df_long["year"].astype(int)
    df_long[value_name] = pd.to_numeric(df_long[value_name], errors="coerce")
    return df_long


def load_and_clean_data(data_path):
    """
    Carga los tres indicadores macroeconómicos y los consolida
    en un único DataFrame.
    """
    inflation_csv = os.path.join(data_path, "inflation_ar.csv")
    unemployment_csv = os.path.join(data_path, "unemployment_ar.csv")
    poverty_csv = os.path.join(data_path, "poverty_ar.csv")

    inflation = reshape_wb_indicator(inflation_csv, "inflation")
    unemployment = reshape_wb_indicator(unemployment_csv, "unemployment")
    poverty = reshape_wb_indicator(poverty_csv, "poverty")

    macro_ar = inflation.merge(unemployment, on="year", how="inner").merge(
        poverty, on="year", how="inner"
    )

    macro_ar = macro_ar[macro_ar["year"] >= 1990].reset_index(drop=True)
    return macro_ar


def plot_time_series(df, output_path):
    """
    Genera y guarda un gráfico de series temporales de inflación,
    desempleo y pobreza.
    """
    plt.style.use("seaborn-v0_8")
    sns.set_palette("tab10")
    sns.set_context("talk")

    fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

    sns.lineplot(data=df, x="year", y="inflation", ax=axes[0])
    axes[0].set_ylabel("Inflation (%)")
    axes[0].set_title("Argentina: annual inflation")

    sns.lineplot(data=df, x="year", y="unemployment", ax=axes[1])
    axes[1].set_ylabel("Unemployment (%)")
    axes[1].set_title("Argentina: unemployment rate")

    sns.lineplot(data=df, x="year", y="poverty", ax=axes[2])
    axes[2].set_ylabel("Poverty (%)")
    axes[2].set_title("Argentina: poverty (national line)")
    axes[2].set_xlabel("Year")

    governments = [
        (1990, 1999, "Menem", "lightblue"),
        (1999, 2001, "De la Rúa", "lightgreen"),
        (2002, 2003, "Duhalde", "khaki"),
        (2003, 2007, "N. Kirchner", "orange"),
        (2007, 2015, "C. Kirchner", "salmon"),
        (2015, 2019, "Macri", "lightgrey"),
        (2019, 2023, "A. Fernández", "plum"),
        (2023, 2025, "Milei", "lightyellow"),
    ]

    for ax in axes:
        for start, end, label, color in governments:
            ax.axvspan(start, end, color=color, alpha=0.15)

    for start, end, label, color in governments:
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
    plt.savefig(os.path.join(output_path, "time_series.png"))
    plt.close()


def plot_correlation_heatmap(df, output_path):
    """
    Calcula y guarda un mapa de calor de la correlación entre las variables.
    """
    corr = df[["inflation", "unemployment", "poverty"]].corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        cbar_kws={"label": "Pearson correlation"},
    )
    plt.title("Correlation: inflation, unemployment and poverty (Argentina)")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "correlation_heatmap.png"))
    plt.close()


def main():
    """
    Función principal para ejecutar el análisis completo.
    """
    DATA_PATH = "data/"
    REPORTS_PATH = "reports/"

    if not os.path.exists(REPORTS_PATH):
        os.makedirs(REPORTS_PATH)

    df = load_and_clean_data(DATA_PATH)
    plot_time_series(df, REPORTS_PATH)
    plot_correlation_heatmap(df, REPORTS_PATH)

    print("Analysis complete. Charts saved in 'reports/' folder.")


if __name__ == "__main__":
    main()
