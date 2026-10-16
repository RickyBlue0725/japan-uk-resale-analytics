import csv
from pathlib import Path
import matplotlib.pyplot as plt

with open("data/market_data.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

items = [
    r for r in rows
    if r["platform"] == "Vinted UK"
    and r["product_id"] == "V11"
    and r["price_type"] == "asking"
]

labels = [
    r["product"].replace("Polo Ralph Lauren Quarter Zip ", "")
    for r in items
]
prices = [float(r["listing_price"]) for r in items]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(labels, prices)

ax.set_title("Polo Ralph Lauren Quarter-Zip - Vinted UK")
ax.set_ylabel("Asking Price (GBP)")
ax.set_xlabel("Listing Variation")

for bar, price in zip(bars, prices):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"£{price:.2f}",
        ha="center"
    )

ax.set_ylim(0, max(prices) * 1.2)
plt.xticks(rotation=15, ha="right")
plt.tight_layout()

Path("outputs").mkdir(exist_ok=True)
plt.savefig("outputs/vinted_price_comparison.png", dpi=200)

print("Chart saved: outputs/vinted_price_comparison.png")
print(f"Average asking price: £{sum(prices)/len(prices):.2f}")
