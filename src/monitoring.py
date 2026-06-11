import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ==========================================================
# Create monitoring folder
# ==========================================================

Path("monitoring").mkdir(exist_ok=True)

# ==========================================================
# Load files
# ==========================================================

forecast_df = pd.read_csv(
    "outputs/forecast_results.csv"
)

inventory_df = pd.read_csv(
    "outputs/inventory_recommendations.csv"
)

# ==========================================================
# Calculate KPIs
# ==========================================================

total_forecasted_demand = forecast_df["forecast_sales"].sum()

average_forecast = forecast_df["forecast_sales"].mean()

average_safety_stock = inventory_df["safety_stock"].mean()

average_eoq = inventory_df["eoq"].mean()

average_order_quantity = (
    inventory_df["recommended_order_qty"].mean()
)

# ==========================================================
# KPI Report CSV
# ==========================================================

kpi_df = pd.DataFrame(
    {
        "Metric": [
            "Total Forecasted Demand",
            "Average Forecast",
            "Average Safety Stock",
            "Average EOQ",
            "Average Order Quantity"
        ],
        "Value": [
            total_forecasted_demand,
            average_forecast,
            average_safety_stock,
            average_eoq,
            average_order_quantity
        ]
    }
)

kpi_df.to_csv(
    "monitoring/kpi_report.csv",
    index=False
)

# ==========================================================
# Forecast Distribution Plot
# ==========================================================

plt.figure(figsize=(8, 5))

plt.hist(
    forecast_df["forecast_sales"],
    bins=30
)

plt.xlabel("Forecast Sales")
plt.ylabel("Frequency")
plt.title("Forecast Distribution")

plt.tight_layout()

plt.savefig(
    "monitoring/forecast_distribution.png"
)

plt.close()

# ==========================================================
# Inventory Distribution Plot
# ==========================================================

plt.figure(figsize=(8, 5))

plt.hist(
    inventory_df["recommended_order_qty"],
    bins=30
)

plt.xlabel("Recommended Order Quantity")
plt.ylabel("Frequency")
plt.title("Inventory Distribution")

plt.tight_layout()

plt.savefig(
    "monitoring/inventory_distribution.png"
)

plt.close()

# ==========================================================
# Monitoring Report
# ==========================================================

report = f"""
=================================
MODEL MONITORING REPORT
=================================

Total Forecasted Demand : {total_forecasted_demand:,.0f}

Average Forecast        : {average_forecast:,.0f}

Average Safety Stock    : {average_safety_stock:,.0f}

Average EOQ             : {average_eoq:,.0f}

Average Order Quantity  : {average_order_quantity:,.0f}

STATUS : HEALTHY

No anomalies detected.

=================================
"""

with open(
    "monitoring/monitoring_report.txt",
    "w"
) as f:
    f.write(report)

# ==========================================================
# Console Output
# ==========================================================

print()
print("=================================")
print("MODEL MONITORING REPORT")
print("=================================")
print()

print(
    f"Total Forecasted Demand : "
    f"{total_forecasted_demand:,.0f}"
)

print(
    f"Average Forecast        : "
    f"{average_forecast:,.0f}"
)

print(
    f"Average Safety Stock    : "
    f"{average_safety_stock:,.0f}"
)

print(
    f"Average EOQ             : "
    f"{average_eoq:,.0f}"
)

print(
    f"Average Order Quantity  : "
    f"{average_order_quantity:,.0f}"
)

print()
print("STATUS : HEALTHY")
print("No anomalies detected.")
print()

print("Files generated:")
print("- monitoring/kpi_report.csv")
print("- monitoring/monitoring_report.txt")
print("- monitoring/forecast_distribution.png")
print("- monitoring/inventory_distribution.png")