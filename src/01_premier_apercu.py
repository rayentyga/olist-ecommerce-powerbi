"""
Projet 1 - Olist | Jour 1 : premier aperçu des 9 fichiers CSV.
A lancer depuis la racine du dépôt :  python src/01_premier_apercu.py
Les CSV doivent être dans data/raw/
"""
from pathlib import Path
import pandas as pd

RAW = Path("data/raw")
fichiers = sorted(RAW.glob("*.csv"))
if not fichiers:
    raise SystemExit("Aucun CSV dans data/raw/ : décompresse l'archive Kaggle dans ce dossier.")

tables = {f.stem.replace("olist_", "").replace("_dataset", ""): pd.read_csv(f) for f in fichiers}

print(f"{len(tables)} tables chargées\n")
resume = []
for nom, df in tables.items():
    resume.append({
        "table": nom,
        "lignes": len(df),
        "colonnes": df.shape[1],
        "doublons": int(df.duplicated().sum()),
        "cellules_vides_%": round(df.isna().mean().mean() * 100, 2),
    })
print(pd.DataFrame(resume).to_string(index=False), "\n")

# Colonnes avec des valeurs manquantes, table par table
for nom, df in tables.items():
    manquants = df.isna().sum()
    manquants = manquants[manquants > 0]
    if not manquants.empty:
        print(f"--- {nom} : valeurs manquantes")
        print(manquants.to_string(), "\n")

# Vérification des clés (doivent être uniques)
cles = {
    "orders": "order_id",
    "customers": "customer_id",
    "products": "product_id",
    "sellers": "seller_id",
}
for nom, cle in cles.items():
    if nom in tables:
        df = tables[nom]
        print(f"Clé {nom}.{cle} unique : {df[cle].is_unique}")

# Période couverte et statuts des commandes
orders = tables["orders"]
dates = pd.to_datetime(orders["order_purchase_timestamp"])
print(f"\nPériode : {dates.min():%Y-%m-%d} -> {dates.max():%Y-%m-%d}")
print("\nStatuts des commandes :")
print(orders["order_status"].value_counts().to_string())

# Clients : un même client (customer_unique_id) peut avoir plusieurs customer_id
cust = tables["customers"]
print(f"\ncustomer_id : {cust['customer_id'].nunique():,} | "
      f"customer_unique_id : {cust['customer_unique_id'].nunique():,}")
