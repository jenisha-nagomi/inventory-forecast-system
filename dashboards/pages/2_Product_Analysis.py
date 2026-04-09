import streamlit as st
import pandas as pd
import altair as alt

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Product Inventory Analysis",
    layout="wide"
)

# -------------------------------------------------
# Page Title
# -------------------------------------------------
st.title("Product Inventory Analysis")

st.markdown(
"""
This section provides product-level insights based on forecasted demand
and calculated reorder points. Select a product to view detailed
inventory metrics and demand forecasts.
"""
)

st.markdown("---")

# -------------------------------------------------
# Load Data
# -------------------------------------------------
reorder_df = pd.read_csv("outputs/tables/reorder_summary.csv")
forecast_df = pd.read_csv("outputs/tables/forecast_results.csv")

# -------------------------------------------------
# Product Selection
# -------------------------------------------------
product_list = reorder_df["Product"].unique()

selected_product = st.selectbox(
    "Select Product",
    product_list
)

product_row = reorder_df[reorder_df["Product"] == selected_product].iloc[0]

# -------------------------------------------------
# KPI Metrics
# -------------------------------------------------
st.subheader("Inventory Metrics")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Lead Time Demand", product_row["Lead Time Demand"])
c2.metric("Safety Stock", product_row["Safety Stock"])
c3.metric("Reorder Point", product_row["Reorder Point"])
c4.metric("Current Stock", product_row["Current Stock"])
c5.metric("Recommended Order Quantity", product_row["Order Quantity"])

st.markdown("---")

# -------------------------------------------------
# Forecast Trend
# -------------------------------------------------
st.subheader("Forecasted Demand Trend")

product_fc = forecast_df[
    forecast_df["Product Name"] == selected_product
].copy()

product_fc["Date"] = pd.to_datetime(product_fc["Date"])

chart = (
    alt.Chart(product_fc)
    .mark_line(point=True)
    .encode(
        x=alt.X("Date:T", title="Date"),
        y=alt.Y("ARIMA:Q", title="Forecasted Demand"),
        tooltip=["Date", "ARIMA"]
    )
    .properties(height=350)
)

st.altair_chart(chart, use_container_width=True)

st.markdown("---")

# -------------------------------------------------
# Inventory Status
# -------------------------------------------------
st.subheader("Inventory Status")

if product_row["Status"] == "Reorder":

    st.warning(
        f"""
Inventory level for **{selected_product}** is currently below the calculated reorder point.

Recommended order quantity: **{int(product_row['Order Quantity'])} units**
"""
    )

else:

    st.success(
        f"""
Inventory level for **{selected_product}** is currently above the reorder point.

No immediate replenishment is required.
"""
    )