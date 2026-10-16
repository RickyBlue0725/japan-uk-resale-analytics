import csv
import matplotlib.pyplot as plt

with open("outputs/resale_scenarios.csv", newline="") as f:
    rows = list(csv.DictReader(f))

names = [r["scenario"] for r in rows]
profits = [float(r["profit_jpy"]) for r in rows]

fig, ax = plt.subplots(figsize=(9, 5))

bars = ax.bar(names, profits)

ax.axhline(0, color="black", linewidth=1)
ax.set_title("Japan-to-UK Resale: Profitability Scenarios")
ax.set_ylabel("Estimated Profit per Item (JPY)")
ax.set_xlabel("Scenario")

for bar, profit in zip(bars, profits):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        profit - 100,
        f"JPY {profit:,.0f}",
        ha="center",
        va="top"
    )

ax.set_ylim(min(profits) * 1.25, 500)
ax.grid(axis="y", alpha=0.2)
fig.tight_layout()

output = "outputs/resale_profit_scenarios.png"
fig.savefig(output, dpi=200)
print("Saved:", output)

plt.show()
