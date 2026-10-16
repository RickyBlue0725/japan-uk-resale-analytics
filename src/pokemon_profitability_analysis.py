import sqlite3

# Assumptions (illustrative, not verified costs)
GBP_TO_JPY = 200
INTERNATIONAL_SHIPPING_JPY = 1500
UK_DOMESTIC_SHIPPING_GBP = 3
SELLING_FEE_RATE = 0.10
OTHER_COSTS_JPY = 500

conn = sqlite3.connect("resale_analysis.db")

query = """
SELECT market, AVG(listing_price)
FROM market_observations
WHERE product_id = 'P01'
  AND listing_status = 'Sold'
GROUP BY market
"""

prices = dict(conn.execute(query).fetchall())
conn.close()

japan_price = prices["Japan"]
uk_price = prices["UK"]

scenarios = {
    "Low": 0.8,
    "Base": 1.0,
    "High": 1.2,
}

print("POKEMON: JAPAN TO UK RESALE ANALYSIS")
print(f"Japan reference price: JPY {japan_price:,.0f}")
print(f"UK reference price: GBP {uk_price:,.2f}")
print(f"Exchange rate assumption: GBP 1 = JPY {GBP_TO_JPY}")
print()

for name, multiplier in scenarios.items():
    sale_gbp = uk_price * multiplier
    revenue_jpy = sale_gbp * GBP_TO_JPY
    selling_fee_jpy = revenue_jpy * SELLING_FEE_RATE

    total_cost_jpy = (
        japan_price
        + INTERNATIONAL_SHIPPING_JPY
        + UK_DOMESTIC_SHIPPING_GBP * GBP_TO_JPY
        + selling_fee_jpy
        + OTHER_COSTS_JPY
    )

    profit_jpy = revenue_jpy - total_cost_jpy

    print(
        f"{name} | Sale: GBP {sale_gbp:,.2f} "
        f"| Estimated profit: JPY {profit_jpy:,.0f}"
    )

print()
print("NOTE: Illustrative cost assumptions only.")
print("UK observations are unverified candidates.")
print("Displayed sold-listing prices may differ from final transaction prices.")
print("Import duties, VAT, returns and other applicable costs are not fully modeled.")