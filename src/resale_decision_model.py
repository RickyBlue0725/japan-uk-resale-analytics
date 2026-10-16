
import sqlite3

DB_PATH = "resale_analysis.db"

# Provisional assumptions — adjust after checking real costs
GBP_TO_JPY = 200
SELLING_FEE_RATE = 0.10
SHIPPING_AND_OTHER_JPY = 2600
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

    sold_prices = []
    for price, price_type, status in rows:
        price_type = (price_type or "").lower()
        status = (status or "").lower()

        if "sold" in price_type and status == "sold":
            sold_prices.append(price)

    if not sold_prices:
        return None

    return sum(sold_prices) / len(sold_prices)

def classify_profit(profit):
    if profit >= TARGET_PROFIT_JPY:
        return "BUY"
    elif profit >= 0:
        return "REVIEW"
    return "SKIP"

db = sqlite3.connect(DB_PATH)

print("=== Japan-to-UK Resale Decision Model ===")

for product_id in PRODUCT_IDS:
    name_row = db.execute(
        "SELECT product FROM products WHERE product_id = ?",
        (product_id,)
    ).fetchone()

    name = name_row[0] if name_row else product_id

    japan_price = get_sold_average(db, product_id, "JP")
    uk_price = get_sold_average(db, product_id, "UK")

    if japan_price is None or uk_price is None:
        print(f"\n{name}: insufficient sold data")
        continue

    revenue_jpy = uk_price * GBP_TO_JPY
    fee_jpy = revenue_jpy * SELLING_FEE_RATE

    profit_jpy = (
        revenue_jpy
        - fee_jpy
        - SHIPPING_AND_OTHER_JPY
        - japan_price
    )

    max_buy_price = (
        revenue_jpy
        - fee_jpy
        - SHIPPING_AND_OTHER_JPY
        - TARGET_PROFIT_JPY
    )

    print(f"\n{name}")
    print(f"Japan average: JPY {japan_price:,.0f}")
    print(f"UK sold average: GBP {uk_price:,.2f}")
    print(f"Estimated profit: JPY {profit_jpy:,.0f}")
    print(f"Max buy price for target profit: JPY {max_buy_price:,.0f}")
    print(f"Decision: {classify_profit(profit_jpy)}")

db.close()

print("\nIMPORTANT: Import VAT, customs duties, returns,")
print("and other unverified costs are excluded.")
print("BUY is a preliminary screening result, not approval to purchase.")
