import os
import sqlite3
import pandas as pd
import numpy as np

print("--- Début de la Segmentation RFM ---")

# Chemins dynamiques
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
db_path = os.path.join(project_root, "customer_intelligence.db")

# Connexion à la base et lecture de la table RFM
conn = sqlite3.connect(db_path)
df_rfm = pd.read_sql("SELECT * FROM customer_rfm", conn)
conn.close()

# Sauvegarde dans le dossier data/
output_path = os.path.join(project_root, "data", "customer_rfm.csv")
df_rfm.to_csv(output_path, index=False)
print(f"Fichier exporté avec succès ici : {output_path}")

# Connexion à SQLite
conn = sqlite3.connect(db_path)

# Charger les transactions
df_tx = pd.read_sql("SELECT * FROM transactions", conn)

# Convertir la date de transaction en datetime
df_tx["transaction_date"] = pd.to_datetime(df_tx["transaction_date"])

# Définir une date de référence (lendemain de la dernière transaction observée)
snapshot_date = df_tx["transaction_date"].max() + pd.Timedelta(days=1)
print(f"Date de référence pour le calcul de la Récence : {snapshot_date.strftime('%Y-%m-%d')}")

# Calcul RFM par client
rfm = df_tx.groupby("customer_id").agg(
    recency=("transaction_date", lambda x: (snapshot_date - x.max()).days),
    frequency=("transaction_id", "count"),
    monetary=("total_amount", "sum")
).reset_index()

# Attribution des scores de 1 à 5 (5 étant le meilleur)
# Pour la Récence, les plus petits délais sont les meilleurs (donc qcut inversé avec labels=[5, 4, 3, 2, 1])
rfm["R_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1], duplicates='drop')
# Pour la Fréquence et le Monétaire, les plus grands nombres sont les meilleurs (labels=[1, 2, 3, 4, 5])
rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["M_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])

# Convertir les scores en entiers
rfm["R_score"] = rfm["R_score"].astype(int)
rfm["F_score"] = rfm["F_score"].astype(int)
rfm["M_score"] = rfm["M_score"].astype(int)

# Score RFM combiné (chaîne de caractères pour lisibilité)
rfm["RFM_Score"] = rfm["R_score"].astype(str) + rfm["F_score"].astype(str) + rfm["M_score"].astype(str)

# Fonction de labélisation des segments clients
def segment_customer(row):
    r, f, m = row["R_score"], row["F_score"], row["M_score"]
    
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    elif r >= 3 and f >= 3:
        return "Loyal Customers"
    elif r == 5 and f == 1:
        return "New Customers"
    elif r >= 4 and f <= 2:
        return "Potential Loyalists"
    elif r <= 2 and f >= 3:
        return "At Risk"
    elif r <= 2 and f <= 2 and m >= 3:
        return "Big Spenders"
    elif r <= 2 and f <= 2:
        return "Hibernating"
    else:
        return "Potential Loyalists"

rfm["segment"] = rfm.apply(segment_customer, axis=1)

# Sauvegarder le résultat RFM dans la base de données SQLite
rfm.to_sql("customer_rfm", conn, if_exists="replace", index=False)

print("\n--- Répartition des clients par segment RFM ---")
segment_counts = rfm["segment"].value_counts()
print(segment_counts)

# Fermeture de la connexion
conn.close()
print("\nSegmentation RFM calculée et sauvegardée dans la base de données avec succès !")
