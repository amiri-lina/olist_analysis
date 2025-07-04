import pandas as pd
import os

#load data
data_dir = "data" 

orders = pd.read_csv(os.path.join(data_dir, "olist_orders_dataset.csv"))
items = pd.read_csv(os.path.join(data_dir, "olist_order_items_dataset.csv"))
payments = pd.read_csv(os.path.join(data_dir, "olist_order_payments_dataset.csv"))
products = pd.read_csv(os.path.join(data_dir, "olist_products_dataset.csv"))
customers = pd.read_csv(os.path.join(data_dir, "olist_customers_dataset.csv"))

print("Orders:", orders.shape)
print("Order items:", items.shape)
print("Payments:", payments.shape)

# 🧼 Étape 2 : Convertir les colonnes date
orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
orders["order_approved_at"] = pd.to_datetime(orders["order_approved_at"])

# 🧼 Étape 3 : Fusionner les tables principales
df = orders.merge(items, on="order_id", how="left")
df = df.merge(payments, on="order_id", how="left")
df = df.merge(customers, on="customer_id", how="left")
df = df.merge(products, on="product_id", how="left")

# 🔎 Étape 4 : Nettoyage
df.dropna(subset=["order_purchase_timestamp"], inplace=True)  # supprimer lignes invalides

# ➕ Étape 5 : Créer colonnes utiles
df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M")
df["order_day"] = df["order_purchase_timestamp"].dt.date

# 🧾 Étape 6 : Exporter un CSV propre
df.to_csv("data/olist_cleaned.csv", index=False)

print("Data is cleaned and saved in olist_cleaned.csv")
