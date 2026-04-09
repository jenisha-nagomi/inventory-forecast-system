# src/data_processing.py
"""
Data Processing Module for Smart Inventory System
-------------------------------------------------
This module handles:
- Loading raw dataset
- Filtering completed orders
- Cleaning datetime fields
- Aggregating daily demand per product
- Creating continuous time-series for forecasting
"""

import pandas as pd


# -------------------------------------------------
# 1. Load Raw Dataset
# -------------------------------------------------
def load_raw_data(path, usecols=None):
    """
    Load the warehouse dataset with selected columns.
    """
    df = pd.read_csv(path, usecols=usecols, encoding="latin1")
    return df


# -------------------------------------------------
# 2. Clean & Filter the Dataset
# -------------------------------------------------
def clean_and_filter(df):
    """
    Keep only completed/closed orders and convert dates.
    Returns cleaned dataframe.
    """
    df = df[df["Order Status"].isin(["COMPLETE", "CLOSED"])].copy()
    df["order date (DateOrders)"] = pd.to_datetime(df["order date (DateOrders)"])
    return df


# -------------------------------------------------
# 3. Daily Demand Aggregation
# -------------------------------------------------
def aggregate_daily_demand(df):
    """
    Convert raw orders into daily aggregated demand per product.
    """
    daily = (
        df.groupby(
            [
                pd.Grouper(key="order date (DateOrders)", freq="D"),
                "Product Name"
            ]
        )["Order Item Quantity"]
        .sum()
        .reset_index()
    )
    return daily


# -------------------------------------------------
# 4. Create Continuous Time-Series for Forecasting
# -------------------------------------------------
def create_timeseries_per_product(daily_df, product_name):
    """
    Extract continuous daily time series for a selected product.
    Missing days are filled with zero demand.
    """
    product_df = (
        daily_df[daily_df["Product Name"] == product_name]
        .sort_values("order date (DateOrders)")
        .copy()
    )

    ts = product_df.set_index("order date (DateOrders)")["Order Item Quantity"]

    full_index = pd.date_range(start=ts.index.min(), end=ts.index.max(), freq="D")
    ts_full = ts.reindex(full_index, fill_value=0)

    return ts_full


# -------------------------------------------------
# 5. Helper Functions
# -------------------------------------------------
def get_sample_product(daily_df):
    """
    Returns the product with the highest number of entries.
    Useful for EDA plots.
    """
    return daily_df["Product Name"].value_counts().index[0]


def get_date_range(daily_df):
    """
    Returns the start and end date of the aggregated dataset.
    """
    start = daily_df["order date (DateOrders)"].min()
    end = daily_df["order date (DateOrders)"].max()
    return start, end


# -------------------------------------------------
# 6. Run Processing (when executed directly)
# -------------------------------------------------
if __name__ == "__main__":

    cols = [
        "order date (DateOrders)",
        "Product Name",
        "Order Item Quantity",
        "Order Status"
    ]

    print("Loading raw dataset...")

    df = load_raw_data("data/raw/DataCoSupplyChainDataset.csv", usecols=cols)

    print("Cleaning dataset...")
    df = clean_and_filter(df)

    print("Aggregating daily demand...")
    daily_demand = aggregate_daily_demand(df)

    print("Saving processed dataset...")

    daily_demand.to_csv("data/processed/daily_demand.csv", index=False)

    print("Data processing completed successfully.")