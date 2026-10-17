# E-Commerce Intelligence Dashboard

An interactive business intelligence dashboard built with **Python, Streamlit, Pandas, Plotly, and SciPy** to explore e-commerce order activity, product performance, order outcomes, marketing channels, and customer shopping behaviour.

The project focuses on making order data understandable and useful for business decision-making. In addition to interactive visualizations, it provides plain-language findings, business impacts, and recommendations based on the selected filters.

## Features

- **Executive overview:** Order counts, total order value, fulfillment and cancellation/return metrics.
- **Product performance:** Compare product-level cancellation and return rates.
- **Order activity:** Explore monthly order trends and order-status distribution.
- **Marketing analysis:** Compare referral-source volume and order quality.
- **Shopping-cart analysis:** Explore cart size and its relationship to order outcomes.
- **Coupon analysis:** Compare coupon usage and order outcomes.
- **Key findings and chart insights:** A "Key findings" summary and an "Explore Insights" button on each chart explain what the data shows, why it matters, and what to do next. Both update with the filters.
- **Drill-downs:** Click KPI cards to inspect supporting data.
- **Filters:** Explore results by year, product, and referral source.
- **Pending order check:** Flags how many orders are still marked Pending and how old the oldest one is.
- **Order records and export:** Browse individual orders and download the cancelled or returned orders as a CSV.

## Technology

- Python
- Pandas — data processing and analysis
- Plotly — interactive charts
- Streamlit — dashboard interface and deployment
- SciPy — chi-square tests to check whether cancellation and return percentages differ clearly between groups
- Git/GitHub — version control and source-code hosting
- Streamlit Community Cloud — live deployment

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
├── verify_statistics.py
├── requirements.txt
└── README.md
```

## Statistical checks

The dashboard uses SciPy chi-square tests to check whether cancellation and return rates differ clearly across products, referral sources, cart sizes, and coupon groups. The results are recalculated when filters change. The `verify_statistics.py` script independently checks the full-data tests. These tests do not prove causes or that groups are identical.

## Key finding

About 41% of orders were cancelled or returned. Chi-square tests found no meaningful difference across products, referral sources, cart sizes or coupons, which points to a business-wide issue rather than a problem with one product or channel.

## How to interpret the financial figures

**Total order value** is the sum of order amounts in the dataset. It is **not verified revenue received** because the data includes cancelled, returned, pending, and in-transit orders. Likewise, cancelled or returned order value should not be described as confirmed financial loss. Actual revenue, refunds, costs, and profit would require additional transaction and accounting data.

## Purpose

This is a hands-on data analytics portfolio project demonstrating data preparation, exploratory analysis, KPI design, interactive visualization, and communication of business findings. Recommendations identify areas for investigation rather than asserting causes that the dataset cannot establish.

## Live dashboard

https://ecommerce-intelligence-dashboard-edrnwcrmk9f45w4u8sbn4e.streamlit.app/


## Source code

https://github.com/indiya88/ecommerce-intelligence-dashboard
