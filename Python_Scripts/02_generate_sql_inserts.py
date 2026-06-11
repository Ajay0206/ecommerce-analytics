"""
============================================================
PHASE 2 (continued): SQL DATA INSERTION SCRIPT GENERATOR
============================================================
Reads the 6 CSV files from Dataset/ and writes a ready-to-run
SQL file (02_insert_data.sql) into SQL_Scripts/.

Run AFTER 01_generate_dataset.py
============================================================
"""

import pandas as pd
import os

BASE      = os.path.dirname(os.path.abspath(__file__))
DATA_DIR  = os.path.join(BASE, "..", "Dataset")
SQL_DIR   = os.path.join(BASE, "..", "SQL_Scripts")
OUT_FILE  = os.path.join(SQL_DIR, "02_insert_data.sql")

def esc(val):
    """Escape a Python value for safe SQL insertion."""
    if val is None or (isinstance(val, float) and str(val) == "nan"):
        return "NULL"
    if isinstance(val, str):
        val = val.replace("'", "''")   # escape single quotes
        return f"'{val}'"
    return str(val)

def build_inserts(df, table, columns, chunk=200):
    """Yield batched INSERT statements."""
    rows = [tuple(row) for row in df[columns].itertuples(index=False, name=None)]
    col_str = ", ".join(columns)
    for i in range(0, len(rows), chunk):
        batch = rows[i:i+chunk]
        vals  = ",\n    ".join(
                    "(" + ", ".join(esc(v) for v in row) + ")"
                    for row in batch
                )
        yield f"INSERT INTO {table} ({col_str}) VALUES\n    {vals};\n"

lines = [
    "-- ============================================================",
    "-- PHASE 2: DATA INSERTION",
    "-- E-Commerce Sales & Customer Analytics Dashboard",
    "-- ============================================================",
    "-- Run AFTER 01_create_schema.sql",
    "-- ============================================================",
    "",
    "USE ecommerce_analytics;",
    "SET FOREIGN_KEY_CHECKS = 0;   -- disable FK checks during bulk load",
    "",
]

tables = [
    ("categories.csv",  "categories",  ["category_id","category_name","description"]),
    ("products.csv",    "products",    ["product_id","product_name","category_id",
                                        "price","cost_price","stock_quantity",
                                        "avg_rating","review_count"]),
    ("customers.csv",   "customers",   ["customer_id","first_name","last_name",
                                        "email","phone","dob","gender",
                                        "city","state","region",
                                        "registration_date","status"]),
    ("orders.csv",      "orders",      ["order_id","customer_id","order_date",
                                        "order_status","payment_method","discount_percent"]),
    ("order_items.csv", "order_items", ["item_id","order_id","product_id",
                                        "quantity","unit_price","discount","total_price"]),
    ("shipping.csv",    "shipping",    ["order_id","carrier","tracking_number",
                                        "ship_date","estimated_delivery",
                                        "actual_delivery","delivery_status","shipping_cost"]),
]

total_rows = 0
for fname, table, cols in tables:
    df  = pd.read_csv(os.path.join(DATA_DIR, fname))
    cnt = len(df)
    total_rows += cnt
    lines.append(f"\n-- ── {table.upper()} ({cnt} rows) ──────────────────")
    for stmt in build_inserts(df, table, cols):
        lines.append(stmt)
    print(f"  ✔  {table:<14}: {cnt} rows written")

lines += [
    "",
    "SET FOREIGN_KEY_CHECKS = 1;   -- re-enable FK checks",
    "",
    "-- ============================================================",
    "-- DATA INSERTION COMPLETE",
    f"-- Total rows inserted : {total_rows}",
    "-- ============================================================",
]

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\n  SQL file saved → {OUT_FILE}")
print(f"  Total rows : {total_rows}")
