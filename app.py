
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


st.set_page_config(page_title="RetailPulse", page_icon="🩺", layout="wide")

PULSE = {
    "signal": "#2FD3B0", "forecast": "#FF6F59", "band": "#FFD166",
    "anomaly": "#EF476F", "muted": "#8A8FA3", "bg": "#12131A",
}

st.markdown(f"""
<style>
    .stApp {{ background-color: {PULSE['bg']}; }}
    div[data-testid="stMetricValue"] {{ color: {PULSE['signal']}; }}
    h1, h2, h3 {{ color: white; }}
</style>
""", unsafe_allow_html=True)

DATA_DIR = Path("pulse_exports")

@st.cache_data
def load(name):
    return pd.read_csv(DATA_DIR / name, index_col=0, parse_dates=True)

monthly = load("monthly_sales.csv")
weekly = load("weekly_sales.csv")
leaderboard = load("model_leaderboard.csv")
ensemble = load("ensemble_forecast.csv")
anomalies = load("confirmed_anomalies.csv")
clusters = load("product_clusters.csv")

st.sidebar.title("🩺 RetailPulse")
page = st.sidebar.radio("Navigate", [
    "Sales Overview", "Forecast Explorer", "Anomaly Report", "Demand Segments"
])
st.sidebar.markdown("---")
st.sidebar.caption("Data-driven demand intelligence for retail stocking decisions.")

# Sales Overview - page 1

if page == "Sales Overview":
    st.title("Sales Overview")

    yearly = monthly.copy()
    yearly["Year"] = yearly.index.year
    yearly_totals = yearly.groupby("Year")["MonthlySales"].sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue (all years)", f"${monthly['MonthlySales'].sum():,.0f}")
    c2.metric("Avg Monthly Sales", f"${monthly['MonthlySales'].mean():,.0f}")
    c3.metric("Latest Month", f"${monthly['MonthlySales'].iloc[-1]:,.0f}")

    st.subheader("Total Sales by Year")
    fig1 = px.bar(x=yearly_totals.index.astype(str), y=yearly_totals.values,
                   labels={"x": "Year", "y": "Sales"}, color_discrete_sequence=[PULSE["signal"]])
    fig1.update_layout(template="plotly_dark", plot_bgcolor=PULSE["bg"], paper_bgcolor=PULSE["bg"])
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Monthly Sales Trend")
    fig2 = px.line(monthly, x=monthly.index, y="MonthlySales",
                    color_discrete_sequence=[PULSE["signal"]])
    fig2.update_layout(template="plotly_dark", plot_bgcolor=PULSE["bg"], paper_bgcolor=PULSE["bg"])
    st.plotly_chart(fig2, use_container_width=True)

    st.info("Region/Category breakdown filters render here once you export "
            "`sales_by_region_category.csv` from the notebook (groupby Region & Category).")

# Forecast Explorer - page 2
elif page == "Forecast Explorer":
    st.title("Forecast Explorer")

    col1, col2 = st.columns(2)
    with col1:
        view = st.selectbox("Select view", ["Overall", "By Category", "By Region"])
    with col2:
        horizon = st.slider("Forecast horizon (months ahead)", 1, 3, 3)

    st.subheader(f"Best-Model Forecast — {view}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly.index, y=monthly["MonthlySales"],
                              mode="lines", name="Actual", line=dict(color=PULSE["signal"], width=2)))
    fig.add_trace(go.Scatter(x=ensemble.index[:horizon], y=ensemble.iloc[:horizon, 0],
                              mode="lines+markers", name="Ensemble Forecast",
                              line=dict(color=PULSE["forecast"], dash="dash")))
    fig.update_layout(template="plotly_dark", plot_bgcolor=PULSE["bg"], paper_bgcolor=PULSE["bg"])
    st.plotly_chart(fig, use_container_width=True)

    best = leaderboard["MAPE (%)"].astype(float).idxmin()
    c1, c2, c3 = st.columns(3)
    c1.metric("Best Model", best)
    c2.metric("MAE", f"{leaderboard.loc[best, 'MAE']:.2f}")
    c3.metric("RMSE", f"{leaderboard.loc[best, 'RMSE']:.2f}")

    st.subheader("Full Model Leaderboard")
    st.dataframe(leaderboard, use_container_width=True)

# Anomaly Report - page 3

elif page == "Anomaly Report":
    st.title("Anomaly Report")
    st.caption("Weeks flagged by BOTH Isolation Forest and rolling Z-score — highest-confidence anomalies.")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=weekly.index, y=weekly["WeeklySales"], mode="lines",
                              name="Weekly Sales", line=dict(color=PULSE["signal"])))
    fig.add_trace(go.Scatter(x=anomalies.index, y=anomalies["sales"], mode="markers",
                              name="Confirmed Anomaly",
                              marker=dict(color=PULSE["anomaly"], size=10, symbol="x")))
    fig.update_layout(template="plotly_dark", plot_bgcolor=PULSE["bg"], paper_bgcolor=PULSE["bg"])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Detected Anomaly Weeks")
    st.dataframe(anomalies.sort_values("sales", ascending=False), use_container_width=True)

# Demand Segment - page 4

elif page == "Demand Segments":
    st.title("Product Demand Segments")
    st.caption('Each sub-category\'s "Demand DNA" — volume, growth, volatility — mapped to a stocking strategy.')

    fig = px.scatter(clusters, x="total_sales", y="volatility", color="cluster_label",
                      size="avg_order_value", hover_name=clusters.index,
                      labels={"total_sales": "Total Sales", "volatility": "Sales Volatility"})
    fig.update_layout(template="plotly_dark", plot_bgcolor=PULSE["bg"], paper_bgcolor=PULSE["bg"])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sub-Category → Cluster → Recommended Strategy")
    st.dataframe(
        clusters[["cluster_label", "total_sales", "growth_rate", "volatility", "recommended_strategy"]],
        use_container_width=True
    )
