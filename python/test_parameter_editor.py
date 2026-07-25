from pathlib import Path

from analogflow.parameter_editor import ParameterEditor

ROOT = Path(__file__).resolve().parent.parent

SOURCE = ROOT / "analog" / "analog_parametric.asc"

OUTPUT = (
    ROOT
    / "analog"
    / "generated"
    / "analog_parametric_W1_35k.asc"
)

editor = ParameterEditor(SOURCE)

editor.set_parameter("W1", "35k")

editor.save(OUTPUT)

print()

print("Created")

print(OUTPUT)