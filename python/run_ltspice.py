from pathlib import Path
import subprocess

# ============================================================
# Configuration
# ============================================================

LTSPICE = Path(r"C:\Users\arush\AppData\Local\Programs\ADI\LTspice\LTspice.exe")

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CIRCUIT = PROJECT_ROOT / "analog" / "analog_parametric.asc"

# ============================================================

print("=" * 60)
print("AnalogFlow")
print("=" * 60)

print(f"LTspice : {LTSPICE}")
print(f"Project : {PROJECT_ROOT}")
print(f"Circuit : {CIRCUIT}")

assert LTSPICE.exists()
assert CIRCUIT.exists()

print("\nLaunching LTspice...\n")

subprocess.run(
    [
        str(LTSPICE),
	"-b",
        "-Run",
        str(CIRCUIT)
    ],
    check=True
)

print("Simulation Finished Successfully!")