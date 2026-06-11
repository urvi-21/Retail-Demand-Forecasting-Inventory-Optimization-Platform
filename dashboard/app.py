import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="Retail Demand Forecasting Platform",
    layout="wide"
)

st.title("Retail Demand Forecasting & Inventory Optimization")

# ==========================================================
# Load Data
# ==========================================================

forecast_df = pd.read_csv(
    "outputs/forecast_results.csv"
)

inventory_df = pd.read_csv(
    "outputs/inventory_recommendations.csv"
)

metrics_df = pd.read_csv(
    "outputs/evaluation_metrics.csv"
)

feature_importance_df = pd.read_csv(
    "outputs/feature_importance.csv"
)

# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.header("Filters")

store_list = sorted(
    forecast_df["store"].unique()
)

dept_list = sorted(
    forecast_df["dept"].unique()
)

selected_store = st.sidebar.selectbox(
    "Store",
    store_list
)

selected_dept = st.sidebar.selectbox(
    "Department",
    dept_list
)

# ==========================================================
# KPIs
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Forecasted Demand",
    f"{forecast_df['forecast_sales'].sum():,.0f}"
)

col2.metric(
    "Average Weekly Demand",
    f"{forecast_df['forecast_sales'].mean():,.0f}"
)

col3.metric(
    "Average Order Quantity",
    f"{inventory_df['recommended_order_qty'].mean():,.0f}"
)

col4.metric(
    "Number of Forecasts",
    len(forecast_df)
)

# ==========================================================
# Forecast for Selected Store + Dept
# ==========================================================

st.header("Demand Forecast")

filtered_forecast = forecast_df[
    (forecast_df["store"] == selected_store)
    &
    (forecast_df["dept"] == selected_dept)
]

fig = px.line(
    filtered_forecast,
    x="forecast_week",
    y="forecast_sales",
    markers=True,
    title=f"Store {selected_store} Dept {selected_dept}"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# Inventory Recommendation
# ==========================================================

st.header("Inventory Recommendation")

filtered_inventory = inventory_df[
    (inventory_df["store"] == selected_store)
    &
    (inventory_df["dept"] == selected_dept)
]

st.dataframe(
    filtered_inventory
)

# ==========================================================
# Model Metrics
# ==========================================================

st.header("Model Performance")

st.dataframe(
    metrics_df
)

# ==========================================================
# Feature Importance
# ==========================================================

st.header("Top Features")

top_features = (
    feature_importance_df
    .head(20)
)

fig2 = px.bar(
    top_features,
    x="Importance",
    y="Feature",
    orientation="h",
    title="Top 20 Feature Importances"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================================
# Portfolio Forecast
# ==========================================================

st.header("Portfolio Forecast")

portfolio_forecast = (
    forecast_df
    .groupby("forecast_week")
    ["forecast_sales"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    portfolio_forecast,
    x="forecast_week",
    y="forecast_sales",
    markers=True,
    title="Portfolio-Level Forecast"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================================
# Raw Tables
# ==========================================================

st.header("Forecast Table")

st.dataframe(
    forecast_df
)

st.header("Inventory Table")

st.dataframe(
    inventory_df
)