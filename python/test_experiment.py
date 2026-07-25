from pathlib import Path

from analogflow.experiment import Experiment

ROOT = Path(__file__).resolve().parent.parent

experiment = Experiment(
    source_schematic=ROOT / "analog" / "analog_parametric.asc",
    output_directory=ROOT / "results",
    parameter="W1",
    value="35k",
    ltspice_path=r"C:\Users\arush\AppData\Local\Programs\ADI\LTspice\LTspice.exe",
)

result = experiment.run()

print()

print("Generated Files")

for key, value in result.items():
    print(f"{key:12} : {value}")