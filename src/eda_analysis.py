import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration du style graphique pour un univers "luxe" (épuré, sombre/clair chic)
sns.set_theme(style="whitegrid")

# Chemins dynamiques
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
db_path = os.path.join(project_root, "customer_intelligence.db")

# Connexion à la base de données SQLite
conn = sqlite3.connect(db_path)

print("--- 1. STATISTIQUES GLOBALES ---")

# Nombre total de clients et de transactions
df_cust = pd.read_sql("SELECT * FROM customers", conn)
df_tx = pd.read_sql("SELECT * FROM transactions", conn)

print(f"Nombre total de clients : {len(df_cust):,}")
print(f"Nombre total de transactions : {len(df_tx):,}")

# Chiffre d'affaires total
total_revenue = df_tx["total_amount"].sum()
print(f"Chiffre d'affaires global : {total_revenue:,.2f} €")

# Dépense moyenne par client
spend_per_customer = df_tx.groupby("customer_id")["total_amount"].sum()
avg_spend = spend_per_customer.mean()
print(f"Dépense moyenne par client : {avg_spend:,.2f} €")


print("\n--- 2. ANALYSE PAR CATÉGORIE DE PRODUITS ---")
cat_analysis = df_tx.groupby("category").agg(
    total_sales=("total_amount", "sum"),
    avg_price=("unit_price", "mean"),
    transaction_count=("transaction_id", "count")
).reset_index().sort_values(by="total_sales", ascending=False)

print(cat_analysis)


print("\n--- 3. TOP 5 DES PAYS PAR CHIFFRE D'AFFAIRES ---")
# Joindre transactions et customers pour analyser par pays
query_country = """
    SELECT c.country, SUM(t.total_amount) as revenue, COUNT(t.transaction_id) as tx_count
    FROM transactions t
    JOIN customers c ON t.customer_id = c.customer_id
    GROUP BY c.country
    ORDER BY revenue DESC
"""
df_country = pd.read_sql(query_country, conn)
print(df_country.head())

# Fermeture de la connexion
conn.close()
print("\nAnalyse exploratoire de base terminée avec succès !")