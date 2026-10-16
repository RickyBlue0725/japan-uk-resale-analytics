
import sqlite3
import csv
from pathlib import Path
import matplotlib.pyplot as plt

DB_PATH = "resale_analysis.db"
OUTPUT_DIR = Path("outputs")

PRODUCT_IDS = ["C01", "P01", "V11"]
EXCHANGE_RATES = [180, 190, 200, 210]

SELLING_FEE_RATE = 0.10
SHIPPING_JPY = 2600
IMPORT_VAT_RATE = 0.20
CUSTOMS_DUTY_RATE = 0.00

OUTPUT_DIR.mkdir(exist_ok=True)


def get_sold_average(db, product_id, market):
    rows = db.execute("""
        SELECT listing_price, price_type, listing_status
        FROM market_observations
        WHERE product_id = ?
          AND UPPER(market) IN (?, ?)
    """, (
        product_id,
        "JAPAN" if market == "JP" else "UK",
        "JP" if market == "JP" else "UK"
    )).fetchall()

    prices = []

    for price, price_type, status in rows:
        if (
            price is not None
            and "sold" in (price_type or "").lower()
            and (status or "").lower() == "sold"
        ):
            prices.append(price)

    return sum(prices) / len(prices) if prices else None


def calculate_profit(buy_price, uk_price, rate):
    revenue = uk_price * rate
    fee = revenue * SELLING_FEE_RATE
    duty = buy_price * CUSTOMS_DUTY_RATE

    # Simplified non-recoverable import VAT scenario
    vat = (
        buy_price + SHIPPING_JPY + duty
    ) * IMPORT_VAT_RATE

    return revenue - fee - buy_price - SHIPPING_JPY - duty - vat


db = sqlite3.connect(DB_PATH)
results = []

for product_id in PRODUCT_IDS:
    product_row = db.execute(
        "SELECT product FROM products WHERE product_id = ?",
        (product_id,)
    ).fetchone()

    if product_row is None:
        continue

    name = product_row[0]
    jp_price = get_sold_average(db, product_id, "JP")
    uk_price = get_sold_average(db, product_id, "UK")

    if jp_price is None or uk_price is None:
        continue

    for rate in EXCHANGE_RATES:
        profit = calculate_profit(jp_price, uk_price, rate)

        results.append({
            "product_id": product_id,
            "product": name,
            "exchange_rate": rate,
            "profit_jpy": round(profit, 2)
        })

db.close()

csv_path = OUTPUT_DIR / "automated_risk_analysis.csv"

with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "product_id",
            "product",
            "exchange_rate",
            "profit_jpy"
        ]
    )
    writer.writeheader()
    writer.writerows(results)

fig, ax = plt.subplots(figsize=(10, 6))

for product_id in PRODUCT_IDS:
    product_rows = [
        row for row in results
        if row["product_id"] == product_id
    ]

    if not product_rows:
        continue

    ax.plot(
        [r["exchange_rate"] for r in product_rows],
        [r["profit_jpy"] for r in product_rows],
        marker="o",
        label=product_rows[0]["product"]
    )

ax.axhline(0, linestyle="--")
ax.set_xlabel("GBP/JPY Exchange Rate")
ax.set_ylabel("Estimated Profit (JPY)")
ax.set_title("Automated Japan-to-UK Resale Risk Analysis")
ax.set_xticks(EXCHANGE_RATES)
ax.legend()
ax.grid(True, alpha=0.3)

fig.tight_layout()

chart_path = OUTPUT_DIR / "automated_risk_analysis.png"
fig.savefig(chart_path, dpi=200, bbox_inches="tight")
plt.close(fig)

print("=== Automated Risk Analysis ===")
print(f"Scenarios calculated: {len(results)}")
print(f"CSV saved: {csv_path}")
print(f"Chart saved: {chart_path}")
print("All values use illustrative cost assumptions.")
