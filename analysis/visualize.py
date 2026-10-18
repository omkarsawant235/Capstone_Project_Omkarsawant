import pandas as pd
import matplotlib.pyplot as plt

customers = pd.read_csv("data/customers.csv")
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders.csv")

orders["payment_method"] = (
    orders["payment_method"]
    .str.upper()
)

returns = (
    orders.groupby(
        "payment_method"
    )["returned"]
    .mean()
    * 100
).sort_values(
    ascending=False
)

plt.figure(figsize=(8,5))

returns.plot(
    kind="bar",
    color="orange"
)

plt.title(
    "COD Returns at 44.4% - 3x Card"
)

plt.ylabel("Return Rate %")

for i, v in enumerate(returns):
    plt.text(
        i,
        v+1,
        f"{v:.1f}%"
    )

plt.tight_layout()

plt.savefig(
    "visualizations/return_rate_by_payment.png"
)

plt.close()


import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Create output folder
Path("visualizations").mkdir(exist_ok=True)

# =========================
# LOAD DATA
# =========================

customers = pd.read_csv("data/customers.csv")
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders.csv")

# =========================
# CLEANING (same as EDA)
# =========================

orders["payment_method"] = (
    orders["payment_method"]
    .str.strip()
    .str.upper()
)

duplicates = orders.duplicated(
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

orders = orders[~duplicates].copy()

orders["discount_pct"] = (
    orders["discount_pct"].fillna(0)
)

orders["rating"] = (
    orders["rating"]
    .fillna(
        orders["rating"].median()
    )
)

# =========================
# MERGE DATA
# =========================

merged = (
    orders
    .merge(products, on="product_id")
    .merge(customers, on="customer_id")
)

merged["order_value"] = (
    merged["quantity"]
    * merged["price"]
    * (1 - merged["discount_pct"] / 100)
)

# =====================================================
# CHART 1
# RETURN RATE BY PAYMENT METHOD
# =====================================================

payment_returns = (
    merged
    .groupby("payment_method")["returned"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

plt.figure(figsize=(8,5))

bars = plt.bar(
    payment_returns.index,
    payment_returns.values,
    color=["tomato","steelblue","seagreen"]
)

for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 1,
        f"{bar.get_height():.1f}%",
        ha="center",
        fontsize=10,
        fontweight="bold"
    )

plt.title("COD Returns at 44.4% — 3x Card")
plt.xlabel("Payment Method")
plt.ylabel("Return Rate (%)")
plt.tight_layout()

plt.savefig(
    "visualizations/return_rate_by_payment.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# =====================================================
# CHART 2
# OUTLIER-CORRECTED MONTHLY REVENUE TREND
# =====================================================

q1 = merged["quantity"].quantile(0.25)
q3 = merged["quantity"].quantile(0.75)

iqr = q3 - q1

lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

corrected = merged[
    (merged["quantity"] >= lower)
    &
    (merged["quantity"] <= upper)
].copy()

corrected["order_date"] = pd.to_datetime(
    corrected["order_date"]
)

corrected["month"] = (
    corrected["order_date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_revenue = (
    corrected
    .groupby("month")["order_value"]
    .sum()
)

peak_month = monthly_revenue.idxmax()

plt.figure(figsize=(10,5))

plt.plot(
    monthly_revenue.index,
    monthly_revenue.values,
    marker="o",
    linewidth=2,
    color="darkorange"
)

for x, y in zip(
    monthly_revenue.index,
    monthly_revenue.values
):
    plt.text(
        x,
        y + 300,
        f"{y:.0f}",
        ha="center"
    )

plt.title(
    f"Outlier-Corrected Monthly Revenue Trend (Peak: {peak_month})"
)

plt.xlabel("Month")
plt.ylabel("Revenue (INR)")
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "visualizations/monthly_revenue_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("✅ Saved: visualizations/return_rate_by_payment.png")
print("✅ Saved: visualizations/monthly_revenue_trend.png")
