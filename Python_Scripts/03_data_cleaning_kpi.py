"""
============================================================
PHASE 4: DATA CLEANING, FEATURE ENGINEERING & KPI ANALYSIS
E-Commerce Sales & Customer Analytics Dashboard
============================================================
Input  : CSV files from Dataset/
Output : cleaned_data.xlsx in Dataset/
         Console KPI report
============================================================
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

BASE     = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "..", "Dataset")

print("=" * 60)
print("  PHASE 4 — Data Cleaning & KPI Analysis")
print("=" * 60)

# ─────────────────────────────────────────────────────────
# STEP 1: Load all datasets
# ─────────────────────────────────────────────────────────
print("\n[1] Loading datasets...")
categories  = pd.read_csv(os.path.join(DATA_DIR, "categories.csv"))
products    = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
customers   = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))
orders      = pd.read_csv(os.path.join(DATA_DIR, "orders.csv"))
order_items = pd.read_csv(os.path.join(DATA_DIR, "order_items.csv"))
shipping    = pd.read_csv(os.path.join(DATA_DIR, "shipping.csv"))

dfs = {"categories": categories, "products": products,
       "customers": customers, "orders": orders,
       "order_items": order_items, "shipping": shipping}
for name, df in dfs.items():
    print(f"   {name:<14}: {df.shape[0]:>5} rows × {df.shape[1]} cols")

# ─────────────────────────────────────────────────────────
# STEP 2: Data Quality Report
# ─────────────────────────────────────────────────────────
print("\n[2] Data Quality Check...")
for name, df in dfs.items():
    nulls = df.isnull().sum().sum()
    dups  = df.duplicated().sum()
    print(f"   {name:<14}: {nulls} nulls | {dups} duplicates")

# ─────────────────────────────────────────────────────────
# STEP 3: Data Cleaning
# ─────────────────────────────────────────────────────────
print("\n[3] Cleaning data...")

# ── Customers ────────────────────────────────────────────
# Fill any missing gender with 'Other'
customers["gender"].fillna("Other", inplace=True)
# Standardise phone: keep only digits and +, trim whitespace
customers["phone"] = customers["phone"].astype(str).str.strip()
# Remove duplicates on email (keep first occurrence)
before = len(customers)
customers.drop_duplicates(subset=["email"], keep="first", inplace=True)
print(f"   Customers: dropped {before - len(customers)} duplicate emails")

# ── Products ─────────────────────────────────────────────
# Ensure no negative prices / costs
products = products[(products["price"] > 0) & (products["cost_price"] > 0)].copy()
products["avg_rating"].fillna(products["avg_rating"].median(), inplace=True)
products["review_count"].fillna(0, inplace=True)
print(f"   Products: {len(products)} rows after price sanity check")

# ── Orders ───────────────────────────────────────────────
orders["order_date"] = pd.to_datetime(orders["order_date"])
before = len(orders)
orders.drop_duplicates(subset=["order_id"], keep="first", inplace=True)
print(f"   Orders: dropped {before - len(orders)} duplicate order IDs")

# ── Order Items ──────────────────────────────────────────
order_items = order_items[
    (order_items["quantity"] > 0) & (order_items["unit_price"] > 0)
].copy()
order_items["total_price"] = (
    order_items["unit_price"] * order_items["quantity"]
    * (1 - order_items["discount"])
).round(2)
print(f"   Order Items: {len(order_items)} valid rows after sanity check")

# ── Shipping ─────────────────────────────────────────────
shipping["ship_date"]          = pd.to_datetime(shipping["ship_date"])
shipping["estimated_delivery"] = pd.to_datetime(shipping["estimated_delivery"])
shipping["actual_delivery"]    = pd.to_datetime(shipping["actual_delivery"])
shipping["shipping_cost"].fillna(0, inplace=True)

# ─────────────────────────────────────────────────────────
# STEP 4: Feature Engineering
# ─────────────────────────────────────────────────────────
print("\n[4] Feature Engineering...")

# ── Customers: age & tenure ──────────────────────────────
customers["dob"]               = pd.to_datetime(customers["dob"])
customers["registration_date"] = pd.to_datetime(customers["registration_date"])
today = pd.Timestamp("2024-07-01")

customers["age"]            = ((today - customers["dob"]).dt.days / 365.25).astype(int)
customers["tenure_months"]  = ((today - customers["registration_date"]).dt.days / 30).astype(int)
customers["age_group"] = pd.cut(
    customers["age"],
    bins=[17, 25, 35, 45, 55, 99],
    labels=["18-25", "26-35", "36-45", "46-55", "55+"]
)
print("   ✔  customer age, tenure, age_group")

# ── Orders: calendar fields ──────────────────────────────
orders["year"]        = orders["order_date"].dt.year
orders["month"]       = orders["order_date"].dt.month
orders["month_name"]  = orders["order_date"].dt.strftime("%b")
orders["quarter"]     = orders["order_date"].dt.quarter
orders["day_of_week"] = orders["order_date"].dt.day_name()
orders["is_weekend"]  = orders["order_date"].dt.dayofweek >= 5
print("   ✔  order year, month, quarter, day_of_week, is_weekend")

# ── Shipping: delay days ─────────────────────────────────
shipping["delivery_delay_days"] = (
    shipping["actual_delivery"] - shipping["estimated_delivery"]
).dt.days.fillna(0).astype(int)
print("   ✔  shipping delivery_delay_days")

# ─────────────────────────────────────────────────────────
# STEP 5: Master Analytical Table (denormalised flat table)
# ─────────────────────────────────────────────────────────
print("\n[5] Building master analytical table...")

master = (
    order_items
    .merge(orders[["order_id","customer_id","order_date","order_status",
                   "payment_method","year","month","month_name",
                   "quarter","day_of_week","is_weekend"]],
           on="order_id")
    .merge(products[["product_id","product_name","category_id","price",
                      "cost_price","avg_rating"]],
           on="product_id")
    .merge(categories[["category_id","category_name"]], on="category_id")
    .merge(customers[["customer_id","first_name","last_name",
                       "gender","age","age_group","city","state",
                       "region","tenure_months"]],
           on="customer_id")
)
# Delivered orders only for revenue analysis
master_delivered = master[master["order_status"] == "Delivered"].copy()
print(f"   Master table  : {len(master)} rows")
print(f"   Delivered rows: {len(master_delivered)} rows")

# ─────────────────────────────────────────────────────────
# STEP 6: KPI Calculations
# ─────────────────────────────────────────────────────────
print("\n[6] KPI Calculations")
print("-" * 40)

total_revenue    = master_delivered["total_price"].sum()
total_orders     = master_delivered["order_id"].nunique()
total_customers  = master_delivered["customer_id"].nunique()
aov              = total_revenue / total_orders
total_units      = master_delivered["quantity"].sum()

# Retention rate: customers who ordered more than once
order_counts     = master_delivered.groupby("customer_id")["order_id"].nunique()
repeat_customers = (order_counts > 1).sum()
retention_rate   = repeat_customers / total_customers * 100

# Churn rate: customers with last order > 180 days before dataset end
max_date         = master_delivered["order_date"].max()
last_order_dates = master_delivered.groupby("customer_id")["order_date"].max()
churned          = (last_order_dates < (max_date - pd.Timedelta(days=180))).sum()
churn_rate       = churned / total_customers * 100

# Revenue growth: compare last year vs prior year
rev_by_year      = master_delivered.groupby("year")["total_price"].sum()
years_sorted     = sorted(rev_by_year.index)
if len(years_sorted) >= 2:
    rev_growth = (rev_by_year[years_sorted[-1]] - rev_by_year[years_sorted[-2]]) \
                 / rev_by_year[years_sorted[-2]] * 100
else:
    rev_growth = 0

print(f"   Total Revenue        : ₹{total_revenue:>14,.2f}")
print(f"   Total Orders         : {total_orders:>14,}")
print(f"   Total Customers      : {total_customers:>14,}")
print(f"   Avg Order Value      : ₹{aov:>14,.2f}")
print(f"   Total Units Sold     : {total_units:>14,}")
print(f"   Repeat Customers     : {repeat_customers:>14,}")
print(f"   Retention Rate       : {retention_rate:>13.1f}%")
print(f"   Churned Customers    : {churned:>14,}")
print(f"   Churn Rate           : {churn_rate:>13.1f}%")
print(f"   Revenue Growth (YoY) : {rev_growth:>13.1f}%")

# ─────────────────────────────────────────────────────────
# STEP 7: Customer Segmentation (RFM)
# ─────────────────────────────────────────────────────────
print("\n[7] RFM Customer Segmentation...")

snapshot_date = max_date + pd.Timedelta(days=1)

rfm = master_delivered.groupby("customer_id").agg(
    recency   = ("order_date",   lambda x: (snapshot_date - x.max()).days),
    frequency = ("order_id",     "nunique"),
    monetary  = ("total_price",  "sum"),
).reset_index()

# Score each metric 1–4 using quartiles (4 = best)
rfm["R_score"] = pd.qcut(rfm["recency"],   4, labels=[4, 3, 2, 1]).astype(int)
rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 4,
                          labels=[1, 2, 3, 4]).astype(int)
rfm["M_score"] = pd.qcut(rfm["monetary"],  4, labels=[1, 2, 3, 4]).astype(int)
rfm["RFM_sum"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]

def segment(row):
    if row["RFM_sum"] >= 10:                    return "Champions"
    elif row["RFM_sum"] >= 8:                   return "Loyal Customers"
    elif row["R_score"] >= 3 and row["F_score"] <= 2: return "Potential Loyalists"
    elif row["R_score"] <= 2 and row["F_score"] >= 3: return "At Risk"
    elif row["RFM_sum"] <= 4:                   return "Lost"
    else:                                       return "Needs Attention"

rfm["segment"] = rfm.apply(segment, axis=1)
seg_summary    = rfm["segment"].value_counts()
print(rfm["segment"].value_counts().to_string())

# ─────────────────────────────────────────────────────────
# STEP 8: Save cleaned data to Excel (multi-sheet)
# ─────────────────────────────────────────────────────────
print("\n[8] Saving cleaned data to Excel...")
out_path = os.path.join(DATA_DIR, "cleaned_data.xlsx")

with pd.ExcelWriter(out_path, engine="xlsxwriter") as writer:
    master_delivered.to_excel(writer, sheet_name="Master_Data",    index=False)
    rfm.to_excel(             writer, sheet_name="RFM_Segments",   index=False)
    customers.to_excel(       writer, sheet_name="Customers",      index=False)
    products.to_excel(        writer, sheet_name="Products",       index=False)
    orders.to_excel(          writer, sheet_name="Orders",         index=False)

print(f"   Saved → {out_path}")

# Store key objects for Phase 5 to re-use
import pickle
cache = {
    "master_delivered": master_delivered,
    "rfm": rfm,
    "customers": customers,
    "products": products,
    "orders": orders,
    "categories": categories,
    "shipping": shipping,
}
cache_path = os.path.join(DATA_DIR, "analysis_cache.pkl")
with open(cache_path, "wb") as f:
    pickle.dump(cache, f)

print(f"   Cache  → {cache_path}")
print()
print("=" * 60)
print("  PHASE 4 COMPLETE ✔")
print("=" * 60)
