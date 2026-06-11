import streamlit as st
import plotly.express as px

from utils.load_data import (
    load_forecast,
    load_inventory
)

# =========================================================
# Load data
# =========================================================

forecast_df = load_forecast()
inventory_df = load_inventory()

# =========================================================
# Page config
# =========================================================

st.title("📈 Executive Overview")

st.markdown(
    """
    High-level overview of demand forecasting and
    inventory optimization.
    """
)

# =========================================================
# KPI calculations
# =========================================================

total_forecast = forecast_df["forecast_sales"].sum()

avg_forecast = forecast_df["forecast_sales"].mean()

avg_order_qty = (
    inventory_df["recommended_order_qty"].mean()
)

forecast_count = len(forecast_df)

# =========================================================
# KPI cards
# =========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Total Forecast",
        f"{total_forecast:,.0f}"
    )

with c2:

    st.metric(
        "Average Forecast",
        f"{avg_forecast:,.0f}"
    )

with c3:

    st.metric(
        "Average Order Qty",
        f"{avg_order_qty:,.0f}"
    )

with c4:

    st.metric(
        "Forecast Count",
        f"{forecast_count:,}"
    )

# =========================================================
# Row 2
# =========================================================

left, right = st.columns([2, 1])

# =========================================================
# Forecast trend
# =========================================================

with left:

    st.subheader("Portfolio Forecast")

    weekly_forecast = (
        forecast_df
        .groupby("forecast_week")["forecast_sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        weekly_forecast,
        x="forecast_week",
        y="forecast_sales",
        markers=True,
        template="plotly_dark"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# Top departments
# =========================================================

with right:

    st.subheader(
        "Top 10 Departments"
    )

    top_depts = (
        forecast_df
        .groupby("dept")["forecast_sales"]
        .sum()
        .reset_index()
        .sort_values(
            "forecast_sales",
            ascending=False
        )
        .head(10)
    )

    fig2 = px.bar(
        top_depts,
        x="forecast_sales",
        y="dept",
        orientation="h",
        template="plotly_dark"
    )

    fig2.update_layout(
        height=450
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =========================================================
# Bottom KPIs
# =========================================================

st.divider()

b1, b2, b3, b4 = st.columns(4)

with b1:

    st.metric(
        "Total Stores",
        forecast_df["store"].nunique()
    )

with b2:

    st.metric(
        "Total Departments",
        forecast_df["dept"].nunique()
    )

with b3:

    st.metric(
        "Average Forecast / Store",
        f"{total_forecast / forecast_df['store'].nunique():,.0f}"
    )

with b4:

    st.metric(
        "Average Forecast / Department",
        f"{total_forecast / forecast_df['dept'].nunique():,.0f}"
    )