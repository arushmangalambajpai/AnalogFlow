from pathlib import Path

from analogflow.runner import LTSpiceRunner

ROOT = Path(__file__).resolve().parent.parent

runner = LTSpiceRunner(
    r"C:\Users\arush\AppData\Local\Programs\ADI\LTspice\LTspice.exe"
)

result = runner.run(
    ROOT / "analog" / "analog_parametric.asc"
)

print()

print("=" * 60)
print("Runner Output")
print("=" * 60)

for key, value in result.items():
    print(f"{key:12}: {value}")