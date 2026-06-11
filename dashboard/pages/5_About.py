import streamlit as st

# ==========================================================
# Page Title
# ==========================================================

st.title("ℹ️ About")

st.markdown(
    """
    Retail Demand Forecasting and Inventory Optimization Platform
    """
)

st.divider()

# ==========================================================
# Overview
# ==========================================================

st.header("Project Overview")

st.write(
    """
This project provides an end-to-end solution for retail demand forecasting
and inventory optimization using machine learning and business analytics.

It predicts future demand and transforms predictions into actionable
inventory decisions using safety stock, reorder point, EOQ and
recommended order quantities.
"""
)

# ==========================================================
# Architecture
# ==========================================================

st.header("System Architecture")

architecture = """
CSV Files
↓
PostgreSQL Database
↓
Feature Engineering
↓
XGBoost Forecasting Model
↓
Recursive Forecasting Engine
↓
Inventory Optimization
↓
FastAPI
↓
Streamlit Dashboard
↓
Power BI Dashboard
↓
Monitoring
"""

st.code(
    architecture,
    language=None
)

# ==========================================================
# Tech Stack
# ==========================================================

st.header("Tech Stack")

c1, c2 = st.columns(2)

with c1:

    st.subheader("Machine Learning")

    st.markdown(
        """
- XGBoost
- SHAP
- Scikit-Learn
- Pandas
- NumPy
"""
    )

    st.subheader("Backend")

    st.markdown(
        """
- FastAPI
- Python
"""
    )

with c2:

    st.subheader("Database")

    st.markdown(
        """
- PostgreSQL
- SQL
"""
    )

    st.subheader("Visualization")

    st.markdown(
        """
- Streamlit
- Plotly
- Power BI
- Matplotlib
"""
    )

# ==========================================================
# Project Highlights
# ==========================================================

st.header("Project Highlights")

st.success(
    """
✓ Demand Forecasting

✓ Feature Engineering

✓ XGBoost Model

✓ Recursive Multi-Step Forecasting

✓ Inventory Optimization

✓ Safety Stock Calculation

✓ Reorder Point Calculation

✓ EOQ Calculation

✓ FastAPI Integration

✓ Power BI Dashboard

✓ Model Monitoring
"""
)

# ==========================================================
# Folder Structure
# ==========================================================

st.header("Folder Structure")

folder_structure = """
forecasting/

├── api/
├── dashboard/
├── database/
├── models/
├── monitoring/
├── notebooks/
├── outputs/
├── src/

"""

st.code(
    folder_structure,
    language=None
)

# ==========================================================
# Author
# ==========================================================

st.header("Author")

st.info(
    """
Developed by Urvi Patel

B.Tech Biomedical Engineering

NIT Raipur

Machine Learning • Data Science • Analytics
"""
)

# ==========================================================
# Footer
# ==========================================================

st.divider()

st.caption(
    "Retail Demand Forecasting and Inventory Optimization Platform"
)