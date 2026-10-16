
import csv
from pathlib import Path

import matplotlib.pyplot as plt

# Canon EF 50mm f/1.8 STM
BUY_PRICES = [5000, 7000, 9000]
SELL_PRICES_GBP = [50, 65, 80]
EXCHANGE_RATES = [180, 200, 210]

# Illustrative assumptions, not verified actual costs
SELLING_FEE_RATE = 0.10
SHIPPING_JPY = 2600
IMPORT_VAT_RATE = 0.20
CUSTOMS_DUTY_RATE = 0.00
TARGET_PROFIT_JPY = 2000

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def calculate_profit(buy_price, sell_price_gbp, fx):
    revenue = sell_price_gbp * fx
    fee = revenue * SELLING_FEE_RATE
    duty = buy_price * CUSTOMS_DUTY_RATE
    vat = (buy_price + SHIPPING_JPY + duty) * IMPORT_VAT_RATE

    return revenue - fee - buy_price - SHIPPING_JPY - duty - vat


def decision(profit):
    if profit >= TARGET_PROFIT_JPY:
        return "BUY"
    if profit >= 0:
        return "REVIEW"
    return "SKIP"


results = []

for buy_price in BUY_PRICES:
    for sell_price in SELL_PRICES_GBP:
        for fx in EXCHANGE_RATES:
            profit = calculate_profit(buy_price, sell_price, fx)

            results.append({
                "buy_price_jpy": buy_price,
                "sell_price_gbp": sell_price,
                "gbp_jpy": fx,
                "profit_jpy": round(profit, 2),
                "decision": decision(profit),
            })

csv_path = OUTPUT_DIR / "canon_scenario_analysis.csv"

with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f, fieldnames=list(results[0].keys())
    )
    writer.writeheader()
    writer.writerows(results)

# Heatmap at GBP/JPY = 200
fx = 200
matrix = [
    [calculate_profit(buy, sell, fx) for sell in SELL_PRICES_GBP]
    for buy in BUY_PRICES
]

fig, ax = plt.subplots(figsize=(8, 5))
heatmap = ax.imshow(matrix, cmap="RdYlGn", aspect="auto")

ax.set_xticks(range(len(SELL_PRICES_GBP)))
ax.set_xticklabels([f"GBP {p}" for p in SELL_PRICES_GBP])
ax.set_yticks(range(len(BUY_PRICES)))
ax.set_yticklabels([f"JPY {p:,}" for p in BUY_PRICES])

ax.set_xlabel("UK Selling Price")
ax.set_ylabel("Japan Purchase Price")
ax.set_title("Canon Lens Profit Scenarios (GBP/JPY = 200)")

for i, row in enumerate(matrix):
    for j, profit in enumerate(row):
        ax.text(
            j, i,
            f"JPY {profit:,.0f}\n{decision(profit)}",
            ha="center", va="center",
            fontsize=9
        )

fig.colorbar(heatmap, ax=ax, label="Estimated Profit (JPY)")
fig.tight_layout()

chart_path = OUTPUT_DIR / "canon_scenario_heatmap.png"
fig.savefig(chart_path, dpi=200, bbox_inches="tight")
plt.close(fig)

print("=== Canon Scenario Analysis ===")
print(f"Scenarios calculated: {len(results)}")

for status in ["BUY", "REVIEW", "SKIP"]:
    count = sum(r["decision"] == status for r in results)
    print(f"{status}: {count}")

print(f"CSV saved: {csv_path}")
print(f"Heatmap saved: {chart_path}")
print("Note: Illustrative VAT, fees and shipping assumptions.")

