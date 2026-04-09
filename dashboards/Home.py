import streamlit as st

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Inventory Forecasting System",
    layout="wide"
)

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("Inventory Forecasting and Replenishment System")

st.markdown(
"""
This application provides a decision-support dashboard for warehouse inventory management.

The system integrates demand forecasting with inventory control analytics to support
data-driven replenishment decisions.
"""
)

st.markdown("---")

# -------------------------------------------------
# System Capabilities
# -------------------------------------------------
st.subheader("System Capabilities")

st.markdown(
"""
The dashboard provides the following analytical features:

• Warehouse-level inventory risk monitoring  
• Product-level demand forecasting  
• Forecast-driven reorder recommendations  
• Safety stock and reorder point analysis  
• Historical demand and forecast comparison
"""
)

st.markdown("---")

# -------------------------------------------------
# Navigation Instructions
# -------------------------------------------------
st.subheader("Navigation")

st.markdown(
"""
Use the sidebar navigation to access the different analytical views:

• **Warehouse Overview** – summary KPIs and inventory risk distribution  
• **Product Analysis** – detailed inventory metrics for individual products  
• **Forecast Explorer** – historical demand and forecast visualization
"""
)

st.markdown("---")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption("Inventory Forecasting and Replenishment Decision Support System")