import pandas as pd
import numpy as np

# ============================================================
# Load datasets
# ============================================================

print("Loading datasets...")

train_df = pd.read_csv(
    "data/train.csv",
    parse_dates=["Date"]
)

features_df = pd.read_csv(
    "data/features.csv",
    parse_dates=["Date"]
)

stores_df = pd.read_csv(
    "data/stores.csv"
)

# ============================================================
# Standardize column names
# ============================================================

train_df.columns = train_df.columns.str.lower()
features_df.columns = features_df.columns.str.lower()
stores_df.columns = stores_df.columns.str.lower()

train_df.rename(
    columns={"isholiday": "is_holiday"},
    inplace=True
)

features_df.rename(
    columns={"isholiday": "is_holiday"},
    inplace=True
)

# ============================================================
# Merge datasets
# ============================================================

print("Merging datasets...")

df = train_df.merge(
    features_df,
    on=["store", "date", "is_holiday"],
    how="left"
)

df = df.merge(
    stores_df,
    on="store",
    how="left"
)

print("Shape after merge:", df.shape)

# ============================================================
# Missing values
# ============================================================

markdown_cols = [
    "markdown1",
    "markdown2",
    "markdown3",
    "markdown4",
    "markdown5"
]

df[markdown_cols] = df[markdown_cols].fillna(0)

df["cpi"] = df["cpi"].fillna(
    df["cpi"].median()
)

df["unemployment"] = df["unemployment"].fillna(
    df["unemployment"].median()
)

# ============================================================
# Encode store type
# ============================================================

type_mapping = {
    "A": 0,
    "B": 1,
    "C": 2
}

df["type"] = df["type"].map(type_mapping)

# ============================================================
# Calendar features
# ============================================================

print("Creating calendar features...")

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["quarter"] = df["date"].dt.quarter
df["week"] = df["date"].dt.isocalendar().week.astype(int)
df["dayofyear"] = df["date"].dt.dayofyear

# ============================================================
# Total markdown
# ============================================================

df["total_markdown"] = (
    df["markdown1"]
    + df["markdown2"]
    + df["markdown3"]
    + df["markdown4"]
    + df["markdown5"]
)

# ============================================================
# Sort data
# ============================================================

df = df.sort_values(
    ["store", "dept", "date"]
)

grouped = df.groupby(
    ["store", "dept"]
)

# ============================================================
# Lag features
# ============================================================

print("Creating lag features...")

df["lag_1"] = grouped["weekly_sales"].shift(1)
df["lag_2"] = grouped["weekly_sales"].shift(2)
df["lag_4"] = grouped["weekly_sales"].shift(4)
df["lag_8"] = grouped["weekly_sales"].shift(8)
df["lag_12"] = grouped["weekly_sales"].shift(12)
df["lag_26"] = grouped["weekly_sales"].shift(26)

# ============================================================
# Rolling means
# ============================================================

print("Creating rolling means...")

df["rolling_mean_4"] = grouped["weekly_sales"].transform(
    lambda x: x.shift(1).rolling(4).mean()
)

df["rolling_mean_8"] = grouped["weekly_sales"].transform(
    lambda x: x.shift(1).rolling(8).mean()
)

# ============================================================
# Rolling standard deviations
# ============================================================

print("Creating rolling std...")

df["rolling_std_4"] = grouped["weekly_sales"].transform(
    lambda x: x.shift(1).rolling(4).std()
)

df["rolling_std_8"] = grouped["weekly_sales"].transform(
    lambda x: x.shift(1).rolling(8).std()
)

# ============================================================
# Exponential Moving Averages
# ============================================================

print("Creating EMA features...")

df["ema_4"] = grouped["weekly_sales"].transform(
    lambda x: x.shift(1).ewm(span=4).mean()
)

df["ema_8"] = grouped["weekly_sales"].transform(
    lambda x: x.shift(1).ewm(span=8).mean()
)

# ============================================================
# Remove NaNs created by lag features
# ============================================================

print("Removing rows with insufficient history...")

df.dropna(inplace=True)

df.reset_index(
    drop=True,
    inplace=True
)

print("Final shape:", df.shape)

# ============================================================
# Save feature-engineered dataset
# ============================================================

output_path = "outputs/feature_engineered_data.csv"

df.to_csv(
    output_path,
    index=False
)

print()
print("Feature engineering complete.")
print("Saved to:", output_path)

print()
print("Columns:")
print(df.columns.tolist())