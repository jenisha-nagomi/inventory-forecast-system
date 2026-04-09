import streamlit as st
import pandas as pd
import altair as alt

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Demand Forecast Analysis",
    layout="wide"
)

# -------------------------------------------------
# Page Title
# -------------------------------------------------
st.title("Demand Forecast Analysis")

st.markdown(
"""
This page visualizes forecasted product demand generated using the ARIMA
time-series forecasting model. The chart displays predicted demand for the
next 14 days for each product.

Select a product to view its forecast trend.
"""
)

st.markdown("---")

# -------------------------------------------------
# Load Forecast Data
# -------------------------------------------------
forecast_df = pd.read_csv("outputs/tables/forecast_results.csv")

# -------------------------------------------------
# Product Selection
# -------------------------------------------------
product_list = forecast_df["Product Name"].unique()

selected_product = st.selectbox(
    "Select Product",
    product_list
)

subset = forecast_df[
    forecast_df["Product Name"] == selected_product
].copy()

subset["Date"] = pd.to_datetime(subset["Date"])

# -------------------------------------------------
# Forecast Chart
# -------------------------------------------------
st.subheader("Forecasted Demand Trend")

chart = (
    alt.Chart(subset)
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

st.caption("Demand Forecast Visualization")