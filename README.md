# 🛒 E-Commerce Sales & Customer Analytics Dashboard

> **End-to-end Data Analyst portfolio project** — from raw data generation to
> SQL analysis, Python EDA, and an interactive Power BI dashboard.

---

## 📌 Project Overview

This project simulates a real-world e-commerce analytics pipeline for a
fictional Indian online retailer. It demonstrates the full data analyst
workflow: schema design, data cleaning, exploratory analysis, KPI reporting,
customer segmentation, and professional dashboarding.

| Attribute | Detail |
|-----------|--------|
| **Domain** | E-Commerce / Retail Analytics |
| **Dataset** | Synthetically generated (Faker + NumPy) |
| **Records** | ~11,700 rows across 6 tables |
| **Time Span** | Jan 2022 – Jun 2024 |
| **Tools** | MySQL · Python · Power BI · Excel |

---

## 🎯 Business Questions Answered

- What is the total revenue, and how has it trended month-over-month?
- Which product categories and individual products drive the most revenue?
- Which regions and cities generate the highest sales?
- Who are the top customers by lifetime value?
- What is the customer retention rate and churn rate?
- How are customers segmented by purchase behaviour (RFM)?
- What is the average order value, and how does it vary by month?
- Which payment methods are most popular?

---

## 🗂️ Project Structure

```
ecommerce_analytics/
│
├── Dataset/
│   ├── categories.csv
│   ├── products.csv
│   ├── customers.csv
│   ├── orders.csv
│   ├── order_items.csv
│   ├── shipping.csv
│   └── cleaned_data.xlsx          ← multi-sheet cleaned output
│
├── SQL_Scripts/
│   ├── 01_create_schema.sql       ← DB + tables with PKs, FKs, indexes
│   ├── 02_insert_data.sql         ← Bulk INSERT statements
│   └── 03_analysis_queries.sql    ← 15+ business queries
│
├── Python_Scripts/
│   ├── 01_generate_dataset.py     ← Faker-based synthetic data generator
│   ├── 02_generate_sql_inserts.py ← CSV → SQL INSERT converter
│   ├── 03_data_cleaning_kpi.py    ← Cleaning, feature engineering, RFM
│   └── 04_eda_visualizations.py   ← 12 Matplotlib / Seaborn charts
│
├── Visualizations/
│   ├── 01_monthly_revenue_trend.png
│   ├── 02_top10_products_revenue.png
│   ├── 03_category_revenue_pie.png
│   ├── 04_region_revenue.png
│   ├── 05_order_status.png
│   ├── 06_payment_methods.png
│   ├── 07_customer_age_distribution.png
│   ├── 08_rfm_segments.png
│   ├── 09_category_month_heatmap.png
│   ├── 10_top10_customers_ltv.png
│   ├── 11_revenue_by_day_of_week.png
│   └── 12_price_distribution_by_category.png
│
├── PowerBI_Files/
│   ├── PowerBI_Dashboard_Guide.md ← Step-by-step Power BI setup
│   └── ecommerce_dashboard.pbix   ← (build manually using guide)
│
├── Documentation/
│   ├── Project_Report.md
│   └── resume_bullets.md
│
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Database | MySQL 8.0 |
| Data Generation | Python · Faker · NumPy |
| Data Analysis | Python · Pandas · NumPy |
| Visualisation | Matplotlib · Seaborn |
| BI Dashboard | Microsoft Power BI Desktop |
| Export | Excel (xlsxwriter) |

---

## 🚀 Quick Start

### 1 — Clone the Repository
```bash
git clone https://github.com/Ajay0206/ecommerce-analytics.git
cd ecommerce-analytics
```

### 2 — Install Python Dependencies
```bash
pip install pandas numpy matplotlib seaborn faker sqlalchemy \
            mysql-connector-python openpyxl xlsxwriter
```

### 3 — Generate the Dataset
```bash
python Python_Scripts/01_generate_dataset.py
```

### 4 — Set Up the MySQL Database
```sql
-- In MySQL Workbench or CLI:
source SQL_Scripts/01_create_schema.sql
source SQL_Scripts/02_insert_data.sql
```

### 5 — Run Analysis Queries
```sql
source SQL_Scripts/03_analysis_queries.sql
```

### 6 — Run Python Analysis
```bash
python Python_Scripts/03_data_cleaning_kpi.py
python Python_Scripts/04_eda_visualizations.py
```

### 7 — Build Power BI Dashboard
Open `PowerBI_Files/PowerBI_Dashboard_Guide.md` and follow the steps.

---

## 📊 Key KPIs (from generated dataset)

| KPI | Value |
|-----|-------|
| Total Revenue | ₹3.42 Cr |
| Total Orders | 1,794 |
| Unique Customers | 480 |
| Avg Order Value | ₹1,90,732 |
| Customer Retention Rate | 89% |
| Churn Rate | 46.5% |
| RFM Champions | 124 customers |
| Loyal Customers | 126 customers |

---

## 🗃️ Database Schema (ERD Summary)

```
categories ──< products ──< order_items >── orders >── customers
                                                 │
                                              shipping
```

- **categories** → **products**: one category has many products
- **products** → **order_items**: one product appears in many line items
- **orders** → **order_items**: one order has many line items
- **customers** → **orders**: one customer places many orders
- **orders** → **shipping**: one-to-one fulfilment record

---

## 📈 Power BI Dashboard Pages

| Page | Purpose |
|------|---------|
| Executive Dashboard | High-level KPIs + revenue trend + category share |
| Sales Dashboard | Monthly trends + product performance + payment analysis |
| Customer Dashboard | RFM segments + demographics + top customers |
| Product Dashboard | Ratings + stock levels + price distribution |

---

## 🔍 SQL Analysis Highlights

- **Window functions** (LAG, RANK) for YoY growth and customer ranking
- **CTEs** for readable multi-step analysis (churn, retention)
- **Aggregate functions** for KPI calculations
- **CASE expressions** for customer segmentation
- **JOINs** across all 6 normalised tables

---

## 👤 Author

**Ajay Kumar**
BCA Graduate | MCA Student | Aspiring Data Analyst
📧 nelloreajaykumar6@gmail.com
🐙 [github.com/Ajay0206](https://github.com/Ajay0206)

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

*Built as a portfolio project to demonstrate real-world data analyst skills
including SQL, Python, data cleaning, EDA, and dashboard development.*
