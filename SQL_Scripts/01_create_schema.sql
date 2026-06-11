-- ============================================================
-- PHASE 2: DATABASE DESIGN & SCHEMA
-- E-Commerce Sales & Customer Analytics Dashboard
-- ============================================================
-- Database : ecommerce_analytics
-- Author   : Ajay Kumar
-- Purpose  : Normalized relational schema with PKs, FKs,
--            indexes, and comments for every table.
-- Run on   : MySQL 8.0+
-- ============================================================

-- ── 0. Create & select database ──────────────────────────
DROP DATABASE IF EXISTS ecommerce_analytics;
CREATE DATABASE ecommerce_analytics
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE ecommerce_analytics;

-- ============================================================
-- TABLE 1: categories
--   Lookup table for product categories.
--   Keeps products table normalised (no repeated strings).
-- ============================================================
CREATE TABLE categories (
    category_id   INT            NOT NULL AUTO_INCREMENT,
    category_name VARCHAR(100)   NOT NULL,
    description   VARCHAR(255)       NULL,

    CONSTRAINT pk_categories PRIMARY KEY (category_id),
    CONSTRAINT uq_category_name UNIQUE (category_name)
);

-- ============================================================
-- TABLE 2: products
--   Master catalogue. References categories via FK.
--   Stores pricing, cost (for margin calculations),
--   stock levels, and crowd-sourced ratings.
-- ============================================================
CREATE TABLE products (
    product_id      INT             NOT NULL AUTO_INCREMENT,
    product_name    VARCHAR(200)    NOT NULL,
    category_id     INT             NOT NULL,
    price           DECIMAL(10, 2)  NOT NULL,
    cost_price      DECIMAL(10, 2)  NOT NULL,
    stock_quantity  INT             NOT NULL DEFAULT 0,
    avg_rating      DECIMAL(3, 1)       NULL,
    review_count    INT                 NULL DEFAULT 0,
    is_active       TINYINT(1)          NOT NULL DEFAULT 1,   -- soft delete flag
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_products   PRIMARY KEY (product_id),
    CONSTRAINT fk_prod_cat   FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,

    -- Speeds up category-level aggregations
    INDEX idx_products_category (category_id),
    INDEX idx_products_price    (price)
);

-- ============================================================
-- TABLE 3: customers
--   One row per registered user.
--   Region column is a derived/denormalised field included
--   intentionally for BI region-slice performance.
-- ============================================================
CREATE TABLE customers (
    customer_id       INT          NOT NULL AUTO_INCREMENT,
    first_name        VARCHAR(80)  NOT NULL,
    last_name         VARCHAR(80)  NOT NULL,
    email             VARCHAR(150) NOT NULL,
    phone             VARCHAR(20)      NULL,
    dob               DATE             NULL,
    gender            ENUM('Male','Female','Other') NULL,
    city              VARCHAR(100)     NULL,
    state             VARCHAR(100)     NULL,
    region            VARCHAR(50)      NULL,
    registration_date DATE         NOT NULL,
    status            ENUM('Active','Inactive') NOT NULL DEFAULT 'Active',

    CONSTRAINT pk_customers     PRIMARY KEY (customer_id),
    CONSTRAINT uq_customer_email UNIQUE (email),

    INDEX idx_cust_region (region),
    INDEX idx_cust_status (status),
    INDEX idx_cust_reg_date (registration_date)
);

-- ============================================================
-- TABLE 4: orders
--   Header-level record per transaction.
--   Line items live in order_items for proper normalisation.
-- ============================================================
CREATE TABLE orders (
    order_id        INT          NOT NULL AUTO_INCREMENT,
    customer_id     INT          NOT NULL,
    order_date      DATE         NOT NULL,
    order_status    ENUM('Processing','Shipped','Delivered',
                         'Cancelled','Returned') NOT NULL DEFAULT 'Processing',
    payment_method  VARCHAR(50)  NOT NULL,
    discount_percent DECIMAL(5,2) NOT NULL DEFAULT 0.00,

    CONSTRAINT pk_orders    PRIMARY KEY (order_id),
    CONSTRAINT fk_ord_cust  FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,

    INDEX idx_orders_customer   (customer_id),
    INDEX idx_orders_date       (order_date),
    INDEX idx_orders_status     (order_status)
);

-- ============================================================
-- TABLE 5: order_items
--   Line items — one row per product per order.
--   total_price stores (unit_price × quantity × (1−discount))
--   as a computed-but-stored value for query speed.
-- ============================================================
CREATE TABLE order_items (
    item_id     INT             NOT NULL AUTO_INCREMENT,
    order_id    INT             NOT NULL,
    product_id  INT             NOT NULL,
    quantity    INT             NOT NULL DEFAULT 1,
    unit_price  DECIMAL(10, 2)  NOT NULL,
    discount    DECIMAL(5, 2)   NOT NULL DEFAULT 0.00,
    total_price DECIMAL(10, 2)  NOT NULL,

    CONSTRAINT pk_order_items  PRIMARY KEY (item_id),
    CONSTRAINT fk_oi_order     FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_oi_product   FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,

    INDEX idx_oi_order   (order_id),
    INDEX idx_oi_product (product_id)
);

-- ============================================================
-- TABLE 6: shipping
--   Fulfilment record for Delivered / Shipped orders.
--   One row per order_id (enforced by PK on order_id).
-- ============================================================
CREATE TABLE shipping (
    order_id            INT          NOT NULL,
    carrier             VARCHAR(100) NOT NULL,
    tracking_number     VARCHAR(50)      NULL,
    ship_date           DATE             NULL,
    estimated_delivery  DATE             NULL,
    actual_delivery     DATE             NULL,
    delivery_status     VARCHAR(50)      NULL,
    shipping_cost       DECIMAL(8, 2)    NULL DEFAULT 0.00,

    CONSTRAINT pk_shipping    PRIMARY KEY (order_id),
    CONSTRAINT fk_ship_order  FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE ON UPDATE CASCADE,

    INDEX idx_ship_status (delivery_status),
    INDEX idx_ship_date   (ship_date)
);

-- ── Verify schema ─────────────────────────────────────────
SHOW TABLES;
-- Expected: categories, customers, order_items, orders,
--           products, shipping

-- ============================================================
-- END OF PHASE 2 — DATABASE DESIGN
-- ============================================================
