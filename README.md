
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

The project was implemented using the following tools and libraries:

* Python
* Pandas
* NumPy
* Matplotlib
* SciPy
* Statsmodels (ARIMA)
* Streamlit
* Altair

---


# How to Run the Project

Follow the steps below to run the complete system.

---

## 1. Install dependencies

From the project root directory run:

```
pip install -r requirements.txt
```

---

## 2. Process the raw dataset

Run the data processing script:

```
python src/data_processing.py
```

This script cleans the dataset and generates:

```
data/processed/daily_demand.csv
```

---

## 3. Run demand forecasting

Run the forecasting module:

```
python src/forecasting.py
```

This script trains the forecasting model and generates:

```
outputs/tables/forecast_results.csv
```

---

## 4. Run reorder calculations

Run the reorder logic:

```
python src/reorder_logic.py
```

This script calculates inventory decisions and generates:

```
outputs/tables/reorder_summary.csv
outputs/tables/warehouse_summary.csv
```

---

## 5. Launch the dashboard

After the output files are generated, start the dashboard:

```
streamlit run dashboards/Home.py
```

The dashboard will open in your browser and display:

* warehouse inventory KPIs
* product-level reorder alerts
* demand forecast trends
* inventory risk indicators

---

# Notebooks

The notebooks folder contains the analytical workflow used during development.

| Notebook                  | Purpose                                 |
| ------------------------- | --------------------------------------- |
| `01_eda.ipynb`            | data exploration and demand aggregation |
| `02_forecasting.ipynb`    | demand forecasting experiments          |
| `03_reorder_system.ipynb` | reorder logic testing                   |

These notebooks are mainly used for **analysis and documentation**, while the system itself runs using the **Python scripts in the `src` folder**.
