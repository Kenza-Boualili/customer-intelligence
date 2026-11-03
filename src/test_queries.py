import sqlite3
import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
conn = sqlite3.connect(os.path.join(project_root, "customer_intelligence.db"))

print("--- Test de la requête : Top 10 clients ---")
top_clients = pd.read_sql("""
    SELECT c.customer_id, c.country, SUM(t.total_amount) AS total_revenue
    FROM customers c JOIN transactions t ON c.customer_id = t.customer_id
    GROUP BY c.customer_id ORDER BY total_revenue DESC LIMIT 5
""", conn)
print(top_clients)

conn.close()
