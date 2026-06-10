from fastapi import FastAPI
import pandas as pd

# ==========================================================
# Create app
# ==========================================================

app = FastAPI(
    title="Retail Demand Forecasting API",
    description="Forecasting and Inventory Optimization System",
    version="1.0"
)

# ==========================================================
# Load outputs once
# ==========================================================

forecast_df = pd.read_csv(
    "outputs/forecast_results.csv"
)

inventory_df = pd.read_csv(
    "outputs/inventory_recommendations.csv"
)

# ==========================================================
# Home
# ==========================================================

@app.get("/")
def home():

    return {
        "message":
        "Retail Demand Forecasting API is running"
    }

# ==========================================================
# Entire forecast table
# ==========================================================

@app.get("/forecast")
def get_forecasts():

    return forecast_df.to_dict(
        orient="records"
    )

# ==========================================================
# Entire inventory table
# ==========================================================

@app.get("/inventory")
def get_inventory():

    return inventory_df.to_dict(
        orient="records"
    )

# ==========================================================
# Forecast for one store
# ==========================================================

@app.get("/forecast/store/{store_id}")
def forecast_by_store(
    store_id: int
):

    result = forecast_df[
        forecast_df["store"] == store_id
    ]

    return result.to_dict(
        orient="records"
    )

# ==========================================================
# Inventory for one store
# ==========================================================

@app.get("/inventory/store/{store_id}")
def inventory_by_store(
    store_id: int
):

    result = inventory_df[
        inventory_df["store"] == store_id
    ]

    return result.to_dict(
        orient="records"
    )

# ==========================================================
# Forecast for one department
# ==========================================================

@app.get("/forecast/dept/{dept_id}")
def forecast_by_dept(
    dept_id: int
):

    result = forecast_df[
        forecast_df["dept"] == dept_id
    ]

    return result.to_dict(
        orient="records"
    )

# ==========================================================
# Inventory for one department
# ==========================================================

@app.get("/inventory/dept/{dept_id}")
def inventory_by_dept(
    dept_id: int
):

    result = inventory_df[
        inventory_df["dept"] == dept_id
    ]

    return result.to_dict(
        orient="records"
    )

# ==========================================================
# Store + Department forecast
# ==========================================================

@app.get("/forecast/{store_id}/{dept_id}")
def forecast_store_dept(
    store_id: int,
    dept_id: int
):

    result = forecast_df[
        (forecast_df["store"] == store_id)
        &
        (forecast_df["dept"] == dept_id)
    ]

    return result.to_dict(
        orient="records"
    )

# ==========================================================
# Store + Department inventory
# ==========================================================

@app.get("/inventory/{store_id}/{dept_id}")
def inventory_store_dept(
    store_id: int,
    dept_id: int
):

    result = inventory_df[
        (inventory_df["store"] == store_id)
        &
        (inventory_df["dept"] == dept_id)
    ]

    return result.to_dict(
        orient="records"
    )

# ==========================================================
# Summary statistics
# ==========================================================

@app.get("/summary")
def summary():

    return {

        "number_of_forecasts":
        len(forecast_df),

        "number_of_inventory_records":
        len(inventory_df),

        "total_forecasted_demand":
        float(
            forecast_df[
                "forecast_sales"
            ].sum()
        ),

        "average_order_quantity":
        float(
            inventory_df[
                "recommended_order_qty"
            ].mean()
        )
    }