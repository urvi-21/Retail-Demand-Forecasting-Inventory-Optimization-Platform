-- ==========================================================
-- 1. Total Revenue
-- ==========================================================
SELECT
    SUM(weekly_sales) AS total_revenue
FROM sales;

-- ==========================================================
-- 2. Top 10 Stores by Revenue
-- ==========================================================
SELECT
    store,
    SUM(weekly_sales) AS revenue
FROM sales
GROUP BY store
ORDER BY revenue DESC
LIMIT 10;

-- ==========================================================
-- 3. Bottom 10 Stores by Revenue
-- ==========================================================
SELECT
    store,
    SUM(weekly_sales) AS revenue
FROM sales
GROUP BY store
ORDER BY revenue
LIMIT 10;

-- ==========================================================
-- 4. Top 10 Departments
-- ==========================================================
SELECT
    dept,
    SUM(weekly_sales) AS revenue
FROM sales
GROUP BY dept
ORDER BY revenue DESC
LIMIT 10;

-- ==========================================================
-- 5. Revenue by Store Type
-- ==========================================================
SELECT
    st.type,
    SUM(sa.weekly_sales) AS revenue
FROM sales sa
JOIN stores st
ON sa.store = st.store
GROUP BY st.type
ORDER BY revenue DESC;

-- ==========================================================
-- 6. Holiday vs Non-Holiday Sales
-- ==========================================================
SELECT
    is_holiday,
    AVG(weekly_sales) AS avg_sales
FROM sales
GROUP BY is_holiday;

-- ==========================================================
-- 7. Monthly Revenue
-- ==========================================================
SELECT
    EXTRACT(MONTH FROM date) AS month,
    SUM(weekly_sales) AS revenue
FROM sales
GROUP BY month
ORDER BY month;

-- ==========================================================
-- 8. Quarterly Revenue
-- ==========================================================
SELECT
    EXTRACT(QUARTER FROM date) AS quarter,
    SUM(weekly_sales) AS revenue
FROM sales
GROUP BY quarter
ORDER BY quarter;

-- ==========================================================
-- 9. Yearly Revenue
-- ==========================================================
SELECT
    EXTRACT(YEAR FROM date) AS year,
    SUM(weekly_sales) AS revenue
FROM sales
GROUP BY year
ORDER BY year;

-- ==========================================================
-- 10. Store Ranking
-- ==========================================================
SELECT
    store,
    SUM(weekly_sales) AS revenue,
    RANK() OVER (
        ORDER BY SUM(weekly_sales) DESC
    ) AS store_rank
FROM sales
GROUP BY store;

-- ==========================================================
-- 11. Revenue Contribution Percentage
-- ==========================================================
SELECT
    store,
    ROUND(
        100.0 * SUM(weekly_sales) /
        (SELECT SUM(weekly_sales) FROM sales),
        2
    ) AS contribution_percent
FROM sales
GROUP BY store
ORDER BY contribution_percent DESC;

-- ==========================================================
-- 12. Highest Revenue Weeks
-- ==========================================================
SELECT
    date,
    SUM(weekly_sales) AS revenue
FROM sales
GROUP BY date
ORDER BY revenue DESC
LIMIT 10;

-- ==========================================================
-- 13. Store Type Statistics
-- ==========================================================
SELECT
    type,
    AVG(size) AS avg_size,
    MAX(size) AS max_size,
    MIN(size) AS min_size
FROM stores
GROUP BY type;

-- ==========================================================
-- 14. Sales by Year and Month
-- ==========================================================
SELECT
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(MONTH FROM date) AS month,
    SUM(weekly_sales) AS revenue
FROM sales
GROUP BY year, month
ORDER BY year, month;

-- ==========================================================
-- 15. Revenue by Store Type and Year
-- ==========================================================
SELECT
    st.type,
    EXTRACT(YEAR FROM sa.date) AS year,
    SUM(sa.weekly_sales) AS revenue
FROM sales sa
JOIN stores st
ON sa.store = st.store
GROUP BY st.type, year
ORDER BY year, revenue DESC;

-- ==========================================================
-- 16. Department Sales Volatility
-- ==========================================================
SELECT
    dept,
    STDDEV(weekly_sales) AS sales_volatility
FROM sales
GROUP BY dept
ORDER BY sales_volatility DESC;

-- ==========================================================
-- 17. Rolling 4-Week Revenue
-- ==========================================================
SELECT
    date,
    SUM(weekly_sales) AS weekly_revenue,
    AVG(
        SUM(weekly_sales)
    ) OVER (
        ORDER BY date
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ) AS rolling_4week_avg
FROM sales
GROUP BY date
ORDER BY date;

-- ==========================================================
-- 18. Top Holiday Weeks
-- ==========================================================
SELECT
    date,
    SUM(weekly_sales) AS revenue
FROM sales
WHERE is_holiday = TRUE
GROUP BY date
ORDER BY revenue DESC
LIMIT 5;

-- ==========================================================
-- 19. Average Sales by Store Type
-- ==========================================================
SELECT
    st.type,
    AVG(sa.weekly_sales) AS avg_sales
FROM sales sa
JOIN stores st
ON sa.store = st.store
GROUP BY st.type;

-- ==========================================================
-- 20. Largest Stores
-- ==========================================================
SELECT
    store,
    size
FROM stores
ORDER BY size DESC
LIMIT 10;

-- ==========================================================
-- 21. Highest Selling Department Per Store
-- ==========================================================
SELECT
    store,
    dept,
    revenue
FROM (
    SELECT
        store,
        dept,
        SUM(weekly_sales) AS revenue,
        RANK() OVER (
            PARTITION BY store
            ORDER BY SUM(weekly_sales) DESC
        ) AS rnk
    FROM sales
    GROUP BY store, dept
) t
WHERE rnk = 1;

-- ==========================================================
-- 22. Monthly Temperature and Sales
-- ==========================================================
SELECT
    EXTRACT(MONTH FROM f.date) AS month,
    AVG(f.temperature) AS avg_temperature,
    AVG(s.weekly_sales) AS avg_sales
FROM sales s
JOIN features f
ON s.store = f.store
AND s.date = f.date
GROUP BY month
ORDER BY month;
# ==========================================================
23. Top Store Within Each Store Type
# ==========================================================
SELECT
    type,
    store,
    revenue
FROM
(
    SELECT
        st.type,
        sa.store,
        SUM(sa.weekly_sales) AS revenue,
        RANK() OVER (
            PARTITION BY st.type
            ORDER BY SUM(sa.weekly_sales) DESC
        ) AS rnk
    FROM sales sa
    JOIN stores st
    ON sa.store = st.store
    GROUP BY st.type, sa.store
) t
WHERE rnk = 1;