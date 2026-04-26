# Project Structure

```
CAPSTONE_INVENTORY
│
├── .streamlit
│   └── config.toml
│
├── dashboards
│   ├── Home.py
│   └── pages
│       ├── 1_Warehouse_Overview.py
│       ├── 2_Product_Analysis.py
│       └── 3_Forecast_Explorer.py
│
├── data
│   ├── raw
│   │   └── DataCoSupplyChainDataset.csv
│   │
│   └── processed
│       └── daily_demand.csv
│
├── notebooks
│   ├── 01_eda.ipynb
│   ├── 02_forecasting.ipynb
│   └── 03_reorder_system.ipynb
│
├── outputs
│   ├── figures
│   │   ├── raw_vs_processed.png
│   │   ├── demand_trend.png
│   │   ├── overall_demand.png
│   │   ├── demand_histogram.png
│   │   ├── top_products.png
│   │   ├── forecast_comparison.png
│   │   ├── reorder_table.png
│   │   └── architecture_final.png
│   └── tables
│       ├── forecast_results.csv
│       ├── reorder_summary.csv
│       └── warehouse_summary.csv
│
├── src
│   ├── data_processing.py
│   ├── forecasting.py
│   └── reorder_logic.py
│
├── requirements.txt
└── README.md
```

---

# Technologies Used

- Python  
- Pandas  
- NumPy  
- Matplotlib  
- SciPy  
- Statsmodels (ARIMA)  
- Streamlit  
- Altair  

---

# How to Run the Project

## 1. Install dependencies

Windows:
```
pip install -r requirements.txt
```

macOS / Linux:
```
pip3 install -r requirements.txt
```

---

## 2. Process the raw dataset

Windows:
```
python src/data_processing.py
```

macOS / Linux:
```
python3 src/data_processing.py
```

Output:
```
data/processed/daily_demand.csv
```

---

## 3. Run demand forecasting

Windows:
```
python src/forecasting.py
```

macOS / Linux:
```
python3 src/forecasting.py
```

Output:
```
outputs/tables/forecast_results.csv
```

---

## 4. Run reorder calculations

Windows:
```
python src/reorder_logic.py
```

macOS / Linux:
```
python3 src/reorder_logic.py
```

Outputs:
```
outputs/tables/reorder_summary.csv
outputs/tables/warehouse_summary.csv
```

---

## 5. Launch the dashboard

Windows / macOS / Linux:
```
streamlit run dashboards/Home.py
```

If streamlit is not recognized:
```
python3 -m streamlit run dashboards/Home.py
```

The dashboard will display:

- warehouse inventory KPIs  
- product-level reorder alerts  
- demand forecast trends  
- inventory risk indicators  

---

# Notebooks

| Notebook | Purpose |
|----------|--------|
| 01_eda.ipynb | Data exploration and demand aggregation |
| 02_forecasting.ipynb | Forecasting experiments |
| 03_reorder_system.ipynb | Reorder logic testing |

These notebooks are used for analysis and documentation, while the system runs using the Python scripts in the `src` folder.
