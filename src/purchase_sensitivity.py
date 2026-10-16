
import csv
import matplotlib.pyplot as plt

# Illustrative assumptions (not verified costs)
sale_gbp = 28.12
fx = 200
shipping_jpy = 1500
other_jpy = 500
fee_rate = 0.12

purchase_prices = list(range(1000, 7001, 500))
net_revenue = sale_gbp * fx * (1 - fee_rate)

profits = [
    net_revenue - price - shipping_jpy - other_jpy
    for price in purchase_prices
]

breakeven_purchase = net_revenue - shipping_jpy - other_jpy

with open("outputs/purchase_sensitivity.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["purchase_price_jpy", "profit_jpy"])
    writer.writerows(zip(purchase_prices, profits))

fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(purchase_prices, profits, marker="o")
ax.axhline(0, color="black", linewidth=1)
ax.axvline(
    breakeven_purchase,
    color="red",
    linestyle="--",
    label=f"Break-even purchase: JPY {breakeven_purchase:,.0f}"
)

ax.set_title("Purchase Price Sensitivity: Japan-to-UK Resale")
ax.set_xlabel("Purchase Price in Japan (JPY)")
ax.set_ylabel("Estimated Profit per Item (JPY)")
ax.grid(alpha=0.25)
ax.legend()

fig.tight_layout()
fig.savefig("outputs/purchase_sensitivity.png", dpi=200)

print("Break-even purchase price:", round(breakeven_purchase), "JPY")
print("Saved: outputs/purchase_sensitivity.png")

plt.show()
