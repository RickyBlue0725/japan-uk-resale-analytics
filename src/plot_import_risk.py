
from pathlib import Path
import matplotlib.pyplot as plt

exchange_rates = [180, 190, 200, 210]

profits = {
    "Canon Lens": [-6286, -5710, -5134, -4557],
    "Pokemon Cards": [-14589, -13193, -11797, -10401],
    "Ralph Lauren": [-5789, -5536, -5283, -5030],
}

output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

fig, ax = plt.subplots(figsize=(10, 6))

for product, values in profits.items():
    ax.plot(
        exchange_rates,
        values,
        marker="o",
        linewidth=2,
        label=product
    )

ax.axhline(0, linestyle="--", linewidth=1)
ax.set_title("Japan-to-UK Resale: FX Sensitivity Analysis")
ax.set_xlabel("GBP/JPY Exchange Rate")
ax.set_ylabel("Estimated Profit per Item (JPY)")
ax.set_xticks(exchange_rates)
ax.legend()
ax.grid(True, alpha=0.3)

fig.tight_layout()

path = output_dir / "import_fx_sensitivity.png"
fig.savefig(path, dpi=200, bbox_inches="tight")
plt.close(fig)

print(f"Chart saved: {path}")
