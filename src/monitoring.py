import pandas as pd
import matplotlib.pyplot as plt

# ======================================
# Load files
# ======================================

forecast_df = pd.read_csv(
    "outputs/forecast_results.csv"
)

inventory_df = pd.read_csv(
    "outputs/inventory_recommendations.csv"
)

metrics_df = pd.read_csv(
    "outputs/evaluation_metrics.csv"
)

# ======================================
# KPI Report
# ======================================

kpi_dict = {

    "Total Forecasted Demand":
        forecast_df["forecast_sales"].sum(),

    "Average Forecast":
        forecast_df["forecast_sales"].mean(),

    "Average Safety Stock":
        inventory_df["safety_stock"].mean(),

    "Average EOQ":
        inventory_df["eoq"].mean(),

    "Average Order Quantity":
        inventory_df["recommended_order_qty"].mean()
}

kpi_report = pd.DataFrame(
    kpi_dict.items(),
    columns=["Metric", "Value"]
)

kpi_report.to_csv(
    "monitoring/kpi_report.csv",
    index=False
)

# ======================================
# Forecast Distribution
# ======================================

plt.figure(figsize=(8,5))

forecast_df["forecast_sales"].hist(
    bins=50
)

plt.title(
    "Forecast Distribution"
)

plt.xlabel(
    "Forecast Sales"
)

plt.ylabel(
    "Frequency"
)

plt.savefig(
    "monitoring/forecast_distribution.png"
)

plt.close()

# ======================================
# Inventory Distribution
# ======================================

plt.figure(figsize=(8,5))

inventory_df[
    "recommended_order_qty"
].hist(
    bins=50
)

plt.title(
    "Order Quantity Distribution"
)

plt.xlabel(
    "Order Quantity"
)

plt.ylabel(
    "Frequency"
)

plt.savefig(
    "monitoring/inventory_distribution.png"
)

plt.close()

print()
print("Monitoring complete.")