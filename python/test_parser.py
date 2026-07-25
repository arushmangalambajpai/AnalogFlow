from pathlib import Path

from analogflow.parser import LTSpiceParser

ROOT = Path(__file__).resolve().parent.parent

RAW = ROOT / "analog" / "analog_parametric.raw"

parser = LTSpiceParser(RAW)

print()

print("=" * 60)
print("Available Traces")
print("=" * 60)

for trace in parser.list_traces():
    print(trace)

print()

time = parser.get_time()

print("Samples :", len(time))
print("Start   :", time[0])
print("End     :", time[-1])