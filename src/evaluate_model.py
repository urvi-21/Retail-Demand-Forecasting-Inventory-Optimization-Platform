import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ==========================================================
# Load Dataset
# ==========================================================

print("Loading dataset...")

df = pd.read_csv(
    "outputs/feature_engineered_data.csv",
    parse_dates=["date"]
)

# ==========================================================
# Encode Type if Needed
# ==========================================================

type_mapping = {
    "A": 0,
    "B": 1,
    "C": 2
}

if df["type"].dtype == "object":
    df["type"] = df["type"].map(type_mapping)

# ==========================================================
# Sort Chronologically
# ==========================================================

df = df.sort_values("date")

# ==========================================================
# Features and Target
# ==========================================================

X = df.drop(
    columns=[
        "weekly_sales",
        "date"
    ]
)

y = df["weekly_sales"]

# ==========================================================
# Chronological Split
# ==========================================================

split_idx = int(len(df) * 0.8)

X_train = X.iloc[:split_idx]
X_test = X.iloc[split_idx:]

y_train = y.iloc[:split_idx]
y_test = y.iloc[split_idx:]

# ==========================================================
# Load Best Model
# ==========================================================

print("Loading XGBoost model...")

model = joblib.load(
    "models/xgb_model.pkl"
)

# ==========================================================
# Predictions
# ==========================================================

y_pred = model.predict(X_test)

# ==========================================================
# Metrics
# ==========================================================

mae = mean_absolute_error(
    y_test,
    y_pred
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred
    )
)

r2 = r2_score(
    y_test,
    y_pred
)

# SMAPE

smape = (
    np.mean(
        2 *
        np.abs(
            y_test - y_pred
        )
        /
        (
            np.abs(y_test)
            +
            np.abs(y_pred)
            +
            1e-10
        )
    )
) * 100

# WAPE

wape = (
    np.sum(
        np.abs(
            y_test - y_pred
        )
    )
    /
    np.sum(
        np.abs(
            y_test
        )
    )
) * 100

# ==========================================================
# Save Metrics
# ==========================================================

metrics_df = pd.DataFrame({

    "Metric": [
        "MAE",
        "RMSE",
        "R2",
        "SMAPE",
        "WAPE"
    ],

    "Value": [
        mae,
        rmse,
        r2,
        smape,
        wape
    ]
})

metrics_df.to_csv(
    "outputs/evaluation_metrics.csv",
    index=False
)

print(metrics_df)

# ==========================================================
# Actual vs Predicted
# ==========================================================

plt.figure(figsize=(10,6))

plt.scatter(
    y_test,
    y_pred,
    alpha=0.3
)

plt.xlabel("Actual Sales")
plt.ylabel("Predicted Sales")
plt.title("Actual vs Predicted")

plt.savefig(
    "outputs/actual_vs_predicted.png"
)

plt.close()

# ==========================================================
# Residual Plot
# ==========================================================

residuals = y_test - y_pred

plt.figure(figsize=(10,6))

sns.histplot(
    residuals,
    bins=50,
    kde=True
)

plt.xlabel("Residual")

plt.title("Residual Distribution")

plt.savefig(
    "outputs/residual_plot.png"
)

plt.close()

# ==========================================================
# Feature Importance
# ==========================================================

importance_df = pd.DataFrame({

    "Feature": X.columns,

    "Importance": model.feature_importances_

})

importance_df = importance_df.sort_values(
    "Importance",
    ascending=False
)

importance_df.to_csv(
    "outputs/feature_importance.csv",
    index=False
)

# Top 20 features

plt.figure(figsize=(10,8))

sns.barplot(

    data=importance_df.head(20),

    x="Importance",

    y="Feature"

)

plt.title(
    "Top 20 Feature Importances"
)

plt.savefig(
    "outputs/feature_importance.png"
)

plt.close()

# ==========================================================
# SHAP Explainability
# ==========================================================

print("Computing SHAP values...")

explainer = shap.TreeExplainer(
    model
)

sample_size = min(
    5000,
    len(X_test)
)

X_sample = X_test.sample(
    sample_size,
    random_state=42
)

shap_values = explainer.shap_values(
    X_sample
)

plt.figure()

shap.summary_plot(

    shap_values,

    X_sample,

    show=False

)

plt.savefig(
    "outputs/shap_summary.png",
    bbox_inches="tight"
)

plt.close()

print()
print("Evaluation complete.")
print()
print("Files generated:")
print()

print("evaluation_metrics.csv")
print("actual_vs_predicted.png")
print("residual_plot.png")
print("feature_importance.csv")
print("feature_importance.png")
print("shap_summary.png")