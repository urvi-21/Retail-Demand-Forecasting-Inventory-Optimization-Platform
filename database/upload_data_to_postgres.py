import pandas as pd
from sqlalchemy import create_engine

# ==========================================================
# PostgreSQL Connection
# ==========================================================

USERNAME = "postgres"
PASSWORD = "postgres123"
HOST = "localhost"
PORT = "5432"
DATABASE = "retail_db"

engine = create_engine(
    f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

# ==========================================================
# Load CSV Files
# ==========================================================

print("Loading output files...")

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
# Standardize Column Names
# ==========================================================

forecast_df.columns = (
    forecast_df.columns
    .str.lower()
)

inventory_df.columns = (
    inventory_df.columns
    .str.lower()
)

metrics_df.columns = (
    metrics_df.columns
    .str.lower()
)

feature_importance_df.columns = (
    feature_importance_df.columns
    .str.lower()
)

# ==========================================================
# Upload Tables
# ==========================================================

print("Uploading forecast_results...")

forecast_df.to_sql(
    "forecast_results",
    engine,
    if_exists="replace",
    index=False
)

print("Uploading inventory_recommendations...")

inventory_df.to_sql(
    "inventory_recommendations",
    engine,
    if_exists="replace",
    index=False
)

print("Uploading evaluation_metrics...")

metrics_df.to_sql(
    "evaluation_metrics",
    engine,
    if_exists="replace",
    index=False
)

print("Uploading feature_importance...")

feature_importance_df.to_sql(
    "feature_importance",
    engine,
    if_exists="replace",
    index=False
)

# ==========================================================
# Summary
# ==========================================================

print()
print("=" * 50)
print("Upload Complete")
print("=" * 50)

print()

print("forecast_results rows:",
      len(forecast_df))

print("inventory_recommendations rows:",
      len(inventory_df))

print("evaluation_metrics rows:",
      len(metrics_df))

print("feature_importance rows:",
      len(feature_importance_df))

print()
print("Tables successfully loaded into PostgreSQL.")