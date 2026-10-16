
import sqlite3

# Assumptions (change these to test different scenarios)
JPY_PER_GBP = 200
INTERNATIONAL_SHIPPING_JPY = 2500
UK_DOMESTIC_SHIPPING_GBP = 5
SELLING_FEE_RATE = 0.10
OTHER_COSTS_JPY = 1000

conn = sqlite3.connect("resale_analysis.db")

query = """
SELECT market, AVG(listing_price)
FROM market_observations
WHERE observation_id IN (
    'JPIPH001', 'JPIPH002', 'JPIPH003',
    'UKIPH001', 'UKIPH003'
)
GROUP BY market
"""

prices = dict(conn.execute(query).fetchall())
conn.close()

jp_price = prices["Japan"]
uk_price = prices["UK"]

print("IPHONE 13: JAPAN TO UK RESALE ANALYSIS")
print(f"Japan reference price: JPY {jp_price:,.0f}")
print(f"UK reference price: GBP {uk_price:.2f}")
print(f"Exchange rate assumption: GBP 1 = JPY {JPY_PER_GBP}")
print()

for name, multiplier in [
    ("Low", 0.8),
    ("Base", 1.0),
    ("High", 1.2),
]:
    sale_gbp = uk_price * multiplier
    revenue_jpy = sale_gbp * JPY_PER_GBP
    selling_fee_jpy = revenue_jpy * SELLING_FEE_RATE
    domestic_shipping_jpy = UK_DOMESTIC_SHIPPING_GBP * JPY_PER_GBP

    profit_jpy = (
        revenue_jpy
        - selling_fee_jpy
        - jp_price
        - INTERNATIONAL_SHIPPING_JPY
        - domestic_shipping_jpy
        - OTHER_COSTS_JPY
    )

    print(
        f"{name} | "
        f"Sale: GBP {sale_gbp:.2f} | "
        f"Estimated profit: JPY {profit_jpy:,.0f}"
    )

print()
print("NOTE: Illustrative cost assumptions only.")
print("UK battery health is unverified.")
print("Sold-listing displayed prices may differ from final transaction prices.")
print("Import taxes, VAT and other applicable costs are not fully modeled.")
