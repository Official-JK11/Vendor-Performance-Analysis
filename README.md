# Vendor-Performance-Analysis
# Vendor Performance Data Analytics Project

A complete end-to-end data analytics case study focusing on **vendor performance**, built with **SQL** and **Python**.  

---

## 🚀 Project Overview

The goal of this project is to analyze vendor purchase and sales data to uncover actionable insights such as:

- Which vendors contribute the most to overall purchases
- Confidence intervals for profit margins (Top vs. Low vendors)
- Impact of bulk purchasing on unit prices and margins
- Comparative distribution of profit margins across vendors
- Pareto analysis (80/20 contribution of vendors)

---

## 📂 Repository Structure

```plaintext
├── data/
│   ├── raw/              # Original raw dataset (CSV/SQL dump)
│   └── processed/        # Cleaned/transformed data
│
├── sql/
│   ├── create_tables.sql # Database schema setup
│   └── queries.sql       # SQL queries for data extraction
│
├── notebooks/
│   ├── eda.ipynb         # Exploratory data analysis
│   └── stats.ipynb       # Confidence intervals, distributions, tests
│
├── scripts/
│   ├── analysis.py       # Main Python analysis script
│   └── utils.py          # Helper functions (e.g., CI calculator)
│
├── README.md
├── requirements.txt      # Python dependencies
└── LICENSE
