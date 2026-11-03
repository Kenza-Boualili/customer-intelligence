import os
import sqlite3
import pandas as pd

print("--- Connexion à SQLite et création de la base de données ---")

# Obtenir le dossier où se trouve ce script (src/)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Remonter d'un cran pour atteindre la racine du projet (customer-intelligence/)
project_root = os.path.dirname(script_dir)

# Chemins absolus vers la base de données et les fichiers CSV
db_path = os.path.join(project_root, "customer_intelligence.db")
customers_path = os.path.join(project_root, "data", "customers.csv")
transactions_path = os.path.join(project_root, "data", "transactions.csv")

# Connexion à SQLite (crée le fichier s'il n'existe pas)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print(f"Base de données SQLite créée/ouverte avec succès : {db_path}")

# 1. Charger les données CSV
print("Chargement des fichiers CSV...")
df_customers = pd.read_csv(customers_path)
df_transactions = pd.read_csv(transactions_path)

# 2. Insérer les DataFrames dans des tables SQL
print("Insertion des données dans les tables SQL 'customers' et 'transactions'...")
df_customers.to_sql("customers", conn, if_exists="replace", index=False)
df_transactions.to_sql("transactions", conn, if_exists="replace", index=False)

# 3. Vérification rapide avec une requête SQL de test
print("\nVérification des tables créées :")
query_test = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql(query_test, conn)
print(tables)

# Compter le nombre de lignes dans chaque table
n_cust_sql = pd.read_sql("SELECT COUNT(*) as count FROM customers", conn)["count"][0]
n_tx_sql = pd.read_sql("SELECT COUNT(*) as count FROM transactions", conn)["count"][0]

print(f"-> Table 'customers' : {n_cust_sql} lignes.")
print(f"-> Table 'transactions' : {n_tx_sql} lignes.")

# Fermeture de la connexion
conn.close()
print("\nBase de données initialisée et fermée proprement !")