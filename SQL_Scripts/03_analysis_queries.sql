-- ============================================================
-- PHASE 3: SQL ANALYSIS QUERIES
-- E-Commerce Sales & Customer Analytics Dashboard
-- ============================================================
-- Each query is numbered, titled, and explained with comments
-- so a beginner can follow the logic step-by-step.
-- Run AFTER 01_create_schema.sql + 02_insert_data.sql
-- ============================================================

USE ecommerce_analytics;

-- ════════════════════════════════════════════════════════════
-- SECTION A — REVENUE & SALES METRICS
-- ════════════════════════════════════════════════════════════

-- ── Query A1: Total Revenue ──────────────────────────────
-- Sum all order-level revenue from delivered orders only.
-- We exclude Cancelled and Returned to avoid inflating KPIs.
SELECT
    ROUND(SUM(oi.total_price), 2)  AS total_revenue,
    COUNT(DISTINCT o.order_id)     AS total_orders,
    COUNT(DISTINCT o.customer_id)  AS unique_customers,
    ROUND(SUM(oi.total_price)
          / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'Delivered';


-- ── Query A2: Monthly Sales Trend ────────────────────────
-- Shows revenue month-by-month to spot seasonality & growth.
SELECT
    DATE_FORMAT(o.order_date, '%Y-%m')          AS month,
    COUNT(DISTINCT o.order_id)                  AS orders_count,
    ROUND(SUM(oi.total_price), 2)               AS monthly_revenue,
    ROUND(AVG(oi.total_price), 2)               AS avg_item_value
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'Delivered'
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
ORDER BY month;


-- ── Query A3: Quarterly Revenue with YoY Growth ──────────
-- Uses LAG() window function to compute Year-on-Year growth%.
WITH quarterly AS (
    SELECT
        YEAR(o.order_date)     AS yr,
        QUARTER(o.order_date)  AS qtr,
        ROUND(SUM(oi.total_price), 2) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'Delivered'
    GROUP BY yr, qtr
)
SELECT
    yr, qtr, revenue,
    LAG(revenue) OVER (PARTITION BY qtr ORDER BY yr) AS prev_yr_revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (PARTITION BY qtr ORDER BY yr))
        / NULLIF(LAG(revenue) OVER (PARTITION BY qtr ORDER BY yr), 0) * 100
    , 2) AS yoy_growth_pct
FROM quarterly
ORDER BY yr, qtr;


-- ── Query A4: Average Order Value (AOV) by Month ─────────
SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    ROUND(SUM(oi.total_price)
          / COUNT(DISTINCT o.order_id), 2) AS aov
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'Delivered'
GROUP BY month
ORDER BY month;


-- ════════════════════════════════════════════════════════════
-- SECTION B — PRODUCT PERFORMANCE
-- ════════════════════════════════════════════════════════════

-- ── Query B1: Top 10 Best-Selling Products by Revenue ────
SELECT
    p.product_id,
    p.product_name,
    c.category_name,
    SUM(oi.quantity)               AS units_sold,
    ROUND(SUM(oi.total_price), 2)  AS total_revenue,
    ROUND(AVG(oi.unit_price), 2)   AS avg_selling_price
FROM order_items oi
JOIN products p  ON oi.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
JOIN orders o    ON oi.order_id = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY p.product_id, p.product_name, c.category_name
ORDER BY total_revenue DESC
LIMIT 10;


-- ── Query B2: Top 10 Products by Units Sold ──────────────
SELECT
    p.product_name,
    c.category_name,
    SUM(oi.quantity)  AS units_sold
FROM order_items oi
JOIN products p   ON oi.product_id  = p.product_id
JOIN categories c ON p.category_id  = c.category_id
JOIN orders o     ON oi.order_id    = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY p.product_name, c.category_name
ORDER BY units_sold DESC
LIMIT 10;


-- ── Query B3: Category Performance ───────────────────────
-- Revenue, orders, and average product rating per category.
SELECT
    c.category_name,
    COUNT(DISTINCT oi.order_id)    AS orders_count,
    SUM(oi.quantity)               AS total_units_sold,
    ROUND(SUM(oi.total_price), 2)  AS category_revenue,
    ROUND(AVG(p.avg_rating), 2)    AS avg_product_rating,
    ROUND(SUM(oi.total_price)
          / SUM(oi.quantity), 2)   AS revenue_per_unit
FROM order_items oi
JOIN products p    ON oi.product_id  = p.product_id
JOIN categories c  ON p.category_id  = c.category_id
JOIN orders o      ON oi.order_id    = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY c.category_name
ORDER BY category_revenue DESC;


-- ── Query B4: Product Profit Margin ──────────────────────
-- Gross margin = (selling_price − cost) / selling_price × 100
SELECT
    p.product_name,
    c.category_name,
    p.price                                       AS list_price,
    p.cost_price,
    ROUND(p.price - p.cost_price, 2)              AS gross_profit,
    ROUND((p.price - p.cost_price) / p.price * 100, 1) AS margin_pct
FROM products p
JOIN categories c ON p.category_id = c.category_id
ORDER BY margin_pct DESC;


-- ════════════════════════════════════════════════════════════
-- SECTION C — CUSTOMER ANALYTICS
-- ════════════════════════════════════════════════════════════

-- ── Query C1: Top 10 Customers by Lifetime Value ─────────
SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.city, c.region,
    COUNT(DISTINCT o.order_id)             AS total_orders,
    ROUND(SUM(oi.total_price), 2)          AS lifetime_value,
    MIN(o.order_date)                      AS first_order,
    MAX(o.order_date)                      AS last_order
FROM customers c
JOIN orders o      ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id   = oi.order_id
WHERE o.order_status = 'Delivered'
GROUP BY c.customer_id, customer_name, c.city, c.region
ORDER BY lifetime_value DESC
LIMIT 10;


-- ── Query C2: Repeat vs One-Time Customers ───────────────
-- Business insight: what % of our customers bought >1 time?
WITH customer_orders AS (
    SELECT customer_id,
           COUNT(DISTINCT order_id) AS order_count
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY customer_id
)
SELECT
    CASE WHEN order_count = 1 THEN 'One-Time'
         WHEN order_count BETWEEN 2 AND 5 THEN 'Repeat (2-5)'
         ELSE 'Loyal (6+)'
    END AS customer_type,
    COUNT(*) AS customer_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM customer_orders
GROUP BY customer_type
ORDER BY customer_count DESC;


-- ── Query C3: Customer Retention Rate (Month-over-Month) ─
-- Retention = customers who bought in month N AND month N-1
WITH monthly_buyers AS (
    SELECT
        customer_id,
        DATE_FORMAT(order_date, '%Y-%m') AS order_month
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY customer_id, order_month
),
retention AS (
    SELECT
        curr.order_month,
        COUNT(DISTINCT curr.customer_id)                AS active_customers,
        COUNT(DISTINCT prev.customer_id)                AS retained_customers
    FROM monthly_buyers curr
    LEFT JOIN monthly_buyers prev
           ON curr.customer_id = prev.customer_id
          AND prev.order_month = DATE_FORMAT(
                DATE_SUB(STR_TO_DATE(CONCAT(curr.order_month, '-01'), '%Y-%m-%d'),
                         INTERVAL 1 MONTH), '%Y-%m')
    GROUP BY curr.order_month
)
SELECT
    order_month,
    active_customers,
    retained_customers,
    ROUND(retained_customers * 100.0
          / NULLIF(active_customers, 0), 2) AS retention_rate_pct
FROM retention
ORDER BY order_month;


-- ── Query C4: Customer Churn Analysis ────────────────────
-- Churn: customers with no orders in the last 6 months
-- (relative to the max date in dataset).
WITH last_order AS (
    SELECT customer_id,
           MAX(order_date) AS last_order_date
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY customer_id
),
cutoff AS (SELECT MAX(order_date) AS max_date FROM orders)
SELECT
    c.customer_id,
    CONCAT(c.first_name,' ',c.last_name) AS customer_name,
    c.region,
    lo.last_order_date,
    DATEDIFF((SELECT max_date FROM cutoff), lo.last_order_date) AS days_since_last_order,
    CASE WHEN DATEDIFF((SELECT max_date FROM cutoff), lo.last_order_date) > 180
         THEN 'Churned'
         ELSE 'Active'
    END AS churn_status
FROM customers c
LEFT JOIN last_order lo ON c.customer_id = lo.customer_id
ORDER BY days_since_last_order DESC;


-- ── Query C5: Customer Acquisition by Month ──────────────
SELECT
    DATE_FORMAT(registration_date, '%Y-%m') AS registration_month,
    COUNT(*)                                AS new_customers
FROM customers
GROUP BY registration_month
ORDER BY registration_month;


-- ════════════════════════════════════════════════════════════
-- SECTION D — REGION & GEOGRAPHY
-- ════════════════════════════════════════════════════════════

-- ── Query D1: Region-wise Sales Analysis ─────────────────
SELECT
    cu.region,
    COUNT(DISTINCT o.order_id)     AS total_orders,
    COUNT(DISTINCT cu.customer_id) AS unique_customers,
    ROUND(SUM(oi.total_price), 2)  AS total_revenue,
    ROUND(AVG(oi.total_price), 2)  AS avg_order_item_value
FROM customers cu
JOIN orders o       ON cu.customer_id = o.customer_id
JOIN order_items oi ON o.order_id     = oi.order_id
WHERE o.order_status = 'Delivered'
GROUP BY cu.region
ORDER BY total_revenue DESC;


-- ── Query D2: Top 10 Cities by Revenue ───────────────────
SELECT
    cu.city, cu.state, cu.region,
    ROUND(SUM(oi.total_price), 2)  AS revenue,
    COUNT(DISTINCT o.order_id)     AS orders
FROM customers cu
JOIN orders o       ON cu.customer_id = o.customer_id
JOIN order_items oi ON o.order_id     = oi.order_id
WHERE o.order_status = 'Delivered'
GROUP BY cu.city, cu.state, cu.region
ORDER BY revenue DESC
LIMIT 10;


-- ════════════════════════════════════════════════════════════
-- SECTION E — OPERATIONS & FULFILMENT
-- ════════════════════════════════════════════════════════════

-- ── Query E1: Order Status Distribution ──────────────────
SELECT
    order_status,
    COUNT(*) AS order_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS percentage
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;


-- ── Query E2: Payment Method Popularity ──────────────────
SELECT
    payment_method,
    COUNT(*) AS orders,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS pct
FROM orders
GROUP BY payment_method
ORDER BY orders DESC;


-- ── Query E3: Average Shipping Delay ─────────────────────
-- Delay = actual_delivery − estimated_delivery (in days).
-- Positive = late; negative = early; 0 = on-time.
SELECT
    carrier,
    COUNT(*)                                         AS shipments,
    ROUND(AVG(DATEDIFF(actual_delivery,
                       estimated_delivery)), 1)       AS avg_delay_days,
    ROUND(AVG(shipping_cost), 2)                     AS avg_shipping_cost
FROM shipping
WHERE actual_delivery IS NOT NULL
GROUP BY carrier
ORDER BY avg_delay_days;


-- ── Query E4: KPI Summary (single-row dashboard card) ────
SELECT
    ROUND(SUM(oi.total_price), 2)                AS total_revenue,
    COUNT(DISTINCT o.order_id)                   AS total_orders,
    COUNT(DISTINCT o.customer_id)                AS total_customers,
    ROUND(SUM(oi.total_price)
          / COUNT(DISTINCT o.order_id), 2)       AS avg_order_value,
    (SELECT COUNT(*) FROM customers
     WHERE status = 'Active')                    AS active_customers,
    (SELECT COUNT(*) FROM products
     WHERE stock_quantity < 20)                  AS low_stock_products
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'Delivered';

-- ============================================================
-- END OF PHASE 3 — SQL ANALYSIS QUERIES
-- ============================================================
