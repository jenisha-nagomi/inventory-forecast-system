# src/forecasting.py
"""
Forecasting Module for Smart Inventory System
---------------------------------------------
This module provides:
- Baseline forecasting models (Naive, MA7)
- ARIMA model training for each product (SKU)
- Multi-product forecasting engine
- Exportable forecast output used by the reorder system
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import timedelta
import warnings
warnings.filterwarnings("ignore")

# -------------------------------------------------
# Evaluation Metrics
# -------------------------------------------------

def mae(y_true, y_pred):
    """Mean Absolute Error."""
    return np.mean(np.abs(y_true - y_pred))


def rmse(y_true, y_pred):
    """Root Mean Squared Error."""
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


# -------------------------------------------------
# Prepare Continuous Time Series
# -------------------------------------------------

def create_continuous_ts(df):
    """
    Convert demand series into a continuous daily time series
    by filling missing dates with zero demand.
    """
    df = df.sort_values("order date (DateOrders)")
    ts = df.set_index("order date (DateOrders)")["Order Item Quantity"]

    full_index = pd.date_range(start=ts.index.min(), end=ts.index.max(), freq="D")
    ts_full = ts.reindex(full_index, fill_value=0)

    return ts_full


# -------------------------------------------------
# Forecast Engine for Single Product
# -------------------------------------------------

def forecast_single_product(daily_demand_df, product_name, horizon=14):
    """
    Train ARIMA(1,1,1) and forecast future demand for a single product.
    Returns a DataFrame with forecasted dates and values.
    """

    # Filter rows for selected product
    product_df = daily_demand_df[
        daily_demand_df["Product Name"] == product_name
    ]

    # Build continuous time series
    ts_full = create_continuous_ts(product_df)

    # Skip if insufficient data
    if len(ts_full) < 30:
        return None

    # Train/Test split (80/20)
    split_idx = int(len(ts_full) * 0.8)
    train = ts_full.iloc[:split_idx]
    test = ts_full.iloc[split_idx:]

    # Baseline models
    naive_forecast = pd.Series(train.iloc[-1], index=test.index)
    ma_forecast = pd.Series(train.tail(7).mean(), index=test.index)

    # ARIMA model
    try:
        model = SARIMAX(
            train,
            order=(1, 1, 1),
            trend="n",
            enforce_stationarity=False,
            enforce_invertibility=False
        )
        result = model.fit(disp=False)

        # Forecast test period
        test_forecast = result.forecast(steps=len(test))
        test_forecast.index = test.index

        # Final model for future forecast
        final_model = SARIMAX(
            ts_full,
            order=(1, 1, 1),
            trend="n",
            enforce_stationarity=False,
            enforce_invertibility=False
        )
        final_result = final_model.fit(disp=False)
        future_forecast = final_result.forecast(steps=horizon)

        # Create future dates
        forecast_dates = pd.date_range(
            start=ts_full.index.max() + timedelta(days=1),
            periods=horizon,
            freq="D"
        )

        # Build DataFrame
        out_df = pd.DataFrame({
            "Date": forecast_dates,
            "Product Name": product_name,
            "ARIMA": [max(0, val) for val in future_forecast]
        })

        return out_df

    except:
        return None


# -------------------------------------------------
# Forecast All Products
# -------------------------------------------------

def forecast_all_products(daily_demand_df, horizon=14):
    """
    Runs ARIMA forecasting for every product in the dataset.
    Returns a single merged DataFrame.
    """

    all_products = daily_demand_df["Product Name"].unique()
    all_results = []

    for product in all_products:
        result = forecast_single_product(daily_demand_df, product, horizon)

        if result is not None:
            all_results.append(result)

    if len(all_results) == 0:
        return pd.DataFrame(columns=["Date", "Product Name", "ARIMA"])

    return pd.concat(all_results, ignore_index=True)


# -------------------------------------------------
# Export Forecast Output
# -------------------------------------------------

def save_forecast_results(df, save_path):
    """Save forecast results to CSV."""
    df.to_csv(save_path, index=False)