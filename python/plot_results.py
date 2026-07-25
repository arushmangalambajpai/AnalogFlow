from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

CSV_DIR = ROOT / "results" / "csv"

PLOT_DIR = ROOT / "results" / "plots"

PARAMETER = "W1"

OUTPUT_NODE = "V(n007)"

PLOT_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------

csv_files = sorted(CSV_DIR.glob(f"{PARAMETER}_*.csv"))

if not csv_files:
    raise FileNotFoundError(f"No CSV files found in {CSV_DIR}")

plt.figure(figsize=(10, 6))

for csv_file in csv_files:

    df = pd.read_csv(csv_file)

    if "time" not in df.columns:
        raise ValueError(f"'time' column missing in {csv_file.name}")

    if OUTPUT_NODE not in df.columns:
        raise ValueError(
            f"'{OUTPUT_NODE}' column missing in {csv_file.name}"
        )

    label = csv_file.stem.replace(f"{PARAMETER}_", "")

    plt.plot(
        df["time"],
        df[OUTPUT_NODE],
        label=label,
        linewidth=2,
    )

plt.title(f"{OUTPUT_NODE} for {PARAMETER} Sweep")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.grid(True)
plt.legend(title=PARAMETER)

output_file = PLOT_DIR / f"{PARAMETER}_sweep.png"

plt.tight_layout()
plt.savefig(output_file, dpi=300)

print()
print("=" * 60)
print("Plot saved successfully")
print("=" * 60)
print(output_file)

plt.show()