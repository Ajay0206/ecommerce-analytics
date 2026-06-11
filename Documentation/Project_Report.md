# Project Report
# E-Commerce Sales & Customer Analytics Dashboard
# ============================================================

## 1. Executive Summary

This project builds a complete end-to-end data analytics solution for a
fictional Indian e-commerce company. Starting from scratch — designing the
database, generating realistic data, cleaning and analysing it in Python,
and finally presenting findings through a Power BI dashboard — it covers
every stage of a professional data analyst's workflow.

**Business Goal**: Give the e-commerce leadership team a single source of
truth for revenue performance, customer behaviour, and product analytics.

---

## 2. Problem Statement

The company has siloed data across orders, customers, products, and shipping
systems. Stakeholders lack:
- A single view of total revenue and growth trends
- Visibility into which products and categories drive profit
- Understanding of customer loyalty and churn patterns
- Regional sales performance breakdowns

---

## 3. Project Phases

### Phase 1 — Dataset Creation
Generated 11,683 records across 6 CSV files using Python's Faker library
with an Indian locale. Data covers Jan 2022 – Jun 2024 and includes realistic
pricing, geographies (16 Indian cities), order statuses, and payment methods.

### Phase 2 — Database Design
Designed a 3NF-normalised MySQL schema with:
- 6 tables (categories, products, customers, orders, order_items, shipping)
- Primary keys on all tables
- Foreign keys enforcing referential integrity
- Indexes on high-frequency JOIN and filter columns

### Phase 3 — SQL Analysis
Wrote 15 analytical queries covering:
- Revenue KPIs and YoY growth using LAG() window function
- Top products and categories by revenue and units sold
- Customer retention and churn using CTEs
- Region-wise and city-wise breakdowns
- Order fulfilment and payment method analysis

### Phase 4 — Python Data Cleaning & KPI Calculation
- Loaded all 6 CSVs into Pandas DataFrames
- Resolved null values (shipping dates, optional fields)
- Removed duplicates; validated price/quantity constraints
- Engineered 7 new features: age, tenure_months, age_group,
  year, month, quarter, day_of_week, delivery_delay_days
- Built a denormalised master table (5,852 rows) for fast aggregation
- Calculated 10 KPIs and performed RFM segmentation

### Phase 5 — EDA & Visualizations
Created 12 charts:

| # | Chart | Type | Insight |
|---|-------|------|---------|
| 1 | Monthly Revenue Trend | Line | Seasonal patterns |
| 2 | Top 10 Products | Horizontal Bar | Revenue drivers |
| 3 | Category Share | Donut | Category mix |
| 4 | Region Revenue | Bar | Geographic performance |
| 5 | Order Status | Bar | Fulfilment health |
| 6 | Payment Methods | Horizontal Bar | Payment preferences |
| 7 | Customer Age | Histogram | Demographics |
| 8 | RFM Segments | Bar | Customer loyalty |
| 9 | Category × Month | Heatmap | Seasonality by category |
| 10 | Top 10 Customers LTV | Horizontal Bar | VIP customers |
| 11 | Revenue by Day | Bar | Weekly patterns |
| 12 | Price Distribution | Box Plot | Pricing strategy |

### Phase 6 — Power BI Dashboard
Designed 4 dashboard pages with 10+ DAX measures and cross-filter slicers.
See `PowerBI_Files/PowerBI_Dashboard_Guide.md` for full setup instructions.

---

## 4. Key Findings

1. **Electronics and Fashion** are the top two revenue categories, contributing
   over 40% of total revenue combined.

2. **South India** (Bangalore, Hyderabad, Chennai, Tirupati) generates the
   highest regional revenue, driven by higher product price points.

3. **89% customer retention rate** indicates strong repeat-purchase behaviour;
   however, a 46.5% churn rate (no orders in 6 months) signals a re-engagement
   opportunity.

4. **RFM analysis** reveals 250 Champions + Loyal Customers (50% of active
   base) who deserve loyalty programme investment.

5. **UPI and Credit Card** together account for over 60% of payments, consistent
   with India's digital payment trends.

6. **Weekday orders** slightly outperform weekends in total revenue, suggesting
   B2C buying behaviour during work hours.

---

## 5. Recommendations

1. Launch a loyalty programme targeting the 124 Champion customers.
2. Run re-engagement email campaigns for 223 churned customers.
3. Expand Electronics inventory for South India fulfilment centres.
4. Introduce weekend-only flash sales to boost weekend revenue share.
5. Negotiate better rates with BlueDart/Delhivery given high shipment volumes.

---

## 6. Tools & Libraries

| Tool/Library | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Core scripting language |
| Pandas | 2.x | Data manipulation |
| NumPy | 1.x | Numerical operations |
| Matplotlib | 3.x | Base visualisation |
| Seaborn | 0.x | Statistical charts |
| Faker | 20.x | Synthetic data generation |
| MySQL | 8.0 | Relational database |
| Power BI Desktop | Latest | Interactive dashboard |
| xlsxwriter | - | Excel export |

---

## 7. Learning Outcomes

After completing this project, you will be able to:
- Design a normalised relational database schema from scratch
- Write complex SQL queries using window functions, CTEs, and subqueries
- Build a complete Python ETL pipeline for data cleaning and transformation
- Perform RFM customer segmentation
- Create professional data visualisations
- Build a multi-page Power BI dashboard with DAX measures
- Document and present a data project for a GitHub portfolio

---

*Report prepared by Ajay Kumar | MCA Student | Data Analyst Fresher*
