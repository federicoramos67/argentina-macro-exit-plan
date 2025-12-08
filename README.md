# Argentina macro: inflation, unemployment and poverty (1990–2024)

## 📘 Overview (EN)

This project analyzes how inflation, unemployment, and poverty evolved in Argentina from 1990 to 2024 using annual World Bank indicators. The notebook builds a cleaned dataset, visualizes the three series over time with government periods highlighted, and computes a simple correlation matrix to understand how these variables move together. The goal is to provide a clear, data‑driven picture of the macroeconomic context behind Argentina’s recurrent crises and to discuss what any potential “exit plan” should take into account.

## 📙 Descripción (ES)

Este proyecto analiza cómo evolucionaron la inflación, el desempleo y la pobreza en Argentina entre 1990 y 2024 utilizando indicadores anuales del Banco Mundial. El notebook construye un dataset limpio, visualiza las tres series en el tiempo resaltando los periodos de gobierno y calcula una matriz de correlaciones para entender cómo se mueven estas variables. El objetivo es ofrecer una visión clara, basada en datos, del contexto macroeconómico detrás de las crisis recurrentes del país y discutir qué debería considerar cualquier posible “plan de salida”.

## 📊 Data sources

All indicators come from the World Bank’s **World Development Indicators (WDI)** for Argentina:

- **Inflation, consumer prices (annual %)** — code `FP.CPI.TOTL.ZG`, country `ARG`.  
- **Unemployment, total (% of total labor force) (modeled ILO estimate)** — code `SL.UEM.TOTL.ZS`, country `ARG`.  
- **Poverty headcount ratio at national poverty lines (% of population)** — code `SI.POV.NAHC`, country `ARG`.  

The processed CSV files used in this project (`inflation_ar.csv`, `unemployment_ar.csv`, `poverty_ar.csv`) are included in the `data/` folder of this repository for easy reproducibility.

Each indicator was downloaded from the World Bank Data website (“Download CSV” for Argentina). The ZIP file contains three CSVs; the actual time‑series data is in the file starting with `API_...csv`, which was renamed to:

- `inflation_ar.csv`  
- `unemployment_ar.csv`  
- `poverty_ar.csv`  

The `Metadata_...` CSV files (indicator and country metadata) were not used in the analysis.

## 📁 Repository structure

- `Argentina_macro_exit_plan.ipynb` – main analysis notebook (Python, pandas, matplotlib, seaborn).  
- `data/` – folder containing the three CSV files used in the analysis:
  - `inflation_ar.csv`
  - `unemployment_ar.csv`
  - `poverty_ar.csv`

## ⚙️ How to run

1. Clone or download this repository to your local machine.  
2. Make sure the `data/` folder with the three CSV files (`inflation_ar.csv`, `unemployment_ar.csv`, `poverty_ar.csv`) is in the same directory as the notebook.  
3. Open `Argentina_macro_exit_plan.ipynb` in Jupyter or Google Colab and run all cells from top to bottom.


## 🔎 Key insights

- Argentina has struggled with high and volatile inflation for most of the period, with recent spikes harming real wages and savings.  
- Poverty tends to increase during episodes of macroeconomic instability, not only when unemployment is high, highlighting the role of inflation and informal, low‑quality jobs.  
- Stabilization policies need to balance fiscal and monetary discipline with social protection to be sustainable over time.  
- Simple, well‑documented public data (like World Bank indicators) can already reveal which macro problems are structural and must be addressed across different governments.

