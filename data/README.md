# 🗂️ Datasets

Todos los indicadores provienen de la base **World Development Indicators (WDI)** del Banco Mundial para Argentina (`ARG`). Los archivos CSV se descargaron directamente del portal de datos del Banco Mundial seleccionando Argentina → _Download CSV_.

---

## Archivos incluidos

| Archivo | Indicador WDI | Descripción | Período con datos |
|---------|--------------|-------------|-------------------|
| `inflation_ar.csv` | [`FP.CPI.TOTL.ZG`](https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=AR) | Inflación, precios al consumidor (% anual) | Reciente (ver nota) |
| `unemployment_ar.csv` | [`SL.UEM.TOTL.ZS`](https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS?locations=AR) | Desempleo total, % de la fuerza laboral (estimación OIT modelada) | 1991–2024 |
| `poverty_ar.csv` | [`SI.POV.NAHC`](https://data.worldbank.org/indicator/SI.POV.NAHC?locations=AR) | Ratio de pobreza en línea de pobreza nacional (% de la población) | Años seleccionados |

---

## Formato de los archivos

Los CSV siguen el formato estándar de exportación del Banco Mundial:
- **4 filas de encabezado** (metadatos del dataset)
- **Fila 5**: nombres de columnas — `Country Name`, `Country Code`, `Indicator Name`, `Indicator Code`, `1960`, `1961`, ..., `2024`
- **Filas de datos**: una fila por país; los valores de cada año son columnas separadas (formato _wide_)
- **Valores ausentes**: celdas vacías para años sin datos disponibles

El script `src/main.py` lee estos archivos con `pd.read_csv(..., skiprows=4)`, filtra por `Country Code == "ARG"` y convierte el formato _wide_ a _long_ (una fila por año).

---

## Notas sobre cobertura

- **Desempleo** tiene la cobertura más completa: datos continuos desde principios de los 90 hasta 2024.
- **Inflación** y **Pobreza** tienen años sin datos en rangos históricos; el análisis usa los años disponibles sin imputación.
- El Banco Mundial actualiza estos indicadores periódicamente. La versión incluida en este repositorio corresponde a la **descarga de diciembre de 2024**.

---

## Reproducir la descarga

Para obtener datos actualizados directamente:

1. Visitá [data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=AR](https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=AR)
2. Hacé clic en **Download → CSV**
3. Del ZIP descargado, usá el archivo que comienza con `API_`
4. Renombrá a `inflation_ar.csv` y reemplazá en esta carpeta
5. Repetí para los otros dos indicadores

---

*Fuente: World Bank Open Data · Licencia: [CC BY 4.0](https://datacatalog.worldbank.org/public-licenses#cc-by)*
