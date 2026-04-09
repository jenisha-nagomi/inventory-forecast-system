import streamlit as st
import pandas as pd
import altair as alt

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Warehouse Overview",
    layout="wide"
)

# -------------------------------------------------
# Page Title
# -------------------------------------------------
st.title("Warehouse Inventory Overview")
st.markdown(
"""
This dashboard provides a high-level overview of warehouse inventory status.
It highlights products that require replenishment based on forecast-driven
reorder point calculations.
"""
)

st.markdown("---")

# -------------------------------------------------
# Load Data
# -------------------------------------------------
reorder_df = pd.read_csv("outputs/tables/reorder_summary.csv")
summary_df = pd.read_csv("outputs/tables/warehouse_summary.csv")

# -------------------------------------------------
# KPI Metrics
# -------------------------------------------------
st.subheader("Warehouse Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Total Products",
    value=int(summary_df["Total Products"].iloc[0])
)

col2.metric(
    label="Products Requiring Reorder",
    value=int(summary_df["Products Needing Reorder"].iloc[0])
)

col3.metric(
    label="Reorder Rate (%)",
    value=f"{summary_df['Reorder Rate (%)'].iloc[0]}"
)

col4.metric(
    label="Total Order Quantity",
    value=int(summary_df["Total Order Quantity"].iloc[0])
)

st.markdown("---")

# -------------------------------------------------
# Inventory Risk Distribution
# -------------------------------------------------
st.subheader("Inventory Risk Distribution")

risk_data = (
    reorder_df.groupby("Risk Level")
    .size()
    .reset_index(name="Count")
)

if len(risk_data) > 0:

    risk_chart = (
        alt.Chart(risk_data)
        .mark_arc(innerRadius=50)
        .encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="Risk Level", type="nominal"),
            tooltip=["Risk Level", "Count"]
        )
        .properties(height=350)
    )

    st.altair_chart(risk_chart, use_container_width=True)

else:
    st.info("Risk distribution data is not available.")

st.markdown("---")

# -------------------------------------------------
# High Risk Products Table
# -------------------------------------------------
st.subheader("Products Requiring Replenishment")

st.markdown(
"""
The following products currently have stock levels below the calculated
reorder point (ROP) and should be prioritized for replenishment.
"""
)

risky_products = reorder_df[reorder_df["Status"] == "Reorder"]

def highlight_reorder(row):
    if row["Status"] == "Reorder":
        return ["background-color:#f8d7da"] * len(row)
    return [""] * len(row)

st.dataframe(
    risky_products.style.apply(highlight_reorder, axis=1),
    use_container_width=True,
    height=350
)

st.markdown("---")

st.caption("Inventory Forecasting and Replenishment Decision Support System")