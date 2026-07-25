from pathlib import Path

from analogflow.parameter_editor import ParameterEditor
from analogflow.runner import LTSpiceRunner
from analogflow.parser import LTSpiceParser
from analogflow.exporter import CSVExporter


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

SOURCE_SCHEMATIC = ROOT / "analog" / "analog_parametric.asc"

LTSPICE = r"C:\Users\arush\AppData\Local\Programs\ADI\LTspice\LTspice.exe"

RESULTS = ROOT / "results"

PARAMETER = "W1"

VALUES = [
    "10k",
    "20k",
    "30k",
    "40k",
    "50k",
]

# ------------------------------------------------------------

generated_dir = RESULTS / "generated"
csv_dir = RESULTS / "csv"

generated_dir.mkdir(parents=True, exist_ok=True)
csv_dir.mkdir(parents=True, exist_ok=True)

runner = LTSpiceRunner(LTSPICE)

print(f"\nSweeping parameter '{PARAMETER}'\n")

for value in VALUES:

    print("-" * 60)
    print(f"{PARAMETER} = {value}")

    # --------------------------------------------------------
    # Generate modified schematic
    # --------------------------------------------------------

    editor = ParameterEditor(SOURCE_SCHEMATIC)

    editor.set_parameter(PARAMETER, value)

    asc_file = generated_dir / f"{PARAMETER}_{value}.asc"

    editor.save(asc_file)

    # --------------------------------------------------------
    # Run LTspice
    # --------------------------------------------------------

    simulation = runner.run(asc_file)

    # --------------------------------------------------------
    # Parse RAW
    # --------------------------------------------------------

    parser = LTSpiceParser(simulation["raw"])

    # --------------------------------------------------------
    # Export CSV
    # --------------------------------------------------------

    exporter = CSVExporter(parser)

    csv_file = csv_dir / f"{PARAMETER}_{value}.csv"

    exporter.export(csv_file)

    print(f"CSV saved to {csv_file}")

print("\nSweep completed successfully.")