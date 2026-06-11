import pandas as pd
import streamlit as st


@st.cache_data
def load_forecast():

    return pd.read_csv(
        "outputs/forecast_results.csv"
    )


@st.cache_data
def load_inventory():

    return pd.read_csv(
        "outputs/inventory_recommendations.csv"
    )


@st.cache_data
def load_metrics():

    return pd.read_csv(
        "outputs/evaluation_metrics.csv"
    )


@st.cache_data
def load_features():

    return pd.read_csv(
        "outputs/feature_importance.csv"
    )