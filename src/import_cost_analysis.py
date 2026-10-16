
import sqlite3

DB_PATH = "resale_analysis.db"

# Illustrative assumptions, NOT verified UK tax rates
GBP_TO_JPY = 200
SELLING_FEE_RATE = 0.10
SHIPPING_JPY = 2600
IMPORT_VAT_RATE = 0.20
CUSTOMS_DUTY_RATE = 0.00
TARGET_PROFIT_JPY = 2000

PRODUCT_IDS = ["C01", "P01", "V11"]


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
        price_type = (price_type or "").lower()
        status = (status or "").lower()

        if "sold" in price_type and status == "sold":
            prices.append(price)

    return sum(prices) / len(prices) if prices else None


def calculate_profit(buy_price, uk_price, exchange_rate):
    revenue = uk_price * exchange_rate
    selling_fee = revenue * SELLING_FEE_RATE

    # Simplified import-cost scenario
    duty = buy_price * CUSTOMS_DUTY_RATE
    vat = (buy_price + SHIPPING_JPY + duty) * IMPORT_VAT_RATE

    profit = (
        revenue
        - selling_fee
        - buy_price
        - SHIPPING_JPY
        - duty
        - vat
    )

    return profit


db = sqlite3.connect(DB_PATH)

print("=== UK Import Cost & Risk Analysis ===")

for product_id in PRODUCT_IDS:
    name = db.execute(
        "SELECT product FROM products WHERE product_id = ?",
        (product_id,)
    ).fetchone()[0]

    jp_price = get_sold_average(db, product_id, "JP")
    uk_price = get_sold_average(db, product_id, "UK")

    if jp_price is None or uk_price is None:
        print(f"\n{name}: insufficient data")
        continue

    print(f"\n{name}")

    for exchange_rate in [180, 190, 200, 210]:
        profit = calculate_profit(
            jp_price, uk_price, exchange_rate
        )

        if profit >= TARGET_PROFIT_JPY:
            decision = "BUY"
        elif profit >= 0:
            decision = "REVIEW"
        else:
            decision = "SKIP"

        print(
            f"GBP/JPY {exchange_rate}: "
            f"Profit JPY {profit:,.0f} | {decision}"
        )

db.close()

print("\nAssumptions:")
print("VAT: 20% illustrative")
print("Duty: 0% illustrative")
print("Selling fee: 10%")
print("Shipping: JPY 2,600")
print("Import valuation and actual taxes must be verified.")
