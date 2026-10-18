/* ============================================================
REPORT A: ORDER TOTALS

Expected Output:
total_orders | total_revenue | avg_order_value
------------------------------------------------
180          | 99860.20      | 554.78
============================================================ */

SELECT
    COUNT(*) AS total_orders,
    ROUND(
        SUM(
            o.quantity *
            p.price *
            (1 - COALESCE(o.discount_pct, 0)/100.0)
        ),
        2
    ) AS total_revenue,
    ROUND(
        AVG(
            o.quantity *
            p.price *
            (1 - COALESCE(o.discount_pct, 0)/100.0)
        ),
        2
    ) AS avg_order_value
FROM orders o
JOIN products p
ON o.product_id = p.product_id;



/* ============================================================
REPORT B: COUNT(*) VS COUNT(RATING)

Expected Output:
total_rows | rating_count | missing_ratings
--------------------------------------------
180        | 165          | 15
============================================================ */

SELECT
    COUNT(*) AS total_rows,
    COUNT(rating) AS rating_count,
    COUNT(*) - COUNT(rating) AS missing_ratings
FROM orders;



/* ============================================================
REPORT C1: CUSTOMER WITH ZERO ORDERS USING LEFT JOIN

Expected Output:
customer_id | name
------------------
C045        | Vihaan
============================================================ */

SELECT
    c.customer_id,
    c.name
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) = 0;



/* ============================================================
REPORT C2: VALIDATION USING NOT IN

Expected Output:
customer_id | name
------------------
C045        | Vihaan
============================================================ */

SELECT
    customer_id,
    name
FROM customers
WHERE customer_id NOT IN (
    SELECT DISTINCT customer_id
    FROM orders
);



/* ============================================================
REPORT D: RETURN RATE BY CITY

Expected Output:

city       | total_orders | returned_orders | return_rate_pct
-------------------------------------------------------------
Jaipur     | 19           | 8               | 42.1
Lucknow    | 49           | 15              | 30.6
Bangalore  | 33           | 8               | 24.2
============================================================ */

SELECT
    c.city,
    COUNT(*) AS total_orders,
    SUM(o.returned) AS returned_orders,
    ROUND(
        100.0 * SUM(o.returned) / COUNT(*),
        1
    ) AS return_rate_pct
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY c.city
HAVING ROUND(
        100.0 * SUM(o.returned) / COUNT(*),
        1
      ) > 20
ORDER BY return_rate_pct DESC;



/* ============================================================
REPORT E1: TOP 5 CUSTOMERS BY TOTAL SPEND

Tie-break note:
customer_id ASC guarantees deterministic ordering
when two customers have identical spend values.

Expected Output:

customer_id | name     | total_spend
-------------------------------------
C043        | Reyansh  | 12920.00
C026        | Isha     | 8371.60
C008        | Meera    | 4564.60
C011        | Arjun    | 4111.00
C042        | Sanya    | 3785.00
============================================================ */

SELECT
    c.customer_id,
    c.name,
    ROUND(
        SUM(
            o.quantity *
            p.price *
            (1 - COALESCE(o.discount_pct,0)/100.0)
        ),
        2
    ) AS total_spend
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC,
         c.customer_id ASC
LIMIT 5;



/* ============================================================
REPORT E2: RANKS 3-5 USING LIMIT OFFSET

Expected Output:

customer_id | name    | total_spend
------------------------------------
C008        | Meera   | 4564.60
C011        | Arjun   | 4111.00
C042        | Sanya   | 3785.00
============================================================ */

SELECT
    c.customer_id,
    c.name,
    ROUND(
        SUM(
            o.quantity *
            p.price *
            (1 - COALESCE(o.discount_pct,0)/100.0)
        ),
        2
    ) AS total_spend
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC,
         c.customer_id ASC
LIMIT 3 OFFSET 2;



/* ============================================================
REPORT F: REVENUE BY CATEGORY

Expected Output:

category      | order_count | category_revenue
----------------------------------------------
Haircare      | 54          | 44956.10
Skincare      | 60          | 27346.00
Babycare      | 30          | 16805.00
PersonalCare  | 36          | 10753.10
============================================================ */

SELECT
    p.category,
    COUNT(*) AS order_count,
    ROUND(
        SUM(
            o.quantity *
            p.price *
            (1 - COALESCE(o.discount_pct,0)/100.0)
        ),
        2
    ) AS category_revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY p.category
ORDER BY category_revenue DESC;



/* ============================================================
REPORT G: CUSTOMER NAMES STARTING WITH 'A'

Expected Output:
10 rows
============================================================ */

SELECT *
FROM customers
WHERE name LIKE 'A%';



/* ============================================================
REPORT H: DISTINCT ACQUISITION SOURCES

Expected Output:

Ad
Organic
Referral
Social
============================================================ */

SELECT DISTINCT acquisition_source
FROM customers
ORDER BY acquisition_source;



/* ============================================================
REPORT I: ALTER TABLE + CASE UPDATE

Expected Output:

loyalty_tier | customer_count
-----------------------------
Gold         | 28
Silver       | 17
============================================================ */

ALTER TABLE customers
ADD COLUMN loyalty_tier VARCHAR(10);

UPDATE customers
SET loyalty_tier =
CASE
    WHEN city_tier = 1 THEN 'Gold'
    ELSE 'Silver'
END;

SELECT
    loyalty_tier,
    COUNT(*) AS customer_count
FROM customers
GROUP BY loyalty_tier
ORDER BY loyalty_tier;
