"""
============================================================
PHASE 1: DATASET GENERATION
E-Commerce Sales & Customer Analytics Dashboard
============================================================
Purpose : Generate realistic e-commerce CSV datasets that
          mimic a production database for analysis.
Author  : Ajay Kumar
Tool    : Python (Faker, Pandas, NumPy)
Output  : 6 CSV files saved to the Dataset/ folder
============================================================
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
import os
from datetime import datetime, timedelta

# ── Reproducibility ──────────────────────────────────────
random.seed(42)
np.random.seed(42)
fake = Faker("en_IN")          # Indian locale for realistic names/addresses
Faker.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "Dataset")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("  PHASE 1 — Dataset Generation")
print("=" * 60)

# ─────────────────────────────────────────────────────────
# 1. CATEGORIES  (8 rows)
# ─────────────────────────────────────────────────────────
categories_data = [
    (1, "Electronics",     "Gadgets, mobiles, laptops"),
    (2, "Fashion",         "Clothing, footwear, accessories"),
    (3, "Home & Kitchen",  "Appliances, furniture, décor"),
    (4, "Sports",          "Fitness, outdoor, equipment"),
    (5, "Beauty",          "Skincare, makeup, grooming"),
    (6, "Books",           "Academic, fiction, non-fiction"),
    (7, "Toys & Games",    "Kids' toys, board games"),
    (8, "Groceries",       "Food, beverages, staples"),
]
categories_df = pd.DataFrame(categories_data,
                             columns=["category_id", "category_name", "description"])
print(f"  ✔  Categories   : {len(categories_df)} rows")

# ─────────────────────────────────────────────────────────
# 2. PRODUCTS  (200 rows)
# ─────────────────────────────────────────────────────────
product_names = {
    1: ["iPhone 15", "Samsung Galaxy S23", "OnePlus 12", "Lenovo IdeaPad",
        "Dell Inspiron", "Sony WH-1000XM5", "JBL Bluetooth Speaker",
        "Xiaomi Smart TV", "Canon EOS Camera", "Apple Watch Series 9"],
    2: ["Nike Air Max", "Adidas Running Shoes", "Levi's Jeans",
        "Zara Formal Shirt", "H&M Dress", "Puma Hoodie",
        "Ray-Ban Sunglasses", "Titan Wristwatch", "Woodland Boots", "FabIndia Kurta"],
    3: ["Instant Pot Cooker", "Philips Air Fryer", "IKEA Study Desk",
        "Godrej Almirah", "Kent RO Purifier", "Prestige Mixer",
        "Bosch Washing Machine", "Havells Fan", "Nilkamal Chair", "Asian Paints Kit"],
    4: ["Cosco Badminton Set", "Nivia Football", "Reebok Gym Gloves",
        "Decathlon Cycle", "Yoga Mat Pro", "Protein Shaker Bottle",
        "Speedo Swimwear", "Hiking Backpack", "Resistance Band Set", "Jump Rope Pro"],
    5: ["Lakme Foundation", "Mamaearth Facewash", "Biotique Moisturiser",
        "Forest Essentials Serum", "Nykaa Lipstick", "WOW Shampoo",
        "Dove Body Lotion", "Gillette Razors", "Plum Night Cream", "L'Oreal Conditioner"],
    6: ["Data Structures by Cormen", "Python Crash Course", "Atomic Habits",
        "The Lean Startup", "Wings of Fire", "Deep Work", "NCERT Physics",
        "Competitive Programming 3", "Zero to One", "Ikigai"],
    7: ["LEGO Classic Set", "Monopoly Board Game", "Rubik's Cube",
        "Remote Control Car", "Barbie Dream House", "Hot Wheels Track",
        "Jenga Tower", "UNO Card Game", "Nerf Blaster", "Play-Doh Kit"],
    8: ["Tata Tea Premium", "Nescafe Classic", "Aashirvaad Atta",
        "Amul Butter 500g", "Fortune Sunflower Oil", "Maggi Noodles Pack",
        "Tropicana Orange Juice", "Haldiram Namkeen", "MTR Ready Meals", "Patanjali Honey"],
}

products = []
product_id = 1
for cat_id, names in product_names.items():
    for name in names:
        price   = round(random.uniform(99, 89999), 2)
        cost    = round(price * random.uniform(0.45, 0.75), 2)
        stock   = random.randint(5, 500)
        rating  = round(random.uniform(3.0, 5.0), 1)
        reviews = random.randint(10, 5000)
        products.append([product_id, name, cat_id, price, cost, stock, rating, reviews])
        product_id += 1

products_df = pd.DataFrame(products,
    columns=["product_id", "product_name", "category_id",
             "price", "cost_price", "stock_quantity", "avg_rating", "review_count"])
print(f"  ✔  Products     : {len(products_df)} rows")

# ─────────────────────────────────────────────────────────
# 3. CUSTOMERS  (500 rows)
# ─────────────────────────────────────────────────────────
cities_states = [
    ("Mumbai",     "Maharashtra"), ("Delhi",      "Delhi"),
    ("Bangalore",  "Karnataka"),   ("Hyderabad",  "Telangana"),
    ("Chennai",    "Tamil Nadu"),  ("Kolkata",    "West Bengal"),
    ("Pune",       "Maharashtra"), ("Ahmedabad",  "Gujarat"),
    ("Jaipur",     "Rajasthan"),   ("Lucknow",    "Uttar Pradesh"),
    ("Surat",      "Gujarat"),     ("Nagpur",     "Maharashtra"),
    ("Indore",     "MP"),          ("Bhopal",     "MP"),
    ("Visakhapatnam","AP"),        ("Tirupati",   "AP"),
]
regions = {
    "Maharashtra": "West",  "Gujarat": "West",  "Rajasthan": "West",
    "Delhi": "North",       "Uttar Pradesh": "North",
    "Karnataka": "South",   "Tamil Nadu": "South",
    "Telangana": "South",   "AP": "South",
    "West Bengal": "East",  "MP": "Central",
}

customers = []
reg_date_start = datetime(2021, 1, 1)
reg_date_end   = datetime(2023, 12, 31)
for i in range(1, 501):
    city, state = random.choice(cities_states)
    region      = regions.get(state, "Other")
    reg_date    = reg_date_start + timedelta(
                    days=random.randint(0, (reg_date_end - reg_date_start).days))
    customers.append([
        i,
        fake.first_name(), fake.last_name(),
        fake.email(),
        fake.phone_number()[:15],
        fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%Y-%m-%d"),
        random.choice(["Male", "Female", "Other"]),
        city, state, region,
        reg_date.strftime("%Y-%m-%d"),
        random.choice(["Active", "Active", "Active", "Inactive"]),
    ])

customers_df = pd.DataFrame(customers,
    columns=["customer_id", "first_name", "last_name", "email", "phone",
             "dob", "gender", "city", "state", "region",
             "registration_date", "status"])
print(f"  ✔  Customers    : {len(customers_df)} rows")

# ─────────────────────────────────────────────────────────
# 4. ORDERS  (3 000 rows)
# ─────────────────────────────────────────────────────────
order_start = datetime(2022, 1, 1)
order_end   = datetime(2024, 6, 30)
statuses    = ["Delivered", "Delivered", "Delivered", "Shipped",
               "Processing", "Cancelled", "Returned"]
payment_methods = ["Credit Card", "Debit Card", "UPI", "Net Banking",
                   "Cash on Delivery", "Wallet"]

orders = []
for i in range(1, 3001):
    cust_id    = random.randint(1, 500)
    order_date = order_start + timedelta(
                   days=random.randint(0, (order_end - order_start).days))
    status     = random.choices(statuses, weights=[60,0,0,15,10,10,5])[0]
    payment    = random.choice(payment_methods)
    discount   = round(random.uniform(0, 0.30), 2)
    orders.append([i, cust_id, order_date.strftime("%Y-%m-%d"),
                   status, payment, discount])

orders_df = pd.DataFrame(orders,
    columns=["order_id", "customer_id", "order_date",
             "order_status", "payment_method", "discount_percent"])
print(f"  ✔  Orders       : {len(orders_df)} rows")

# ─────────────────────────────────────────────────────────
# 5. ORDER ITEMS  (5 000–8 000 rows)
# ─────────────────────────────────────────────────────────
order_items = []
item_id = 1
for _, order in orders_df.iterrows():
    num_items = random.choices([1, 2, 3, 4], weights=[40, 35, 15, 10])[0]
    chosen    = random.sample(range(1, 81), min(num_items, 80))
    for prod_id in chosen:
        price = float(products_df.loc[products_df.product_id == prod_id, "price"].values[0])
        qty   = random.randint(1, 4)
        disc  = order["discount_percent"]
        total = round(price * qty * (1 - disc), 2)
        order_items.append([item_id, int(order["order_id"]),
                            prod_id, qty, price, disc, total])
        item_id += 1

order_items_df = pd.DataFrame(order_items,
    columns=["item_id", "order_id", "product_id",
             "quantity", "unit_price", "discount", "total_price"])
print(f"  ✔  Order Items  : {len(order_items_df)} rows")

# ─────────────────────────────────────────────────────────
# 6. SHIPPING  (one record per delivered/shipped order)
# ─────────────────────────────────────────────────────────
carriers   = ["BlueDart", "Delhivery", "Ekart", "DTDC", "FedEx India"]
shipped_orders = orders_df[orders_df["order_status"].isin(["Delivered", "Shipped"])]

shipping = []
for _, order in shipped_orders.iterrows():
    ship_date = datetime.strptime(order["order_date"], "%Y-%m-%d") \
                + timedelta(days=random.randint(1, 3))
    est_del   = ship_date + timedelta(days=random.randint(3, 7))
    act_del   = est_del + timedelta(days=random.randint(-1, 3)) \
                if order["order_status"] == "Delivered" else None
    cost = round(random.uniform(40, 250), 2)
    shipping.append([
        int(order["order_id"]),
        random.choice(carriers),
        fake.bothify("TRK##########"),
        ship_date.strftime("%Y-%m-%d"),
        est_del.strftime("%Y-%m-%d"),
        act_del.strftime("%Y-%m-%d") if act_del else None,
        order["order_status"],
        cost,
    ])

shipping_df = pd.DataFrame(shipping,
    columns=["order_id", "carrier", "tracking_number",
             "ship_date", "estimated_delivery", "actual_delivery",
             "delivery_status", "shipping_cost"])
print(f"  ✔  Shipping     : {len(shipping_df)} rows")

# ─────────────────────────────────────────────────────────
# Save all CSVs
# ─────────────────────────────────────────────────────────
files = {
    "categories.csv":   categories_df,
    "products.csv":     products_df,
    "customers.csv":    customers_df,
    "orders.csv":       orders_df,
    "order_items.csv":  order_items_df,
    "shipping.csv":     shipping_df,
}
for fname, df in files.items():
    path = os.path.join(OUTPUT_DIR, fname)
    df.to_csv(path, index=False)

print()
print("  All 6 CSV files saved to Dataset/")
print("=" * 60)
print("  PHASE 1 COMPLETE ✔")
print("=" * 60)
