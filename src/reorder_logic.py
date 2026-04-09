# src/reorder_logic.py

import pandas as pd
import numpy as np
from scipy.stats import norm

# -------------------------------------------------
# Safety Stock Calculation
# -------------------------------------------------

def compute_safety_stock(std, lead_time, z):
    """Calculate safety stock using Z × Std × sqrt(Lead Time)."""
    if pd.isna(std) or std == 0:
        std = 1  # fallback for zero variability
    return np.ceil(z * std * np.sqrt(lead_time))


# -------------------------------------------------
# Reorder Table (Per Product)
# -------------------------------------------------

def compute_reorder_table(
    forecast_df,
    historical_df,
    lead_time=7,
    service_level=0.95,
    forecast_horizon=14
):
    z = norm.ppf(service_level)
    products = forecast_df["Product Name"].unique()
    results = []

    for product in products:

        fcast = forecast_df[forecast_df["Product Name"] == product]
        hist = historical_df[historical_df["Product Name"] == product]

        # Lead Time Demand
        ltd = np.ceil(fcast["ARIMA"].head(lead_time).sum())

        # Historical Std
        std = hist["Order Item Quantity"].std()

        # Safety Stock
        ss = compute_safety_stock(std, lead_time, z)

        # Reorder Point
        rop = ltd + ss

        # Forecast Cycle Demand
        cycle_demand = np.ceil(fcast["ARIMA"].head(forecast_horizon).sum())

        # Simulated Current Stock (placeholder for ERP)
        current = int(np.floor(ltd * np.random.uniform(0.6, 1.2)))

        # Decision Logic
        if current < rop:
            status = "Reorder"
            order_qty = max(0, int(np.ceil(cycle_demand + ss - current)))
        else:
            status = "Stock OK"
            order_qty = 0

        results.append([
            product, ltd, ss, rop, cycle_demand, current, order_qty, status
        ])

    reorder_df = pd.DataFrame(results, columns=[
        "Product",
        "Lead Time Demand",
        "Safety Stock",
        "Reorder Point",
        "Forecast Cycle Demand (14d)",
        "Current Stock",
        "Order Quantity",
        "Status"
    ])

    reorder_df["Risk Level"] = np.where(
        reorder_df["Status"] == "Reorder",
        "🔴 High Risk",
        "🟢 Safe"
    )

    reorder_df = reorder_df.sort_values(
        by=["Status", "Order Quantity"],
        ascending=[True, False]
    ).reset_index(drop=True)

    return reorder_df


# -------------------------------------------------
# Warehouse-Level KPIs
# -------------------------------------------------

def compute_warehouse_summary(reorder_df):
    total_products = len(reorder_df)
    products_reorder = (reorder_df["Status"] == "Reorder").sum()
    total_order_qty = reorder_df["Order Quantity"].sum()

    reorder_rate = (products_reorder / total_products) * 100

    return pd.DataFrame({
        "Total Products": [total_products],
        "Products Needing Reorder": [products_reorder],
        "Total Order Quantity": [total_order_qty],
        "Reorder Rate (%)": [round(reorder_rate, 2)]
    })