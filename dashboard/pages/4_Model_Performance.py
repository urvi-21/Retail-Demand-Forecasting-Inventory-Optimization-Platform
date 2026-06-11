import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

from utils.load_data import (
    load_metrics,
    load_features
)

# ==========================================================
# Load Data
# ==========================================================

metrics_df = load_metrics()

features_df = load_features()

# ==========================================================
# Page Title
# ==========================================================

st.title("🤖 Model Performance")

st.markdown(
    """
    Evaluate forecasting model performance and
    understand feature importance.
    """
)

# ==========================================================
# Metric Cards
# ==========================================================

metric_dict = dict(
    zip(
        metrics_df["Metric"],
        metrics_df["Value"]
    )
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "MAE",
        f"{metric_dict['MAE']:,.2f}"
    )

with c2:
    st.metric(
        "RMSE",
        f"{metric_dict['RMSE']:,.2f}"
    )

with c3:
    st.metric(
        "R²",
        f"{metric_dict['R2']:.4f}"
    )

with c4:
    st.metric(
        "SMAPE",
        f"{metric_dict['SMAPE']:.2f}"
    )

with c5:
    st.metric(
        "WAPE",
        f"{metric_dict['WAPE']:.2f}"
    )

# ==========================================================
# Feature Importance Chart
# ==========================================================

st.subheader(
    "Top Feature Importance"
)

top_features = (
    features_df
    .sort_values(
        "Importance",
        ascending=False
    )
    .head(20)
)

fig = px.bar(
    top_features,
    x="Importance",
    y="Feature",
    orientation="h",
    template="plotly_dark"
)

fig.update_layout(
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# Images
# ==========================================================

st.subheader(
    "Diagnostic Plots"
)

left, right = st.columns(2)

with left:

    st.image(
        "outputs/actual_vs_predicted.png",
        caption="Actual vs Predicted"
    )

    st.image(
        "outputs/residual_plot.png",
        caption="Residual Plot"
    )

with right:

    st.image(
        "outputs/feature_importance.png",
        caption="Feature Importance"
    )

    st.image(
        "outputs/shap_summary.png",
        caption="SHAP Summary"
    )