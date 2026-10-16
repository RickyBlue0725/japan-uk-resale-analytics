import statistics

# Sold prices collected from Mercari Japan
japan_prices = [
    11800, 11000, 11890, 9000, 12500,
    10000, 10000, 8900, 16000, 12500, 10500
]

# Indicative eBay UK sold-listing prices
uk_prices = [
    70.00, 62.58, 60.52, 59.49, 78.08,
    48.57, 41.92, 89.00, 62.58, 62.58,
    62.58, 72.92, 69.43, 53.28, 31.58,
    67.74, 67.75, 79.00, 69.43, 69.43,
    62.58, 79.00, 78.08, 77.39, 69.99,
    67.75, 63.05, 52.25, 60.54, 47.00,
    72.92, 60.46
]

fx_rate = 200
selling_fee_rate = 0.10
shipping_and_other_jpy = 2600

jp_avg = statistics.mean(japan_prices)
uk_avg = statistics.mean(uk_prices)

revenue_jpy = uk_avg * fx_rate
selling_fee_jpy = revenue_jpy * selling_fee_rate

break_even_purchase = (
    revenue_jpy - selling_fee_jpy - shipping_and_other_jpy
)

profit_jpy = break_even_purchase - jp_avg

print("=== Canon EF 50mm f/1.8 STM ===")
print(f"Japan samples: {len(japan_prices)}")
print(f"Japan average: JPY {jp_avg:,.0f}")
print(f"UK samples: {len(uk_prices)}")
print(f"UK average: GBP {uk_avg:.2f}")
print(f"Estimated profit: JPY {profit_jpy:,.0f}")
print(f"Break-even purchase price: JPY {break_even_purchase:,.0f}")

print("\nPurchase price scenarios:")
for purchase_price in [5000, 7000, 9000, 11000]:
    profit = break_even_purchase - purchase_price
    print(f"JPY {purchase_price:,} -> Profit JPY {profit:,.0f}")

print("\nNOTE: Indicative sold-listing prices, not verified final transaction prices.")
print("VAT, import duties, returns, and other costs are not fully modeled.")