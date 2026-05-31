---
title: "SQL Essentials for Data Engineers"
date: "2026-03-01"
category: "Software Engineering"
excerpt: "Beyond basic SELECT queries — window functions, CTEs, query optimization, and patterns that separate production data engineers from casual users."
---

# SQL Essentials for Data Engineers

SQL is the lingua franca of data engineering. While basic queries get you started, production data work demands deeper knowledge of window functions, Common Table Expressions, query optimization, and robust pipeline patterns.

## Window Functions: Analytics Without Self-Joins

Window functions perform calculations across rows related to the current row without collapsing the result set:

```sql
SELECT
    department,
    employee_name,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank,
    AVG(salary) OVER (PARTITION BY department) as dept_avg,
    salary - AVG(salary) OVER (PARTITION BY department) as above_avg
FROM employees;
```

Key window functions:
- **ROW_NUMBER()**: Sequential row numbering within partitions
- **RANK() / DENSE_RANK()**: Ranking with gaps (RANK) or without (DENSE_RANK)
- **LAG() / LEAD()**: Access previous or next row values
- **SUM() OVER**: Running totals and moving averages

## Common Table Expressions: Modular Queries

CTEs make complex queries readable and debuggable by breaking them into named steps:

```sql
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', order_date) as month,
        SUM(amount) as revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY 1
),
growth AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) as prev_revenue,
        ROUND(
            (revenue - LAG(revenue) OVER (ORDER BY month)) /
            NULLIF(LAG(revenue) OVER (ORDER BY month), 0) * 100,
            2
        ) as growth_pct
    FROM monthly_revenue
)
SELECT * FROM growth
WHERE prev_revenue IS NOT NULL
ORDER BY growth_pct DESC;
```

## Query Optimization Patterns

Slow queries are the most common production issue. These patterns consistently improve performance:

### Filter Early, Filter Often

Apply WHERE clauses before joins to reduce the data volume entering expensive operations:

```sql
-- Slow: filters after join
SELECT *
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.order_date >= '2026-01-01';

-- Fast: filters before join
SELECT *
FROM customers c
JOIN (SELECT * FROM orders WHERE order_date >= '2026-01-01') o
    ON c.id = o.customer_id;
```

### Indexing Strategy

| Query Pattern | Index Type | Example |
|--------------|-----------|---------|
| Exact lookup | B-tree | `WHERE id = 42` |
| Range queries | B-tree (sorted) | `WHERE date > '2026-01-01'` |
| Text search | GIN/trigram | `WHERE name ILIKE '%search%'` |
| JSON queries | GIN | `WHERE metadata->>'key' = 'value'` |

### EXPLAIN ANALYZE

Always profile queries before optimizing:

```sql
EXPLAIN ANALYZE
SELECT customer_id, COUNT(*)
FROM orders
WHERE status = 'pending'
GROUP BY customer_id;
```

Look for sequential scans on large tables, high row estimates vs actuals, and sorts spilling to disk.

## Pipeline Patterns

### Incremental Loading

Instead of full reloads, process only changed records:

```sql
-- Using a watermark table
INSERT INTO analytics.daily_orders
SELECT *
FROM raw.orders
WHERE updated_at > (SELECT last_processed FROM pipeline_watermark WHERE table_name = 'orders');
```

### Idempotent Upserts

Ensure pipelines can be re-run safely:

```sql
MERGE INTO target_table AS t
USING source_table AS s
ON t.id = s.id
WHEN MATCHED THEN UPDATE SET
    t.value = s.value,
    t.updated_at = CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN INSERT (id, value, created_at)
VALUES (s.id, s.value, CURRENT_TIMESTAMP);
```

## Conclusion

SQL mastery separates data engineers who can ship reliable pipelines from those who write fragile, slow queries. Invest in window functions, CTEs, and optimization patterns — they pay dividends on every project.
