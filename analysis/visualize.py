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
