<div align="center">



\# AnalogFlow



\### An Automation Framework for LTspice-Based Analog Circuit Characterization



\*Automate schematic generation, simulation, waveform extraction, parameter sweeps, and analog circuit characterization.\*



\---



!\[Python](https://img.shields.io/badge/Python-3.10+-blue.svg)

!\[LTspice](https://img.shields.io/badge/LTspice-24-orange.svg)

!\[License](https://img.shields.io/badge/License-MIT-green.svg)



</div>



\---



\# Overview



AnalogFlow is a lightweight Python framework that automates the complete LTspice simulation workflow.



Instead of manually editing schematics, launching simulations, exporting waveforms, and processing results, AnalogFlow provides a reproducible pipeline that performs these operations automatically.



The framework is designed for:



\- Analog circuit characterization

\- Parameter sweeps

\- Comparator analysis

\- Neural circuit exploration

\- Research automation

\- Rapid design-space exploration



\---



\# Features



\## Automatic Parameter Editing



Programmatically modify LTspice parameters without editing schematic files manually.



\- Resistors

\- Capacitors

\- Voltage sources

\- Custom `.param` values



\---



\## Batch LTspice Simulation



Launch LTspice directly from Python.



Supports:



\- Batch mode

\- Automatic RAW detection

\- Automatic LOG detection

\- Error reporting



\---



\## RAW File Parsing



Read LTspice RAW files directly.



Retrieve



\- simulation time

\- node voltages

\- currents

\- arbitrary traces



without exporting data manually.



\---



\## CSV Export



Convert LTspice simulations into CSV datasets suitable for



\- NumPy

\- Pandas

\- MATLAB

\- Excel

\- Machine Learning workflows



\---



\## Automated Circuit Characterization



Generate complete characterization datasets automatically.



Examples include



\- Voltage transfer characteristics

\- 2D parameter sweeps

\- Threshold analysis

\- Activation maps

\- Binary decision regions



\---



\## Report Generation



Automatically generate



\- CSV datasets

\- Markdown reports

\- Heatmaps

\- Publication-ready figures



\---



\# Framework Architecture



```

&#x20;                LTspice Schematic

&#x20;                       │

&#x20;                       ▼

&#x20;             ParameterEditor

&#x20;                       │

&#x20;                       ▼

&#x20;           Generated Schematics

&#x20;                       │

&#x20;                       ▼

&#x20;              LTSpiceRunner

&#x20;                       │

&#x20;                       ▼

&#x20;            LTspice RAW / LOG

&#x20;                       │

&#x20;                       ▼

&#x20;              LTSpiceParser

&#x20;               │            │

&#x20;               ▼            ▼

&#x20;        CSV Exporter   Characterization

&#x20;               │            │

&#x20;               └──────┬─────┘

&#x20;                      ▼

&#x20;            Reports • CSV • Figures

```



\---



\# Project Structure



```

AnalogFlow/



│

├── analog/

│   ├── LTspice schematics

│   └── generated schematics

│

├── analogflow/

│   ├── parameter\_editor.py

│   ├── runner.py

│   ├── parser.py

│   ├── exporter.py

│   └── experiment.py

│

├── python/

│   ├── characterize.py

│   ├── characterize\_neuron.py

│   ├── test\_runner.py

│   ├── test\_parser.py

│   ├── test\_parameter\_editor.py

│   ├── plot\_results.py

│   └── ...

│

├── output/

│

├── results/

│

├── README.md

└── LICENSE

```



\---



\# Core Modules



\## ParameterEditor



Reads LTspice schematics and modifies parameter values.



Example



```python

editor = ParameterEditor(source)



editor.set\_parameter("R1", "20k")



editor.save(output)

```



\---



\## LTSpiceRunner



Launches LTspice simulations directly.



```python

runner = LTSpiceRunner(LTSPICE)



simulation = runner.run(schematic)

```



Automatically detects



\- RAW file

\- LOG file

\- NET file



\---



\## LTSpiceParser



Reads LTspice RAW files.



```python

parser = LTSpiceParser(raw)



time = parser.get\_time()



vout = parser.get\_trace("V(vout)")

```



\---



\## CSVExporter



Converts simulation results into CSV format.



```python

exporter = CSVExporter(parser)



exporter.export(csv\_file)

```



\---



\# Example Workflow



```

LTspice Schematic



&#x20;       │



&#x20;       ▼



Parameter Editing



&#x20;       │



&#x20;       ▼



Simulation



&#x20;       │



&#x20;       ▼



RAW Parsing



&#x20;       │



&#x20;       ▼



CSV Export



&#x20;       │



&#x20;       ▼



Characterization



&#x20;       │



&#x20;       ▼



Heatmaps

Reports

Statistics

```



\---



\# Neuron Characterization



AnalogFlow includes an automated neuron characterization workflow.



The characterization script performs a complete two-dimensional sweep of input voltages.



For every operating point it



\- Generates a parameterized schematic

\- Runs LTspice

\- Extracts the final output voltage

\- Classifies the neuron output

\- Generates visualization



Outputs include



\- Continuous activation heatmap

\- Binary classification map

\- CSV dataset

\- Markdown report



\---



\# Example Results



\## Continuous Activation Map



<p align="center">

<img src="docs/images/activation\_heatmap.png" width="650">

</p>



\---



\## Binary Classification Map



<p align="center">

<img src="docs/images/classification\_heatmap.png" width="650">

</p>



\---



\# Installation



Clone the repository



```bash

git clone https://github.com/<username>/AnalogFlow.git



cd AnalogFlow

```



Create a virtual environment



```bash

python -m venv venv

```



Activate



Windows



```bash

venv\\Scripts\\activate

```



Linux



```bash

source venv/bin/activate

```



Install dependencies



```bash

pip install -r requirements.txt

```



\---



\# Running



\## Test LTspice



```bash

python python/test\_runner.py

```



\---



\## Parameter Sweep



```bash

python python/characterize.py

```



\---



\## Neuron Characterization



```bash

python python/characterize\_neuron.py

```



\---



\# Applications



AnalogFlow can be used for



\- Analog IC Design

\- Comparator Characterization

\- Sensor Interface Evaluation

\- Operational Amplifier Analysis

\- Neural Circuits

\- Research Automation

\- Analog Design Space Exploration

\- Educational Laboratories



\---



\# Current Capabilities



\- Automatic schematic generation

\- LTspice batch execution

\- RAW parsing

\- CSV export

\- Parameter sweeps

\- Two-dimensional characterization

\- Heatmap generation

\- Markdown report generation



\---



\# Planned Features



\- Monte Carlo automation

\- AC sweep automation

\- Frequency response characterization

\- Noise analysis

\- Optimization engine

\- Interactive dashboard

\- GitHub Pages documentation

\- Multi-dimensional parameter sweeps

\- SPICE compatibility beyond LTspice



\---



\# Requirements



\- Python 3.10+

\- LTspice 24

\- Windows



Python Packages



\- numpy

\- pandas

\- matplotlib



\---



\# License



Released under the MIT License.



\---



\# Author



\*\*Arush Mangalam Bajpai\*\*



Electrical and Electronics Engineering



BITS Pilani



\---



<div align="center">



\*\*AnalogFlow aims to simplify analog circuit exploration by making LTspice simulations reproducible, scriptable, and scalable.\*\*



</div>

