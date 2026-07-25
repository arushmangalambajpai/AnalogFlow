from pathlib import Path

from analogflow.parser import LTSpiceParser
from analogflow.exporter import CSVExporter

ROOT = Path(__file__).resolve().parent.parent

RAW = ROOT / "analog" / "analog_parametric.raw"

OUTPUT = ROOT / "results" / "csv" / "simulation.csv"

parser = LTSpiceParser(RAW)

exporter = CSVExporter(parser)

df = exporter.export(OUTPUT)

print(df.head())

print()

print("Rows :", len(df))
print("Cols :", len(df.columns))

print()

print("Saved to")

print(OUTPUT)