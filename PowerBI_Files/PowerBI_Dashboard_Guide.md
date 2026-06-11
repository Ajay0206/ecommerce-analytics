# Power BI Dashboard Setup Guide
# E-Commerce Sales & Customer Analytics Dashboard
# ============================================================

## Overview
This document walks you through building a 4-page professional
Power BI dashboard using the cleaned_data.xlsx file.

---

## STEP 1 — Import Data

1. Open Power BI Desktop
2. Click **Get Data → Excel Workbook**
3. Browse to `Dataset/cleaned_data.xlsx`
4. Select all sheets:
   - Master_Data
   - RFM_Segments
   - Customers
   - Products
   - Orders
5. Click **Load**

---

## STEP 2 — Data Model Relationships

In the **Model view**, create these relationships:

| From Table  | Column      | To Table    | Column      | Type        |
|-------------|-------------|-------------|-------------|-------------|
| Master_Data | customer_id | Customers   | customer_id | Many-to-One |
| Master_Data | product_id  | Products    | product_id  | Many-to-One |
| Master_Data | customer_id | RFM_Segments| customer_id | Many-to-One |

---

## STEP 3 — DAX Measures

Create a dedicated **Measures Table** (Enter Data → blank table named "KPIs"):

```dax
// ── Core Revenue Measures ──────────────────────────────
Total Revenue =
    SUMX(Master_Data, Master_Data[total_price])

Total Orders =
    DISTINCTCOUNT(Master_Data[order_id])

Total Customers =
    DISTINCTCOUNT(Master_Data[customer_id])

Avg Order Value =
    DIVIDE([Total Revenue], [Total Orders], 0)

Total Units Sold =
    SUM(Master_Data[quantity])

// ── Customer Measures ─────────────────────────────────
Repeat Customers =
    CALCULATE(
        DISTINCTCOUNT(Master_Data[customer_id]),
        FILTER(
            SUMMARIZE(Master_Data, Master_Data[customer_id],
                      "OrderCount", DISTINCTCOUNT(Master_Data[order_id])),
            [OrderCount] > 1
        )
    )

Retention Rate % =
    DIVIDE([Repeat Customers], [Total Customers], 0) * 100

Churn Rate % = 100 - [Retention Rate %]

// ── Period Comparison ─────────────────────────────────
Revenue LY =
    CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Master_Data[order_date]))

Revenue Growth % =
    DIVIDE([Total Revenue] - [Revenue LY], [Revenue LY], 0) * 100

// ── Average Rating ────────────────────────────────────
Avg Product Rating =
    AVERAGE(Products[avg_rating])
```

---

## STEP 4 — Dashboard Pages

### PAGE 1 — Executive Dashboard
**Theme colour: Navy (#1A3C5E)**

KPI Cards (top row):
- Total Revenue
- Total Orders
- Total Customers
- Avg Order Value
- Retention Rate %
- Revenue Growth %

Visuals:
- **Line Chart**: Total Revenue by order_date (Month)
- **Donut Chart**: Revenue by category_name
- **Bar Chart**: Revenue by region
- **Card**: Churn Rate %

Slicers:
- Year
- Region
- Category

---

### PAGE 2 — Sales Dashboard

Visuals:
- **Area Chart**: Monthly revenue trend with year comparison
- **Bar Chart**: Top 10 products by Total Revenue
- **Matrix**: Category × Month revenue heatmap
- **Clustered Bar**: Revenue by payment_method
- **Pie Chart**: Order status distribution

Slicers:
- Date Range (slider)
- Order Status
- Category

---

### PAGE 3 — Customer Dashboard

KPI Cards:
- Total Customers
- Repeat Customers
- Retention Rate %
- Avg Customer Tenure (months)

Visuals:
- **Bar Chart**: RFM Segment distribution (from RFM_Segments)
- **Bar Chart**: Customers by age_group
- **Donut Chart**: Customers by gender
- **Map Visual**: Customer count by city/state
- **Table**: Top 10 customers (name, region, LTV, orders)

Slicers:
- Region
- Gender
- Age Group

---

### PAGE 4 — Product Dashboard

KPI Cards:
- Total Products
- Avg Product Rating
- Total Units Sold
- Low Stock Count (stock < 20)

Visuals:
- **Bar Chart**: Top 10 products by units_sold
- **Scatter Plot**: price vs avg_rating (sized by review_count)
- **Bar Chart**: Category-wise avg rating
- **Table**: Products with low stock (stock_quantity < 20)
- **Bar Chart**: Revenue per unit by category

Slicers:
- Category
- Price Range

---

## STEP 5 — Formatting Tips

1. **Colour Theme**: Use hex #1A3C5E (navy) as primary, #F39C12 (gold) as accent
2. **KPI Cards**: Set background to white, add conditional formatting
3. **Titles**: Bold, 14pt, navy colour
4. **Report Background**: Light grey (#F5F6FA)
5. **Tooltips**: Enable and customise for all charts
6. **Cross-filtering**: Enable interactions between all visuals

---

## STEP 6 — Publishing

1. Save as `PowerBI_Files/ecommerce_dashboard.pbix`
2. Publish to Power BI Service (requires account)
3. Schedule data refresh if connected to live MySQL

---

## DAX Colour Formatting Example

```dax
// Conditional colour for Revenue Growth card
Revenue Growth Colour =
    IF([Revenue Growth %] >= 0, "#27AE60", "#E74C3C")
```

---

*Note: Power BI .pbix files are binary and cannot be auto-generated
 by a script. Use this guide to build the dashboard manually.
 The cleaned_data.xlsx contains all required data.*
