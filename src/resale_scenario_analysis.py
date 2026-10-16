import sqlite3
import csv
from pathlib import Path

DB = "resale_analysis.db"
OUTPUT = Path("outputs/resale_scenarios.csv")

# Illustrative assumptions, not verified market costs
GBP_TO_JPY = 200
SHIPPING_JPY = 1500
OTHER_COST_JPY = 500
SELLING_FEE_RATE = 0.12

conn = sqlite3.connect(DB)

query = """
SELECT market, AVG(listing_price)
FROM market_observations
WHERE product_id = 'V11'
  AND listing_status = 'sold'
  AND price_type = 'sold_displayed_price'
  AND observation_id IN (
    'CAND001', 'CAND002',
    'JPNEW001', 'JPNEW002',
    'UKSOLD001', 'UKSOLD002'
)
GROUP BY market
"""

prices = dict(conn.execute(query).fetchall())
conn.close()

purchase_jpy = prices["JP"]
uk_reference_gbp = prices["UK"]

scenarios = [
    ("Low", 0.80),
    ("Base", 1.00),
    ("High", 1.20),
]

results = []

for name, multiplier in scenarios:
    sale_gbp = uk_reference_gbp * multiplier
    gross_revenue_jpy = sale_gbp * GBP_TO_JPY
    selling_fee_jpy = gross_revenue_jpy * SELLING_FEE_RATE

    total_cost_jpy = (
        purchase_jpy
        + SHIPPING_JPY
        + OTHER_COST_JPY
        + selling_fee_jpy
    )

    profit_jpy = gross_revenue_jpy - total_cost_jpy

    margin_pct = (
        profit_jpy / gross_revenue_jpy * 100
        if gross_revenue_jpy else 0
    )

    breakeven_gbp = (
        purchase_jpy + SHIPPING_JPY + OTHER_COST_JPY
    ) / (GBP_TO_JPY * (1 - SELLING_FEE_RATE))

    results.append({
        "scenario": name,
        "sale_price_gbp": round(sale_gbp, 2),
        "purchase_cost_jpy": round(purchase_jpy),
        "gross_revenue_jpy": round(gross_revenue_jpy),
        "total_cost_jpy": round(total_cost_jpy),
        "profit_jpy": round(profit_jpy),
        "margin_pct": round(margin_pct, 2),
        "breakeven_price_gbp": round(breakeven_gbp, 2),
    })

OUTPUT.parent.mkdir(exist_ok=True)

with open(OUTPUT, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("JAPAN TO UK RESALE SCENARIO ANALYSIS")
print("JP reference:", round(purchase_jpy), "JPY")
print("UK reference:", round(uk_reference_gbp, 2), "GBP")
print("FX assumption:", GBP_TO_JPY, "JPY/GBP")
print()

for row in results:
    print(
        row["scenario"],
        "| Sale: GBP", row["sale_price_gbp"],
        "| Profit: JPY", row["profit_jpy"],
        "| Margin:", str(row["margin_pct"]) + "%",
        "| Break-even: GBP", row["breakeven_price_gbp"]
    )

print()
print("Saved:", OUTPUT)
