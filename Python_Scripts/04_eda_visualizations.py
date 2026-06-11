"""
============================================================
PHASE 5: EXPLORATORY DATA ANALYSIS & VISUALIZATIONS
E-Commerce Sales & Customer Analytics Dashboard
============================================================
Input  : analysis_cache.pkl (from Phase 4)
Output : 12 PNG charts saved to Visualizations/
============================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")          # headless — no display needed
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pickle, os, warnings
warnings.filterwarnings("ignore")

# ── Style ─────────────────────────────────────────────────
plt.rcParams.update({
    "figure.dpi":        150,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.titlesize":    13,
    "axes.labelsize":    11,
    "xtick.labelsize":   9,
    "ytick.labelsize":   9,
    "font.family":       "DejaVu Sans",
})
PALETTE  = ["#1A3C5E","#2E86C1","#85C1E9","#F1948A","#F39C12",
            "#27AE60","#8E44AD","#E74C3C"]
NAVY     = "#1A3C5E"
GOLD     = "#F39C12"
sns.set_palette(PALETTE)

BASE    = os.path.dirname(os.path.abspath(__file__))
VIZ_DIR = os.path.join(BASE, "..", "Visualizations")
os.makedirs(VIZ_DIR, exist_ok=True)

# ── Load cache ────────────────────────────────────────────
cache_path = os.path.join(BASE, "..", "Dataset", "analysis_cache.pkl")
with open(cache_path, "rb") as f:
    cache = pickle.load(f)

md   = cache["master_delivered"]   # master delivered dataframe
rfm  = cache["rfm"]
cust = cache["customers"]
prod = cache["products"]
cats = cache["categories"]
ship = cache["shipping"]

print("=" * 60)
print("  PHASE 5 — EDA & Visualizations")
print("=" * 60)

def save(fig, name):
    path = os.path.join(VIZ_DIR, name)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✔  Saved: {name}")

# ═════════════════════════════════════════════════════════
# CHART 1 — Monthly Revenue Trend (Line Chart)
# ═════════════════════════════════════════════════════════
monthly = (md.groupby(["year","month","month_name"])["total_price"]
             .sum().reset_index())
monthly["period"] = monthly["year"].astype(str) + "-" + \
                    monthly["month"].astype(str).str.zfill(2)
monthly.sort_values("period", inplace=True)

fig, ax = plt.subplots(figsize=(13, 4))
ax.plot(monthly["period"], monthly["total_price"] / 1e6,
        color=NAVY, linewidth=2.2, marker="o", markersize=4)
ax.fill_between(monthly["period"], monthly["total_price"] / 1e6,
                alpha=0.12, color=NAVY)
ax.set_title("Monthly Revenue Trend", fontweight="bold")
ax.set_xlabel("Month"); ax.set_ylabel("Revenue (₹ Millions)")
plt.xticks(rotation=45, ha="right")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f"₹{x:.1f}M"))
save(fig, "01_monthly_revenue_trend.png")

# ═════════════════════════════════════════════════════════
# CHART 2 — Top 10 Products by Revenue (Horizontal Bar)
# ═════════════════════════════════════════════════════════
top_prod = (md.groupby("product_name")["total_price"]
              .sum().nlargest(10).sort_values())
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top_prod.index, top_prod.values / 1e6,
               color=PALETTE[:10][::-1])
ax.set_title("Top 10 Products by Revenue", fontweight="bold")
ax.set_xlabel("Revenue (₹ Millions)")
for bar in bars:
    ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2,
            f"₹{bar.get_width():.1f}M", va="center", fontsize=8)
save(fig, "02_top10_products_revenue.png")

# ═════════════════════════════════════════════════════════
# CHART 3 — Category Revenue Share (Donut / Pie)
# ═════════════════════════════════════════════════════════
cat_rev = md.groupby("category_name")["total_price"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 7))
wedges, texts, autotexts = ax.pie(
    cat_rev.values, labels=cat_rev.index,
    autopct="%1.1f%%", startangle=140,
    pctdistance=0.82, colors=PALETTE,
    wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2))
for at in autotexts: at.set_fontsize(8)
ax.set_title("Revenue Share by Category", fontweight="bold", pad=15)
save(fig, "03_category_revenue_pie.png")

# ═════════════════════════════════════════════════════════
# CHART 4 — Region-wise Sales (Bar Chart)
# ═════════════════════════════════════════════════════════
region_rev = (md.groupby("region")["total_price"]
                .sum().sort_values(ascending=False))
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(region_rev.index, region_rev.values / 1e6,
              color=PALETTE[:len(region_rev)], edgecolor="white")
ax.set_title("Revenue by Region", fontweight="bold")
ax.set_ylabel("Revenue (₹ Millions)")
for b in bars:
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.1,
            f"₹{b.get_height():.1f}M", ha="center", fontsize=9, fontweight="bold")
save(fig, "04_region_revenue.png")

# ═════════════════════════════════════════════════════════
# CHART 5 — Order Status Distribution (Bar)
# ═════════════════════════════════════════════════════════
orders_all = cache["orders"]
status_cnt = orders_all["order_status"].value_counts()
colors_map = {"Delivered": "#27AE60", "Shipped": "#2E86C1",
              "Processing": GOLD,     "Cancelled": "#E74C3C",
              "Returned":  "#8E44AD"}
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(status_cnt.index,
              status_cnt.values,
              color=[colors_map.get(s, NAVY) for s in status_cnt.index],
              edgecolor="white")
ax.set_title("Order Status Distribution", fontweight="bold")
ax.set_ylabel("Number of Orders")
for b in bars:
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 10,
            f"{b.get_height():,}", ha="center", fontsize=9)
save(fig, "05_order_status.png")

# ═════════════════════════════════════════════════════════
# CHART 6 — Payment Method Distribution (Horizontal Bar)
# ═════════════════════════════════════════════════════════
pay_cnt = orders_all["payment_method"].value_counts().sort_values()
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(pay_cnt.index, pay_cnt.values, color=NAVY, edgecolor="white")
ax.set_title("Orders by Payment Method", fontweight="bold")
ax.set_xlabel("Number of Orders")
for i, v in enumerate(pay_cnt.values):
    ax.text(v + 5, i, str(v), va="center", fontsize=9)
save(fig, "06_payment_methods.png")

# ═════════════════════════════════════════════════════════
# CHART 7 — Customer Age Distribution (Histogram)
# ═════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(cust["age"], bins=20, color=NAVY, edgecolor="white", alpha=0.85)
ax.axvline(cust["age"].mean(), color=GOLD, linewidth=2,
           linestyle="--", label=f"Mean age: {cust['age'].mean():.0f}")
ax.set_title("Customer Age Distribution", fontweight="bold")
ax.set_xlabel("Age"); ax.set_ylabel("Count")
ax.legend()
save(fig, "07_customer_age_distribution.png")

# ═════════════════════════════════════════════════════════
# CHART 8 — RFM Customer Segments (Bar)
# ═════════════════════════════════════════════════════════
seg_cnt = rfm["segment"].value_counts()
seg_colors = {"Champions": "#27AE60", "Loyal Customers": "#2E86C1",
              "Potential Loyalists": "#85C1E9", "Needs Attention": GOLD,
              "At Risk": "#F1948A", "Lost": "#E74C3C"}
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(seg_cnt.index, seg_cnt.values,
              color=[seg_colors.get(s, NAVY) for s in seg_cnt.index],
              edgecolor="white")
ax.set_title("RFM Customer Segmentation", fontweight="bold")
ax.set_ylabel("Number of Customers")
plt.xticks(rotation=20, ha="right")
for b in bars:
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1,
            str(int(b.get_height())), ha="center", fontsize=9, fontweight="bold")
save(fig, "08_rfm_segments.png")

# ═════════════════════════════════════════════════════════
# CHART 9 — Heatmap: Revenue by Category × Month
# ═════════════════════════════════════════════════════════
pivot = md.pivot_table(values="total_price",
                       index="category_name",
                       columns="month_name",
                       aggfunc="sum",
                       fill_value=0)
month_order = ["Jan","Feb","Mar","Apr","May","Jun",
               "Jul","Aug","Sep","Oct","Nov","Dec"]
pivot = pivot.reindex(columns=[m for m in month_order if m in pivot.columns])

fig, ax = plt.subplots(figsize=(14, 6))
sns.heatmap(pivot / 1e6, annot=True, fmt=".1f", cmap="Blues",
            linewidths=0.5, ax=ax, cbar_kws={"label": "Revenue (₹M)"})
ax.set_title("Revenue Heatmap — Category × Month", fontweight="bold")
ax.set_xlabel("Month"); ax.set_ylabel("Category")
save(fig, "09_category_month_heatmap.png")

# ═════════════════════════════════════════════════════════
# CHART 10 — Top 10 Customers by Lifetime Value
# ═════════════════════════════════════════════════════════
top_cust = (md.groupby(["customer_id","first_name","last_name"])
              ["total_price"].sum()
              .nlargest(10).reset_index())
top_cust["name"] = top_cust["first_name"] + " " + top_cust["last_name"]
top_cust.sort_values("total_price", inplace=True)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top_cust["name"], top_cust["total_price"] / 1e6,
               color=NAVY, edgecolor="white")
ax.set_title("Top 10 Customers by Lifetime Value", fontweight="bold")
ax.set_xlabel("Revenue (₹ Millions)")
for b in bars:
    ax.text(b.get_width() + 0.02, b.get_y() + b.get_height() / 2,
            f"₹{b.get_width():.2f}M", va="center", fontsize=8)
save(fig, "10_top10_customers_ltv.png")

# ═════════════════════════════════════════════════════════
# CHART 11 — Revenue by Day of Week (Bar)
# ═════════════════════════════════════════════════════════
dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
dow_rev = md.groupby("day_of_week")["total_price"].sum().reindex(dow_order) / 1e6

fig, ax = plt.subplots(figsize=(9, 5))
colors = [GOLD if d in ["Saturday","Sunday"] else NAVY for d in dow_rev.index]
ax.bar(dow_rev.index, dow_rev.values, color=colors, edgecolor="white")
ax.set_title("Revenue by Day of Week", fontweight="bold")
ax.set_ylabel("Revenue (₹ Millions)")
plt.xticks(rotation=20, ha="right")
save(fig, "11_revenue_by_day_of_week.png")

# ═════════════════════════════════════════════════════════
# CHART 12 — Product Price Distribution by Category (Box)
# ═════════════════════════════════════════════════════════
prod_with_cat = prod.merge(cats, on="category_id")
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=prod_with_cat, x="category_name", y="price",
            palette=PALETTE, ax=ax)
ax.set_title("Product Price Distribution by Category", fontweight="bold")
ax.set_xlabel("Category"); ax.set_ylabel("Price (₹)")
plt.xticks(rotation=25, ha="right")
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
save(fig, "12_price_distribution_by_category.png")

print()
print("  12 charts saved to Visualizations/")
print("=" * 60)
print("  PHASE 5 COMPLETE ✔")
print("=" * 60)
