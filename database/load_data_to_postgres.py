import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.types import (
    Integer,
    Float,
    Boolean,
    Date,
    String
)

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
# Read CSV Files
# ==========================================================

sales_df = pd.read_csv(
    r"D:\forecasting\data\train.csv",
    parse_dates=["Date"]
)

features_df = pd.read_csv(
    r"D:\forecasting\data\features.csv",
    parse_dates=["Date"]
)

stores_df = pd.read_csv(
    r"D:\forecasting\data\stores.csv"
)

# ==========================================================
# Standardize Column Names
# ==========================================================

sales_df.columns = (
    sales_df.columns
    .str.strip()
    .str.lower()
)

features_df.columns = (
    features_df.columns
    .str.strip()
    .str.lower()
)

stores_df.columns = (
    stores_df.columns
    .str.strip()
    .str.lower()
)

# ==========================================================
# Rename Columns
# ==========================================================

sales_df.rename(
    columns={
        "isholiday": "is_holiday"
    },
    inplace=True
)

features_df.rename(
    columns={
        "isholiday": "is_holiday"
    },
    inplace=True
)

# ==========================================================
# Convert Dates
# ==========================================================

sales_df["date"] = pd.to_datetime(
    sales_df["date"]
).dt.date

features_df["date"] = pd.to_datetime(
    features_df["date"]
).dt.date

# ==========================================================
# Upload Sales Table
# ==========================================================

sales_df.to_sql(
    "sales",
    engine,
    if_exists="replace",
    index=False,
    dtype={
        "store": Integer(),
        "dept": Integer(),
        "date": Date(),
        "weekly_sales": Float(),
        "is_holiday": Boolean()
    }
)

# ==========================================================
# Upload Features Table
# ==========================================================

features_df.to_sql(
    "features",
    engine,
    if_exists="replace",
    index=False,
    dtype={
        "store": Integer(),
        "date": Date(),
        "temperature": Float(),
        "fuel_price": Float(),
        "markdown1": Float(),
        "markdown2": Float(),
        "markdown3": Float(),
        "markdown4": Float(),
        "markdown5": Float(),
        "cpi": Float(),
        "unemployment": Float(),
        "is_holiday": Boolean()
    }
)

# ==========================================================
# Upload Stores Table
# ==========================================================

stores_df.to_sql(
    "stores",
    engine,
    if_exists="replace",
    index=False,
    dtype={
        "store": Integer(),
        "type": String(1),
        "size": Integer()
    }
)

# ==========================================================
# Verification
# ==========================================================

print("\n===================================")
print("Upload Complete")
print("===================================\n")

print("Sales rows    :", len(sales_df))
print("Features rows :", len(features_df))
print("Stores rows   :", len(stores_df))

print("\nSales Columns")
print(sales_df.columns.tolist())

print("\nFeatures Columns")
print(features_df.columns.tolist())

print("\nStores Columns")
print(stores_df.columns.tolist())

print("\nSales Data Types")
print(sales_df.dtypes)

print("\nFeatures Data Types")
print(features_df.dtypes)

print("\nStores Data Types")
print(stores_df.dtypes)

print("\n===================================")
print("Tables successfully loaded into PostgreSQL.")
print("===================================")