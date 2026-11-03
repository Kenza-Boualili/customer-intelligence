import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Fixer la reproductibilité pour obtenir les mêmes résultats à chaque exécution
np.random.seed(42)
random.seed(42)

# Créer les dossiers nécessaires s'ils n'existent pas
os.makedirs("data", exist_ok=True)
os.makedirs("src", exist_ok=True)
os.makedirs("notebooks", exist_ok=True)
os.makedirs("sql", exist_ok=True)
os.makedirs("powerbi", exist_ok=True)
os.makedirs("images", exist_ok=True)

print("--- 1. Génération des clients (Customers) ---")

n_customers = 2000
start_date_customers = datetime(2024, 1, 1)
end_date_customers = datetime(2025, 6, 30)  # Inscriptions sur 1 an et demi

countries_cities = {
    "France": ["Paris", "Nice", "Cannes"],
    "United States": ["New York", "Los Angeles", "Miami"],
    "Japan": ["Tokyo", "Osaka"],
    "United Kingdom": ["London"],
    "Italy": ["Milan", "Rome"],
    "United Arab Emirates": ["Dubai"],
}

# Liste des IDs clients (corrigée)
customer_ids = [f"CUST_{i:05d}" for i in range(1, n_customers + 1)]

signup_dates = [
    start_date_customers
    + timedelta(
        seconds=random.randint(
            0, int((end_date_customers - start_date_customers).total_seconds())
        )
    )
    for _ in range(n_customers)
]

countries = []
cities = []
for _ in range(n_customers):
    country = random.choices(
        list(countries_cities.keys()), weights=[30, 25, 20, 10, 10, 5], k=1
    )[0]
    city = random.choice(countries_cities[country])
    countries.append(country)
    cities.append(city)

df_customers = pd.DataFrame(
    {
        "customer_id": customer_ids,
        "signup_date": signup_dates,
        "country": countries,
        "city": cities,
    }
)

# Sauvegarde des clients
df_customers.to_csv("data/customers.csv", index=False)
print(f"-> {len(df_customers)} clients générés et sauvegardés dans data/customers.csv")


print("\n--- 2. Génération des transactions (Transactions) ---")

n_transactions = 15000
categories_prices = {
    "Maroquinerie": (2000, 8000),
    "Joaillerie": (5000, 30000),
    "Horlogerie": (4000, 25000),
    "Prêt-à-porter": (1500, 6000),
    "Chaussures": (700, 2000),
    "Parfums & Beauté": (150, 450),
}

transaction_ids = [f"TXN_{i:06d}" for i in range(1, n_transactions + 1)]

# Sélection aléatoire des clients (les clients VIP achètent plus souvent)
vip_customers = np.random.choice(
    customer_ids, size=int(n_customers * 0.2), replace=False
)
weights = [
    5 if cid in vip_customers else 1 for cid in df_customers["customer_id"]
]
weights = np.array(weights) / sum(weights)

sampled_customers = np.random.choice(
    customer_ids, size=n_transactions, p=weights, replace=True
)

tx_dates = []
categories = []
quantities = []
unit_prices = []
store_names = []

stores = [
    "Boutique Paris Faubourg",
    "Boutique NY Fifth Ave",
    "Boutique Tokyo Ginza",
    "Boutique London New Bond",
    "Boutique Milan Montenapoleone",
    "Boutique Dubai Mall",
]

for cust_id in sampled_customers:
    # Récupérer la date d'inscription du client pour que la transaction soit postérieure
    cust_signup = df_customers.loc[
        df_customers["customer_id"] == cust_id, "signup_date"
    ].values[0]
    cust_signup_dt = pd.to_datetime(cust_signup)

    # Date de transaction entre l'inscription et le 31 décembre 2025
    max_date = datetime(2025, 12, 31)
    if cust_signup_dt >= max_date:
        tx_date = cust_signup_dt
    else:
        delta_seconds = int((max_date - cust_signup_dt).total_seconds())
        tx_date = cust_signup_dt + timedelta(
            seconds=random.randint(0, max(1, delta_seconds))
        )
    tx_dates.append(tx_date)

    # Catégorie de produit
    cat = random.choices(
        list(categories_prices.keys()),
        weights=[35, 15, 15, 20, 10, 5],
        k=1,
    )[0]
    categories.append(cat)

    # Prix unitaire selon la catégorie
    min_p, max_p = categories_prices[cat]
    price = round(
        np.random.triangular(min_p, min_p + (max_p - min_p) * 0.2, max_p), 2
    )
    unit_prices.append(price)

    # Quantité (généralement 1 ou 2 dans le luxe)
    qty = random.choices([1, 2, 3], weights=[85, 12, 3], k=1)[0]
    quantities.append(qty)

    # Boutique associée
    store_names.append(random.choice(stores))

df_transactions = pd.DataFrame(
    {
        "transaction_id": transaction_ids,
        "customer_id": sampled_customers,
        "transaction_date": tx_dates,
        "category": categories,
        "quantity": quantities,
        "unit_price": unit_prices,
        "total_amount": np.array(quantities) * np.array(unit_prices),
        "store_name": store_names,
    }
)

# Trier par date de transaction
df_transactions = df_transactions.sort_values(
    by="transaction_date"
).reset_index(drop=True)

# Sauvegarde des transactions
df_transactions.to_csv("data/transactions.csv", index=False)
print(
    f"-> {len(df_transactions)} transactions générées et sauvegardées dans data/transactions.csv"
)
print("\nGénération des données terminée avec succès !")