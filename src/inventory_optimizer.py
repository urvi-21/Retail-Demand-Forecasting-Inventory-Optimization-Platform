import pandas as pd
import numpy as np

# ==========================================================
# Parameters
# ==========================================================

SERVICE_LEVEL_Z = 1.65      # 95% service level
LEAD_TIME = 2               # weeks

ORDER_COST = 100            # ₹ per order
HOLDING_COST = 10           # ₹ per unit/year

# ==========================================================
# Load Forecasts
# ==========================================================

print("Loading forecasts...")

forecast_df = pd.read_csv(
    "outputs/forecast_results.csv"
)

print("Shape:", forecast_df.shape)

# ==========================================================
# Group by Store and Department
# ==========================================================

groups = forecast_df.groupby(
    ["store", "dept"]
)

results = []

print("Computing inventory recommendations...")

# ==========================================================
# Inventory Calculations
# ==========================================================

for (store, dept), group in groups:

    demand_forecast = (
        group["forecast_sales"]
        .values
    )

    avg_weekly_demand = np.mean(
        demand_forecast
    )

    demand_std = np.std(
        demand_forecast
    )

    annual_demand = (
        avg_weekly_demand * 52
    )

    # ------------------------------------------------------
    # Safety Stock
    # ------------------------------------------------------

    safety_stock = (
        SERVICE_LEVEL_Z
        *
        demand_std
        *
        np.sqrt(LEAD_TIME)
    )

    # ------------------------------------------------------
    # Reorder Point
    # ------------------------------------------------------

    reorder_point = (
        avg_weekly_demand
        * LEAD_TIME
        +
        safety_stock
    )

    # ------------------------------------------------------
    # EOQ
    # ------------------------------------------------------

    eoq = np.sqrt(
        (
            2
            *
            annual_demand
            *
            ORDER_COST
        )
        /
        HOLDING_COST
    )

    # ------------------------------------------------------
    # Recommended Order Quantity
    # ------------------------------------------------------

    recommended_order_qty = (
        safety_stock
        +
        eoq
    )

    # ------------------------------------------------------
    # Save Results
    # ------------------------------------------------------

    results.append({

        "store": store,

        "dept": dept,

        "avg_weekly_demand":
            avg_weekly_demand,

        "annual_demand":
            annual_demand,

        "demand_std":
            demand_std,

        "safety_stock":
            safety_stock,

        "reorder_point":
            reorder_point,

        "eoq":
            eoq,

        "recommended_order_qty":
            recommended_order_qty

    })

# ==========================================================
# Create DataFrame
# ==========================================================

inventory_df = pd.DataFrame(
    results
)

# ==========================================================
# Round Values
# ==========================================================

numeric_cols = [

    "avg_weekly_demand",

    "annual_demand",

    "demand_std",

    "safety_stock",

    "reorder_point",

    "eoq",

    "recommended_order_qty"

]

inventory_df[
    numeric_cols
] = (
    inventory_df[
        numeric_cols
    ]
    .round(0)
)

# ==========================================================
# Save
# ==========================================================

inventory_df.to_csv(

    "outputs/inventory_recommendations.csv",

    index=False

)

# ==========================================================
# Summary
# ==========================================================

print()

print("Inventory optimization complete.")

print()

print(
    inventory_df.head()
)

print()

print("Saved:")

print(
    "outputs/inventory_recommendations.csv"
)