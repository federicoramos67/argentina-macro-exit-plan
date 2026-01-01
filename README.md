# Análisis Macroeconómico de Argentina (1990-2024)

## 📘 Descripción

Este proyecto analiza la evolución de la inflación, el desempleo y la pobreza en Argentina utilizando indicadores anuales del Banco Mundial. El objetivo es ofrecer una visión clara y basada en datos del contexto macroeconómico detrás de las crisis recurrentes del país.

El análisis incluye:
- Carga y limpieza de datos de indicadores del Banco Mundial.
- Visualización de las series temporales, destacando los períodos de gobierno.
- Cálculo de una matriz de correlación para entender cómo se interrelacionan estas variables.

## 📁 Estructura del Repositorio

El proyecto está organizado siguiendo una estructura estándar para proyectos de Data Science:

- `src/`: Contiene el script principal `main.py` con toda la lógica del análisis.
- `data/`: Almacena los datasets originales (`inflation_ar.csv`, `unemployment_ar.csv`, `poverty_ar.csv`).
- `notebooks/`: Incluye el notebook original `Argentina_macro_exit_plan.ipynb` como registro de la exploración inicial.
- `reports/`: Guarda las visualizaciones generadas (`time_series.png`, `correlation_heatmap.png`).
- `tests/`: Destinada a futuras pruebas unitarias.
- `run.py`: Script para ejecutar el flujo de trabajo completo con un solo comando.
- `requirements.txt`: Lista de dependencias de Python para una fácil instalación.

## ⚙️ Cómo Ejecutar el Análisis

Para replicar este análisis, sigue estos pasos:

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tomas-heredia/argentina-macro-exit-plan.git
   cd argentina-macro-exit-plan
   ```

2. **Instala las dependencias:**
   Asegúrate de tener Python 3 instalado. Luego, instala las librerías necesarias ejecutando:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta el análisis:**
   Simplemente ejecuta el script `run.py` desde la raíz del proyecto:
   ```bash
   python run.py
   ```
   Tras la ejecución, los gráficos actualizados se guardarán en la carpeta `reports/`.

## 📊 Fuentes de Datos

Todos los indicadores provienen de los **Indicadores de Desarrollo Mundial (WDI)** del Banco Mundial para Argentina:

- **Inflación, precios al consumidor (% anual)** - `FP.CPI.TOTL.ZG`
- **Desempleo, total (% de la fuerza laboral total)** - `SL.UEM.TOTL.ZS`
- **Tasa de pobreza (% de la población)** - `SI.POV.NAHC`

Los archivos CSV procesados se incluyen en la carpeta `data/` para facilitar la reproducibilidad.
