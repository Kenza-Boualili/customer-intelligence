-- 1. Top 10 des clients selon le chiffre d'affaires
SELECT 
    c.customer_id,
    c.country,
    c.city,
    ROUND(SUM(t.total_amount), 2) AS total_revenue,
    COUNT(t.transaction_id) AS total_transactions
FROM customers c
JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY c.customer_id, c.country, c.city
ORDER BY total_revenue DESC
LIMIT 10;


-- 2. Nombre de clients par segment RFM
SELECT 
    segment,
    COUNT(customer_id) AS customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM customer_rfm), 2) AS percentage
FROM customer_rfm
GROUP BY segment
ORDER BY customer_count DESC;


-- 3. Répartition du chiffre d'affaires par segment RFM
SELECT 
    r.segment,
    ROUND(SUM(t.total_amount), 2) AS segment_revenue,
    ROUND(SUM(t.total_amount) * 100.0 / (SELECT SUM(total_amount) FROM transactions), 2) AS revenue_percentage
FROM customer_rfm r
JOIN transactions t ON r.customer_id = t.customer_id
GROUP BY r.segment
ORDER BY segment_revenue DESC;


-- 4. Identification des clients inactifs depuis plus de 180 jours (At Risk / Hibernating)
SELECT 
    customer_id,
    recency AS days_since_last_purchase,
    monetary AS total_spent,
    frequency
FROM customer_rfm
WHERE recency > 180
ORDER BY monetary DESC;


-- 5. Fréquence moyenne et panier moyen par segment RFM 
SELECT 
    r.segment,
    ROUND(AVG(r.frequency), 2) AS avg_frequency,
    ROUND(AVG(r.monetary), 2) AS avg_monetary,
    ROUND(SUM(t.total_spend) / SUM(t.total_tx), 2) AS avg_basket_size
FROM customer_rfm r
JOIN (
    SELECT customer_id, COUNT(transaction_id) AS total_tx, SUM(total_amount) AS total_spend
    FROM transactions
    GROUP BY customer_id
) t ON r.customer_id = t.customer_id
GROUP BY r.segment
ORDER BY avg_monetary DESC;


-- 6. Évolution mensuelle de la clientèle active
SELECT 
    strftime('%Y-%m', transaction_date) AS month,
    COUNT(DISTINCT customer_id) AS active_customers,
    COUNT(transaction_id) AS total_transactions,
    ROUND(SUM(total_amount), 2) AS monthly_revenue
FROM transactions
GROUP BY month
ORDER BY month ASC;
