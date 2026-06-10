import pandas as pd
import numpy as np
import joblib

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

# ==========================================================
# Load Feature Engineered Dataset
# ==========================================================

print("Loading dataset...")

df = pd.read_csv(
    "outputs/feature_engineered_data.csv",
    parse_dates=["date"]
)

print("Shape:", df.shape)

# ==========================================================
# Encode categorical variables
# ==========================================================

type_mapping = {
    "A": 0,
    "B": 1,
    "C": 2
}

if df["type"].dtype == "object":
    df["type"] = df["type"].map(type_mapping)

# ==========================================================
# Sort by date
# ==========================================================

df = df.sort_values("date")

# ==========================================================
# Drop Date Column
# ==========================================================

X = df.drop(
    columns=[
        "weekly_sales",
        "date"
    ]
)

y = df["weekly_sales"]

# ==========================================================
# Chronological Train-Test Split
# ==========================================================

split_idx = int(
    len(df) * 0.8
)

X_train = X.iloc[:split_idx]
X_test = X.iloc[split_idx:]

y_train = y.iloc[:split_idx]
y_test = y.iloc[split_idx:]

print()
print("Train size:", X_train.shape)
print("Test size :", X_test.shape)

# ==========================================================
# XGBoost
# ==========================================================

print()
print("Training XGBoost...")

xgb_model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=8,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

xgb_model.fit(
    X_train,
    y_train
)

# ==========================================================
# LightGBM
# ==========================================================

print()
print("Training LightGBM...")

lgb_model = LGBMRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=8,
    random_state=42,
    n_jobs=-1
)

lgb_model.fit(
    X_train,
    y_train
)

# ==========================================================
# Predictions
# ==========================================================

xgb_pred = xgb_model.predict(
    X_test
)

lgb_pred = lgb_model.predict(
    X_test
)

# ==========================================================
# Metric Function
# ==========================================================

def evaluate_model(
    y_true,
    y_pred
):

    mae = mean_absolute_error(
        y_true,
        y_pred
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_true,
            y_pred
        )
    )

    r2 = r2_score(
        y_true,
        y_pred
    )

    mape = (
        np.mean(
            np.abs(
                (y_true - y_pred)
                /
                np.maximum(
                    y_true,
                    1
                )
            )
        )
        * 100
    )

    return (
        mae,
        rmse,
        r2,
        mape
    )

# ==========================================================
# Metrics
# ==========================================================

xgb_metrics = evaluate_model(
    y_test,
    xgb_pred
)

lgb_metrics = evaluate_model(
    y_test,
    lgb_pred
)

metrics_df = pd.DataFrame(

    {
        "Model": [
            "XGBoost",
            "LightGBM"
        ],

        "MAE": [
            xgb_metrics[0],
            lgb_metrics[0]
        ],

        "RMSE": [
            xgb_metrics[1],
            lgb_metrics[1]
        ],

        "R2": [
            xgb_metrics[2],
            lgb_metrics[2]
        ],

        "MAPE": [
            xgb_metrics[3],
            lgb_metrics[3]
        ]
    }

)

print()
print(metrics_df)

# ==========================================================
# Save Metrics
# ==========================================================

metrics_df.to_csv(
    "outputs/model_metrics.csv",
    index=False
)

# ==========================================================
# Save Models
# ==========================================================

joblib.dump(
    xgb_model,
    "models/xgb_model.pkl"
)

joblib.dump(
    lgb_model,
    "models/lgb_model.pkl"
)

print()
print("Models saved.")

# ==========================================================
# Select Best Model
# ==========================================================

if xgb_metrics[1] < lgb_metrics[1]:

    best_model = "XGBoost"

else:

    best_model = "LightGBM"

print()
print("Best Model:", best_model)