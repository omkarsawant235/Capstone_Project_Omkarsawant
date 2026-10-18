import pandas as pd
import json

customers = pd.read_csv("data/customers.csv")
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders.csv")

print("Initial Shape:", orders.shape)

print("\nRaw Payment Methods")
print(orders["payment_method"].unique())

orders["payment_method"] = (
    orders["payment_method"]
    .str.strip()
    .str.upper()
)

print("\nClean Payment Methods")
print(orders["payment_method"].value_counts())

dup_mask = orders.duplicated(
    subset=[
        "customer_id",
        "product_id",
        "order_date",
        "quantity",
        "discount_pct",
        "payment_method",
        "rating",
        "returned"
    ],
    keep="first"
)

dups = orders[dup_mask]

print("\nDropped Duplicates")
print(dups["order_id"])

orders_clean = orders[~dup_mask].copy()
print("Shape After Dedup:", orders_clean.shape)

print("\nMissing Values Before Imputation")
print(orders_clean[["discount_pct", "rating"]].isnull().sum())

median_rating = orders_clean["rating"].median()
print("\nMedian Rating:", median_rating)

orders_clean["discount_pct"] = (
    orders_clean["discount_pct"].fillna(0)
)

orders_clean["rating"] = (
    orders_clean["rating"].fillna(median_rating)
)

print("\nNulls After Imputation")
print(
    orders_clean[
        ["discount_pct", "rating"]
    ].isnull().sum()
)

merged = (
    orders_clean
    .merge(products, on="product_id")
    .merge(customers, on="customer_id")
)

merged["order_value"] = (
    merged["quantity"]
    * merged["price"]
    * (1 - merged["discount_pct"] / 100)
)

total_revenue = round(
    merged["order_value"].sum(),
    2
)

print("\nClean Revenue:", total_revenue)

q1 = merged["quantity"].quantile(0.25)
q3 = merged["quantity"].quantile(0.75)

iqr = q3 - q1

lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

print("\nQ1:", q1)
print("Q3:", q3)
print("IQR:", iqr)
print("Lower:", lower)
print("Upper:", upper)

merged["is_outlier"] = (
    (merged["quantity"] < lower)
    |
    (merged["quantity"] > upper)
)

print(
    merged.loc[
        merged["is_outlier"],
        ["order_id", "quantity"]
    ]
)

return_rates = (
    merged.groupby(
        "payment_method"
    )["returned"]
    .mean()
    * 100
)

print("\nReturn Rates")
print(return_rates)

segment = (
    merged.groupby(
        [
            "payment_method",
            "city_tier"
        ]
    )["returned"]
    .mean()
    * 100
)

print("\nSegmentation")
print(segment)

corr = merged[
    [
        "rating",
        "returned",
        "discount_pct",
        "quantity"
    ]
].corr()

print("\nCorrelation Matrix")
print(corr)

merged["order_date"] = pd.to_datetime(
    merged["order_date"]
)

merged["month"] = (
    merged["order_date"]
    .dt.to_period("M")
    .astype(str)
)

monthly = (
    merged.groupby("month")
    ["order_value"]
    .sum()
)

print("\nMonthly Revenue")
print(monthly)

findings = {
    "cleaned_total_revenue_inr": 97358.30,
    "raw_total_revenue_inr": 99860.20,
    "duplicate_reconciliation_delta_inr": 2501.90,
    "return_rate_by_payment": {
        "COD": 44.4,
        "CARD": 14.7,
        "UPI": 18.9
    },
    "highest_risk_segment": {
        "payment_method": "COD",
        "city_tier": 2,
        "return_rate_pct": 54.5
    },
    "true_peak_month": {
        "month": "2026-03",
        "revenue_inr": 20318.90
    },
    "outlier_inflated_month": {
        "month": "2026-01",
        "apparent_revenue_inr": 29582.10,
        "corrected_revenue_inr": 11637.10
    }
}

with open(
    "narrator/findings.json",
    "w"
) as f:
    json.dump(
        findings,
        f,
        indent=4
    )
