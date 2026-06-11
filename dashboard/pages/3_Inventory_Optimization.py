import streamlit as st
import plotly.express as px

from utils.load_data import load_inventory

# ==========================================================
# Load Data
# ==========================================================

inventory_df = load_inventory()

# ==========================================================
# Title
# ==========================================================

st.title("📦 Inventory Optimization")

st.markdown(
    """
    Optimize inventory levels using safety stock,
    reorder points, EOQ and recommended order quantities.
    """
)

# ==========================================================
# KPI Calculations
# ==========================================================

avg_safety_stock = inventory_df["safety_stock"].mean()

avg_reorder_point = inventory_df["reorder_point"].mean()

avg_eoq = inventory_df["eoq"].mean()

avg_order_qty = inventory_df["recommended_order_qty"].mean()

# ==========================================================
# KPI Cards
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Safety Stock",
        f"{avg_safety_stock:,.0f}"
    )

with c2:

    st.metric(
        "Reorder Point",
        f"{avg_reorder_point:,.0f}"
    )

with c3:

    st.metric(
        "EOQ",
        f"{avg_eoq:,.0f}"
    )

with c4:

    st.metric(
        "Order Quantity",
        f"{avg_order_qty:,.0f}"
    )

# ==========================================================
# Charts Row
# ==========================================================

left, right = st.columns(2)

# ==========================================================
# Top Inventory Requirements
# ==========================================================

with left:

    st.subheader(
        "Top Departments by Order Quantity"
    )

    top_inventory = (
        inventory_df
        .groupby("dept")["recommended_order_qty"]
        .sum()
        .reset_index()
        .sort_values(
            "recommended_order_qty",
            ascending=False
        )
        .head(10)
    )

    fig1 = px.bar(
        top_inventory,
        x="recommended_order_qty",
        y="dept",
        orientation="h",
        template="plotly_dark"
    )

    fig1.update_layout(
        height=500
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# ==========================================================
# Scatter Plot
# ==========================================================

with right:

    st.subheader(
        "Demand vs Order Quantity"
    )

    fig2 = px.scatter(
        inventory_df,
        x="avg_weekly_demand",
        y="recommended_order_qty",
        size="safety_stock",
        color="dept",
        template="plotly_dark"
    )

    fig2.update_layout(
        height=500
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==========================================================
# Inventory Table
# ==========================================================

st.subheader(
    "Inventory Details"
)

display_cols = [
    "store",
    "dept",
    "avg_weekly_demand",
    "safety_stock",
    "reorder_point",
    "eoq",
    "recommended_order_qty"
]

st.dataframe(
    inventory_df[display_cols],
    use_container_width=True
)