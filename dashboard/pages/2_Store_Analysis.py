import streamlit as st
import plotly.express as px

from utils.load_data import load_forecast

# ==========================================================
# Load data
# ==========================================================

forecast_df = load_forecast()

# ==========================================================
# Page Title
# ==========================================================

st.title("🏪 Store Analysis")

st.markdown(
    """
    Explore forecast patterns by store and department.
    """
)

# ==========================================================
# Filters
# ==========================================================

c1, c2 = st.columns(2)

with c1:

    selected_store = st.selectbox(
        "Select Store",
        sorted(
            forecast_df["store"].unique()
        )
    )

with c2:

    selected_dept = st.selectbox(
        "Select Department",
        sorted(
            forecast_df["dept"].unique()
        )
    )

# ==========================================================
# Filter Data
# ==========================================================

filtered_df = forecast_df[
    (forecast_df["store"] == selected_store)
    &
    (forecast_df["dept"] == selected_dept)
]

# ==========================================================
# Forecast Trend
# ==========================================================

st.subheader(
    "Forecast Trend"
)

fig = px.line(
    filtered_df,
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

# ==========================================================
# Heatmap
# ==========================================================

st.subheader(
    "Demand Heatmap"
)

heatmap_data = (
    forecast_df
    .pivot_table(
        values="forecast_sales",
        index="dept",
        columns="forecast_week",
        aggfunc="sum"
    )
)

fig2 = px.imshow(
    heatmap_data,
    aspect="auto",
    template="plotly_dark",
    color_continuous_scale="Viridis"
)

fig2.update_layout(
    height=500
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================================
# Top Departments
# ==========================================================

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

fig3 = px.bar(
    top_depts,
    x="forecast_sales",
    y="dept",
    orientation="h",
    template="plotly_dark"
)

fig3.update_layout(
    height=450
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================================
# Forecast Table
# ==========================================================

st.subheader(
    "Forecast Details"
)

st.dataframe(
    filtered_df,
    use_container_width=True
)