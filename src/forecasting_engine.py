import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# ==========================================================
# Parameters
# ==========================================================

HORIZON = 12

# ==========================================================
# Load Model
# ==========================================================

print("Loading model...")

model = joblib.load(
    "models/xgb_model.pkl"
)

# ==========================================================
# Load Dataset
# ==========================================================

print("Loading feature-engineered data...")

df = pd.read_csv(
    "outputs/feature_engineered_data.csv",
    parse_dates=["date"]
)

df = df.sort_values(
    ["store", "dept", "date"]
)

# ==========================================================
# Group by Store and Department
# ==========================================================

groups = df.groupby(
    ["store", "dept"]
)

forecast_rows = []

print("Forecasting all store-department series...")

# ==========================================================
# Loop through all series
# ==========================================================

for (store, dept), history in groups:

    history = history.copy()

    sales_history = list(
        history["weekly_sales"].values
    )

    last_row = history.iloc[-1].copy()
    last_date = last_row["date"]

    for h in range(1, HORIZON + 1):

        next_date = last_date + pd.Timedelta(weeks=1)

        # ==================================================
        # Calendar features
        # ==================================================

        year = next_date.year
        month = next_date.month
        quarter = next_date.quarter
        week = int(next_date.isocalendar().week)
        dayofyear = next_date.dayofyear

        # ==================================================
        # Safe lag features
        # ==================================================

        def safe_lag(k):

            if len(sales_history) >= k:
                return sales_history[-k]

            return sales_history[0]

        lag_1 = safe_lag(1)
        lag_2 = safe_lag(2)
        lag_4 = safe_lag(4)
        lag_8 = safe_lag(8)
        lag_12 = safe_lag(12)
        lag_26 = safe_lag(26)

        # ==================================================
        # Rolling means
        # ==================================================

        rolling_mean_4 = np.mean(
            sales_history[-min(4, len(sales_history)):]
        )

        rolling_mean_8 = np.mean(
            sales_history[-min(8, len(sales_history)):]
        )

        # ==================================================
        # Rolling std
        # ==================================================

        rolling_std_4 = np.std(
            sales_history[-min(4, len(sales_history)):]
        )

        rolling_std_8 = np.std(
            sales_history[-min(8, len(sales_history)):]
        )

        # ==================================================
        # EMA
        # ==================================================

        ema_4 = (
            pd.Series(sales_history)
            .ewm(span=4)
            .mean()
            .iloc[-1]
        )

        ema_8 = (
            pd.Series(sales_history)
            .ewm(span=8)
            .mean()
            .iloc[-1]
        )

        # ==================================================
        # Build feature vector
        # ==================================================

        X_future = pd.DataFrame({

            "store": [store],
            "dept": [dept],

            "is_holiday": [False],

            "temperature": [last_row["temperature"]],
            "fuel_price": [last_row["fuel_price"]],

            "markdown1": [last_row["markdown1"]],
            "markdown2": [last_row["markdown2"]],
            "markdown3": [last_row["markdown3"]],
            "markdown4": [last_row["markdown4"]],
            "markdown5": [last_row["markdown5"]],

            "cpi": [last_row["cpi"]],
            "unemployment": [last_row["unemployment"]],

            "type": [last_row["type"]],
            "size": [last_row["size"]],

            "year": [year],
            "month": [month],
            "quarter": [quarter],
            "week": [week],
            "dayofyear": [dayofyear],

            "total_markdown": [last_row["total_markdown"]],

            "lag_1": [lag_1],
            "lag_2": [lag_2],
            "lag_4": [lag_4],
            "lag_8": [lag_8],
            "lag_12": [lag_12],
            "lag_26": [lag_26],

            "rolling_mean_4": [rolling_mean_4],
            "rolling_mean_8": [rolling_mean_8],

            "rolling_std_4": [rolling_std_4],
            "rolling_std_8": [rolling_std_8],

            "ema_4": [ema_4],
            "ema_8": [ema_8]

        })

        # ==================================================
        # Forecast
        # ==================================================

        forecast = model.predict(
            X_future
        )[0]

        forecast = max(
            forecast,
            0
        )

        # ==================================================
        # Save
        # ==================================================

        forecast_rows.append({

            "store": store,
            "dept": dept,
            "forecast_week": h,
            "date": next_date,
            "forecast_sales": forecast

        })

        # ==================================================
        # Update history recursively
        # ==================================================

        sales_history.append(
            forecast
        )

        last_date = next_date

# ==========================================================
# Save Forecasts
# ==========================================================

forecast_df = pd.DataFrame(
    forecast_rows
)

forecast_df.to_csv(
    "outputs/forecast_results.csv",
    index=False
)

print()

print("Forecasting complete.")

print()

print(
    forecast_df.head()
)

# ==========================================================
# Portfolio-level Forecast Plot
# ==========================================================

portfolio_forecast = (
    forecast_df
    .groupby(
        "forecast_week"
    )["forecast_sales"]
    .sum()
)

plt.figure(
    figsize=(10,6)
)

portfolio_forecast.plot(
    marker="o"
)

plt.xlabel(
    "Forecast Week"
)

plt.ylabel(
    "Total Demand"
)

plt.title(
    "Portfolio Demand Forecast"
)

plt.grid()

plt.tight_layout()

plt.savefig(
    "outputs/forecast_plot.png"
)

plt.close()

print()

print("Files generated:")

print("forecast_results.csv")
print("forecast_plot.png")