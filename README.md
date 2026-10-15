# E-Commerce Intelligence Dashboard

An interactive business intelligence dashboard built with **Python, Streamlit, Pandas, and Plotly** to explore e-commerce order activity, product performance, order outcomes, marketing channels, and customer shopping behaviour.

The project focuses on making order data understandable and useful for business decision-making. In addition to interactive visualizations, it provides plain-language findings, business impacts, and recommendations based on the selected filters.

## Features

- **Executive overview:** Order counts, total order value, fulfillment and cancellation/return metrics.
- **Product performance:** Compare product-level cancellation and return rates.
- **Order activity:** Explore monthly order trends and order-status distribution.
- **Marketing analysis:** Compare referral-source volume and order quality.
- **Shopping-cart analysis:** Explore cart size and its relationship to order outcomes.
- **Coupon analysis:** Compare coupon usage and order outcomes.
- **Interactive insights:** Chart-specific insights and an executive summary that respond to dashboard filters.
- **Drill-downs:** Click KPI cards to inspect supporting data.
- **Filters:** Explore results by year, product, and referral source.

## Technology

- Python
- Pandas — data processing and analysis
- Plotly — interactive charts
- Streamlit — dashboard interface and deployment

## Run locally

1. Clone the repository and open its folder.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the dashboard:

   ```bash
   python -m streamlit run app.py
   ```

The dashboard expects the cleaned dataset in `data/cleaned_E-Commerce Orders.csv`.

## Project structure

```text
├── .streamlit/
│   └── config.toml
├── data/
│   └── cleaned_E-Commerce Orders.csv
├── app.py
├── insights.py
├── requirements.txt
└── README.md
```

## How to interpret the financial figures

**Total order value** is the sum of order amounts in the dataset. It is **not verified revenue received** because the data includes cancelled, returned, pending, and in-transit orders. Likewise, cancelled or returned order value should not be described as confirmed financial loss. Actual revenue, refunds, costs, and profit would require additional transaction and accounting data.

## Purpose

This is a hands-on data analytics portfolio project demonstrating data preparation, exploratory analysis, KPI design, interactive visualization, and communication of business findings. Recommendations identify areas for investigation rather than asserting causes that the dataset cannot establish.

## Live dashboard

A Streamlit Community Cloud link can be added here after deployment.
