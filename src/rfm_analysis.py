import os
import sqlite3
import pandas as pd
import numpy as np

print("--- Début de la Segmentation RFM ---")

# Chemins dynamiques
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
db_path = os.path.join(project_root, "customer_intelligence.db")

# 1. Connexion et chargement des transactions
conn = sqlite3.connect(db_path)
df_tx = pd.read_sql("SELECT * FROM transactions", conn)

# Conversion de la date
df_tx["transaction_date"] = pd.to_datetime(df_tx["transaction_date"])
snapshot_date = df_tx["transaction_date"].max() + pd.Timedelta(days=1)
print(f"Date de référence : {snapshot_date.strftime('%Y-%m-%d')}")

# 2. Calcul RFM par client
rfm = df_tx.groupby("customer_id").agg(
    recency=("transaction_date", lambda x: (snapshot_date - x.max()).days),
    frequency=("transaction_id", "count"),
    monetary=("total_amount", "sum")
).reset_index()

# Attribution des scores de 1 à 5
rfm["R_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1], duplicates='drop')
rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["M_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])

rfm["R_score"] = rfm["R_score"].astype(int)
rfm["F_score"] = rfm["F_score"].astype(int)
rfm["M_score"] = rfm["M_score"].astype(int)
rfm["RFM_Score"] = rfm["R_score"].astype(str) + rfm["F_score"].astype(str) + rfm["M_score"].astype(str)

# 3. Fonction de labélisation (Ordre corrigé : New Customers avant Potential Loyalists)
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

# 4. Sauvegarde dans la base SQLite
rfm.to_sql("customer_rfm", conn, if_exists="replace", index=False)
conn.close()

# 5. Export propre vers le dossier data/ à la fin
output_path = os.path.join(project_root, "data", "customer_rfm.csv")
rfm.to_csv(output_path, index=False)

print("\n--- Répartition des clients par segment RFM ---")
print(rfm["segment"].value_counts())
print(f"\nPipeline RFM exécuté avec succès et exporté ici : {output_path}")
