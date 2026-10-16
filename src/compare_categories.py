
from pathlib import Path
import csv
import matplotlib.pyplot as plt

# Previous Base scenario results (JPY per item)
# These are provisional and use different assumptions.
results = [
    {"category": "iPhone 13", "profit_jpy": -13616},
    {"category": "Pokemon Cards", "profit_jpy": -5177},
    {"category": "Ralph Lauren", "profit_jpy": -3072},
    {"category": "Canon Lens", "profit_jpy": -2357},
]

# Sort from highest to lowest estimated profit
results.sort(key=lambda x: x["profit_jpy"], reverse=True)

output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

# Save CSV
csv_path = output_dir / "category_profit_comparison.csv"

with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f, fieldnames=["category", "profit_jpy"]
    )
    writer.writeheader()
    writer.writerows(results)

# Create chart
categories = [r["category"] for r in results]
profits = [r["profit_jpy"] for r in results]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(categories, profits)

ax.axvline(0, linewidth=1)
ax.set_xlabel("Estimated Profit per Item (JPY)")
ax.set_title("Japan-to-UK Resale: Profitability Comparison")
ax.invert_yaxis()

for bar, profit in zip(bars, profits):
    x = profit - 200
    ax.text(
        x,
        bar.get_y() + bar.get_height() / 2,
        f"JPY {profit:,.0f}",
        ha="right",
        va="center"
    )

fig.tight_layout()

chart_path = output_dir / "category_profit_comparison.png"
fig.savefig(chart_path, dpi=200, bbox_inches="tight")
plt.close(fig)

print("=== Category Profitability Ranking ===")
for i, result in enumerate(results, 1):
    print(
        f"{i}. {result['category']}: "
        f"JPY {result['profit_jpy']:,.0f}"
    )

print(f"\nCSV saved: {csv_path}")
print(f"Chart saved: {chart_path}")
print("\nNote: Results are provisional and not fully comparable.")
