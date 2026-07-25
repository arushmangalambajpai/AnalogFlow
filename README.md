<div align="center">

# AnalogFlow

### An Automation Framework for LTspice-Based Analog Circuit Characterization

*Automate schematic generation, simulation, waveform extraction, parameter sweeps, and analog circuit characterization.*

---

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![LTspice](https://img.shields.io/badge/LTspice-24-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

</div>

---

# Overview

AnalogFlow is a lightweight Python framework that automates the complete LTspice simulation workflow.

Instead of manually editing schematics, launching simulations, exporting waveforms, and processing results, AnalogFlow provides a reproducible pipeline that performs these operations automatically.

The framework is designed for:

- Analog circuit characterization
- Parameter sweeps
- Comparator analysis
- Neural circuit exploration
- Research automation
- Rapid design-space exploration

---

# Features

## Automatic Parameter Editing

Programmatically modify LTspice parameters without editing schematic files manually.

- Resistors
- Capacitors
- Voltage sources
- Custom `.param` values

---

## Batch LTspice Simulation

Launch LTspice directly from Python.

Supports:

- Batch mode
- Automatic RAW detection
- Automatic LOG detection
- Error reporting

---

## RAW File Parsing

Read LTspice RAW files directly.

Retrieve

- simulation time
- node voltages
- currents
- arbitrary traces

without exporting data manually.

---

## CSV Export

Convert LTspice simulations into CSV datasets suitable for

- NumPy
- Pandas
- MATLAB
- Excel
- Machine Learning workflows

---

## Automated Circuit Characterization

Generate complete characterization datasets automatically.

Examples include

- Voltage transfer characteristics
- 2D parameter sweeps
- Threshold analysis
- Activation maps
- Binary decision regions

---

## Report Generation

Automatically generate

- CSV datasets
- Markdown reports
- Heatmaps
- Publication-ready figures

---

# Framework Architecture

```
                 LTspice Schematic
                        │
                        ▼
              ParameterEditor
                        │
                        ▼
            Generated Schematics
                        │
                        ▼
               LTSpiceRunner
                        │
                        ▼
             LTspice RAW / LOG
                        │
                        ▼
               LTSpiceParser
                │            │
                ▼            ▼
         CSV Exporter   Characterization
                │            │
                └──────┬─────┘
                       ▼
             Reports • CSV • Figures
```

---

# Project Structure

```
AnalogFlow/

│
├── analog/
│   ├── LTspice schematics
│   └── generated schematics
│
├── analogflow/
│   ├── parameter_editor.py
│   ├── runner.py
│   ├── parser.py
│   ├── exporter.py
│   └── experiment.py
│
├── python/
│   ├── characterize.py
│   ├── characterize_neuron.py
│   ├── test_runner.py
│   ├── test_parser.py
│   ├── test_parameter_editor.py
│   ├── plot_results.py
│   └── ...
│
├── output/
│
├── results/
│
├── README.md
└── LICENSE
```

---

# Core Modules

## ParameterEditor

Reads LTspice schematics and modifies parameter values.

Example

```python
editor = ParameterEditor(source)

editor.set_parameter("R1", "20k")

editor.save(output)
```

---

## LTSpiceRunner

Launches LTspice simulations directly.

```python
runner = LTSpiceRunner(LTSPICE)

simulation = runner.run(schematic)
```

Automatically detects

- RAW file
- LOG file
- NET file

---

## LTSpiceParser

Reads LTspice RAW files.

```python
parser = LTSpiceParser(raw)

time = parser.get_time()

vout = parser.get_trace("V(vout)")
```

---

## CSVExporter

Converts simulation results into CSV format.

```python
exporter = CSVExporter(parser)

exporter.export(csv_file)
```

---

# Example Workflow

```
LTspice Schematic

        │

        ▼

Parameter Editing

        │

        ▼

Simulation

        │

        ▼

RAW Parsing

        │

        ▼

CSV Export

        │

        ▼

Characterization

        │

        ▼

Heatmaps
Reports
Statistics
```

---

# Neuron Characterization

AnalogFlow includes an automated neuron characterization workflow.

The characterization script performs a complete two-dimensional sweep of input voltages.

For every operating point it

- Generates a parameterized schematic
- Runs LTspice
- Extracts the final output voltage
- Classifies the neuron output
- Generates visualization

Outputs include

- Continuous activation heatmap
- Binary classification map
- CSV dataset
- Markdown report

---

# Example Results

## Continuous Activation Map

<p align="center">
<img src="docs/images/activation_heatmap.png" width="650">
</p>

---

## Binary Classification Map

<p align="center">
<img src="docs/images/classification_heatmap.png" width="650">
</p>

---

# Installation

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
venv\Scripts\activate
```

Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running

## Test LTspice

```bash
python python/test_runner.py
```

---

## Parameter Sweep

```bash
python python/characterize.py
```

---

## Neuron Characterization

```bash
python python/characterize_neuron.py
```

---

# Applications

AnalogFlow can be used for

- Analog IC Design
- Comparator Characterization
- Sensor Interface Evaluation
- Operational Amplifier Analysis
- Neural Circuits
- Research Automation
- Analog Design Space Exploration
- Educational Laboratories

---

# Current Capabilities

- Automatic schematic generation
- LTspice batch execution
- RAW parsing
- CSV export
- Parameter sweeps
- Two-dimensional characterization
- Heatmap generation
- Markdown report generation

---

# Planned Features

- Monte Carlo automation
- AC sweep automation
- Frequency response characterization
- Noise analysis
- Optimization engine
- Interactive dashboard
- GitHub Pages documentation
- Multi-dimensional parameter sweeps
- SPICE compatibility beyond LTspice

---

# Requirements

- Python 3.10+
- LTspice 24
- Windows

Python Packages

- numpy
- pandas
- matplotlib

---

# License

Released under the MIT License.

---

# Author

**Arush Mangalam Bajpai**

Electrical and Electronics Engineering

BITS Pilani

---

<div align="center">

**AnalogFlow aims to simplify analog circuit exploration by making LTspice simulations reproducible, scriptable, and scalable.**

</div>
