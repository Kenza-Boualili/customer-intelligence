# 💎 Luxury Retail Customer Intelligence & RFM Analytics Dashboard

## Executive Summary

This project delivers an end-to-end business intelligence and client intelligence solution tailored for high-end luxury houses (*Maison de Luxe*). Designed to align with the analytical standards of leading prestige groups like **LVMH, Hermès, and Kering**, this interactive platform synthesizes total enterprise revenue, customer count, average spend per client, dynamic country filtering, and deep **RFM (Recency, Frequency, Monetary) segmentation**. All datasets used in this project are synthetically generated for educational and analytical purposes. No real customer or company data is used.

The architecture spans the full data analytics lifecycle:

1. **Data Engineering & Preparation** via Python (`pandas`, `numpy`) and **Power Query** (Locale US formatting & type casting).
2. **Relational Data Modeling & RFM Segmentation** via SQL (`sqlite3`) and DAX Engine.
3. **Interactive Executive Visualization** via Power BI (*Minimalist Dark `#121212` & Gold `#D4AF37` Theme*).

---

## 🛠️ Technical Architecture & Stack

| Layer | Technology | Usage & Functionality |
| :--- | :--- | :--- |
| **Data Engine** | `Python 3.10+` | Dataset orchestration, transaction modeling, schema normalization |
| **Data Transformation** | `Power Query (M)` | Decimal conversion, culture handling (US Locale), string clean-up |
| **Visual Analytics** | `Power BI Desktop` | Interactive dynamic slicers, DAX measures, luxury aesthetic custom styling |
| **Documentation** | `Markdown / VS Code` | Technical reporting and executive insights |

---

## 📊 Business Metrics & Key Performance Indicators

- **Total Revenue:** `€114.70M`
- **Total Active Customers:** `2,000`
- **Average Spend per Customer:** `€57.37K`
- **Primary RFM Revenue Driver:** `Champions Segment`
- **Geographic Markets:** `France, USA, Japan`

---

## 💻 Relational Database & DAX Formulations

### DAX Measures (`pbix/measures.dax`)

```dax
-- ============================================================
-- LUXURY RETAIL ANALYTICS — DAX MEASURES
-- ============================================================

-- 1. Total Enterprise Revenue
Total Revenue = SUM(transactions[total_amount])

-- 2. Total Unique Active Customers
Total Customers = DISTINCTCOUNT(customers[customer_id])

-- 3. Average Spend per Customer
Avg Customer Spend = DIVIDE([Total Revenue], [Total Customers], 0)
```

### SQL Interrogation Queries (`queries.sql`)

```sql
-- ============================================================
-- RFM & VIP CLIENT ANALYSIS QUERIES
-- ============================================================

-- 1. Revenue & Customer Distribution by RFM Segment
SELECT 
    r.segment,
    COUNT(DISTINCT r.customer_id) AS total_customers,
    ROUND(SUM(t.total_amount), 2) AS total_revenue,
    ROUND(AVG(t.total_amount), 2) AS avg_spend_per_customer
FROM customer_rfm r
JOIN transactions t ON r.customer_id = t.customer_id
GROUP BY r.segment
ORDER BY total_revenue DESC;

-- 2. Top 10 VIP High-Net-Worth Individual (HNWI) Client Identification
SELECT 
    c.customer_id,
    c.country,
    r.segment,
    ROUND(SUM(t.total_amount), 2) AS total_revenue
FROM customers c
JOIN customer_rfm r ON c.customer_id = r.customer_id
JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY c.customer_id, c.country, r.segment
ORDER BY total_revenue DESC
LIMIT 10;
```

---

## 🎯 Strategic Business Recommendations

### 1. Capitalization on the *Champions* RFM Segment
- **Finding:** The *Champions* segment contributes the highest proportion of the €114.70M total revenue.
- **Action:** Design hyper-personalized clienteling initiatives, including early access to limited edition high-jewelry collections and exclusive private salon events in Paris, Tokyo, and New York.

### 2. High Average Spend Optimization (€57.37K / Client)
- **Finding:** Average spend per client stands at a high €57.37K, confirming strong brand equity and multi-category purchasing.
- **Action:** Expand cross-category concierge recommendations (e.g., pairing high-watchmaking acquisitions with custom leather goods) to further elevate ticket size.

### 3. Targeted Re-engagement Strategy for *At Risk* Clients
- **Finding:** A noticeable subset of formerly high-spending clients show declining recency scores (*At Risk*).
- **Action:** Empower Client Advisors with automated alerts to offer bespoke anniversary gifts or private home appointments to re-ignite engagement before churn occurs.

---

<p align="center">
  <i>Designed for Executive Analytics & Luxury Retail Strategy</i>
</p>