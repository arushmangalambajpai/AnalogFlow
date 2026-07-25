from pathlib import Path
import numpy as np
import pandas as pd

# ----------------------------------------------------------
# Configuration
# ----------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

CSV = ROOT / "results" / "csv" / "W1_20k.csv"

# ----------------------------------------------------------

df = pd.read_csv(CSV)

print("=" * 80)
print("ANALOGFLOW CIRCUIT DIAGNOSTIC")
print("=" * 80)

print("\nColumns found:\n")

for c in df.columns:
    print("   ", c)

print()

# ----------------------------------------------------------
# Basic statistics
# ----------------------------------------------------------

print("=" * 80)
print("NODE STATISTICS")
print("=" * 80)

for col in df.columns:

    if col == "time":
        continue

    x = df[col]

    print(f"\n{col}")

    print("-" * 60)

    print(f"Minimum      : {x.min(): .5f} V")
    print(f"Maximum      : {x.max(): .5f} V")
    print(f"Mean         : {x.mean(): .5f} V")
    print(f"Std Dev      : {x.std(): .5f} V")
    print(f"Peak-Peak    : {(x.max()-x.min()): .5f} V")

# ----------------------------------------------------------
# Detect constant nodes
# ----------------------------------------------------------

print()
print("=" * 80)
print("CONSTANT NODE CHECK")
print("=" * 80)

for col in df.columns:

    if col == "time":
        continue

    x = df[col]

    if np.std(x) < 1e-6:
        print(f"{col:20} CONSTANT")

# ----------------------------------------------------------
# Detect rail saturation
# ----------------------------------------------------------

print()
print("=" * 80)
print("SATURATION CHECK")
print("=" * 80)

RAIL_HIGH = 5
RAIL_LOW = -5

TOL = 0.15

for col in df.columns:

    if col == "time":
        continue

    x = df[col]

    pct_high = np.mean(np.abs(x - RAIL_HIGH) < TOL) * 100
    pct_low = np.mean(np.abs(x - RAIL_LOW) < TOL) * 100

    if pct_high > 80:
        print(f"{col:20} HIGH RAIL ({pct_high:.1f}%)")

    if pct_low > 80:
        print(f"{col:20} LOW RAIL ({pct_low:.1f}%)")

# ----------------------------------------------------------
# Comparator analysis
# ----------------------------------------------------------

print()
print("=" * 80)
print("COMPARATOR ANALYSIS")
print("=" * 80)

try:

    comp = df["V(n007)"]
    ref = df["V(n010)"]

    diff = comp - ref

    print(f"Difference Min : {diff.min():.5f}")
    print(f"Difference Max : {diff.max():.5f}")

    crossings = np.sum(np.diff(np.sign(diff)) != 0)

    print(f"Zero Crossings : {crossings}")

    if crossings == 0:

        if diff.mean() > 0:
            print("\nLimiter is ALWAYS above threshold.")

        else:
            print("\nLimiter is ALWAYS below threshold.")

except KeyError:

    print("Could not locate comparator nodes.")

# ----------------------------------------------------------
# Correlation
# ----------------------------------------------------------

print()
print("=" * 80)
print("CORRELATION MATRIX")
print("=" * 80)

numeric = df.drop(columns=["time"])

corr = numeric.corr()

print(corr)

# ----------------------------------------------------------
# First few samples
# ----------------------------------------------------------

print()
print("=" * 80)
print("FIRST 20 SAMPLES")
print("=" * 80)

print(df.head(20))

# ----------------------------------------------------------
# Last samples
# ----------------------------------------------------------

print()
print("=" * 80)
print("LAST 20 SAMPLES")
print("=" * 80)

print(df.tail(20))

# ----------------------------------------------------------
# Output transition analysis
# ----------------------------------------------------------

print()
print("=" * 80)
print("OUTPUT TRANSITION ANALYSIS")
print("=" * 80)

vout = df["V(vout)"]

transition_indices = []

for i in range(1, len(vout)):

    if (vout.iloc[i-1] < 0 and vout.iloc[i] > 0) or \
       (vout.iloc[i-1] > 0 and vout.iloc[i] < 0):

        transition_indices.append(i)

print(f"Total output transitions : {len(transition_indices)}")

if len(transition_indices):

    print("\nTransition times:")

    for idx in transition_indices:
        print(f"{df['time'].iloc[idx]:.6f} s")

print()

print("=" * 80)
print("ACTIVATION vs THRESHOLD")
print("=" * 80)

print(df[["time", "V(n007)", "V(n010)", "V(vout)"]].head(40))
print()
print("=" * 80)
print("SWITCHING INSTANT")
print("=" * 80)

vout = df["V(vout)"]

for i in range(1, len(vout)):
    if vout.iloc[i-1] < 0 <= vout.iloc[i]:
        print("Rising edge at", df["time"].iloc[i])
    if vout.iloc[i-1] > 0 >= vout.iloc[i]:
        print("Falling edge at", df["time"].iloc[i])
        
print()
print("=" * 80)
print("END OF REPORT")
print("=" * 80)