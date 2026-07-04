# retail-pulse-Dashboard

# 🩺 RetailPulse — Sales Forecasting & Demand Intelligence System

An end-to-end retail analytics project that predicts future product demand, detects unusual sales
patterns, segments products by demand behavior, and presents everything through a deployed interactive
dashboard.

Built on 4 years of Superstore sales data, RetailPulse compares three independent forecasting approaches
(SARIMA, Prophet, XGBoost), blends them into a confidence-weighted ensemble, cross-validates anomalies
using two separate detection methods, and clusters products into demand groups with recommended
stocking strategies.

**🔗 Live dashboard:** [your-app-name.streamlit.app](https://your-app-name.streamlit.app) *(replace with your actual link)*



## What this project does

| Capability | Approach |
|---|---|
| Data exploration | Time-feature engineering, revenue/region/seasonality analysis |
| Time series analysis | Trend/seasonal/residual decomposition, stationarity testing (ADF) |
| Forecasting | SARIMA, Prophet, XGBoost — compared on MAE / RMSE / MAPE, plus a blended ensemble |
| Anomaly detection | Isolation Forest + rolling Z-score, cross-checked for agreement |
| Product segmentation | K-Means clustering on volume, growth, volatility, order value ("Demand DNA") |
| Deployment | 4-page interactive Streamlit dashboard |



## Project structure

```
retail-pulse-dashboard/
├── RetailPulse_Sales_Forecasting.ipynb   # Full analysis notebook (run in Google Colab)
├── app.py                                # Streamlit dashboard (reads exported CSVs)
├── requirements.txt                      # Python dependencies
├── RetailPulse_Executive_Report.pdf      # 2-page business summary for non-technical stakeholders
└── pulse_exports/                        # Model outputs consumed by the dashboard
    ├── monthly_sales.csv
    ├── weekly_sales.csv
    ├── model_leaderboard.csv
    ├── ensemble_forecast.csv
    ├── confirmed_anomalies.csv
    └── product_clusters.csv



## How it's built

The notebook is organized as a small pipeline of cooperating classes rather than a flat script:


DataForge → TimeSeriesLab → ForecastArena → AnomalyRadar → DemandSegmenter → RetailPulseEngine
```

`RetailPulseEngine` is the single entry point — one call (`run_full_pipeline()`) runs the entire
analysis and exports the CSVs the dashboard needs (`export_for_dashboard()`).

---

## Running it yourself

### 1. Run the analysis notebook
Open `RetailPulse_Sales_Forecasting.ipynb` in [Google Colab](https://colab.research.google.com/).
You'll need a free [Kaggle](https://kaggle.com) account and API token to pull the datasets
(instructions are in the notebook's setup cell). Running it end-to-end regenerates all files in
`pulse_exports/`.

### 2. Run the dashboard locally
```bash
git clone https://github.com/your-username/retail-pulse-dashboard.git
cd retail-pulse-dashboard
pip install -r requirements.txt
streamlit run app.py
```
Opens at `http://localhost:8501`.

### 3. Deploy it
Push this repo (including `pulse_exports/`) to GitHub, then deploy for free on
[Streamlit Community Cloud](https://share.streamlit.io) by pointing it at `app.py`.



## Dashboard pages

1. **Sales Overview** — yearly/monthly revenue trends
2. **Forecast Explorer** — best-model forecast by category/region with MAE/RMSE
3. **Anomaly Report** — confirmed anomaly weeks (flagged by both detection methods)
4. **Demand Segments** — product clusters and recommended stocking strategy per group



## Datasets

- [Superstore Sales Dataset](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting) — primary sales data
- [Video Game Sales Dataset](https://www.kaggle.com/datasets/gregorut/videogamesales) — secondary dataset used for multi-source merging practice



## Tech stack

Python · Pandas · Statsmodels (SARIMA) · Prophet · XGBoost · Scikit-learn (Isolation Forest, K-Means, PCA) · Plotly · Streamlit



## Limitations

Forecasts assume near-future demand behaves like recent historical patterns and will not anticipate
one-off shocks (new competitors, supply disruptions, sudden demand shifts). Model should be
re-validated and retrained on a regular cadence rather than treated as a one-time deliverable.



