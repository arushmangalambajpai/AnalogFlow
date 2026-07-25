import math
import re
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analogflow.parser import LTSpiceParser
from analogflow.parameter_editor import ParameterEditor
from analogflow.runner import LTSpiceRunner

# ==============================================================================
# CONFIGURATION
# ==============================================================================
SCHEMATIC = Path(__file__).parent.parent / "analog" / "analog_parametric.asc"
LTSPICE = r"C:\Users\arush\AppData\Local\Programs\ADI\LTspice\LTspice.exe"
OUTPUT_DIRECTORY = "./output"

START = 0.0
STOP = 5.0
STEP = 0.2
THRESHOLD = 2.5


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def prepare_parameterized_schematic(source_path: Path, dest_path: Path) -> Path:
    """
    Reads the original schematic, replaces PULSE(...) voltage sources for V1 and V2
    with DC parameters {VIN1} and {VIN2}, ensures .param directives exist,
    and writes to dest_path without altering the source schematic.
    """
    if not source_path.exists():
        raise FileNotFoundError(f"Source schematic not found: {source_path}")

    content = source_path.read_text(encoding="utf-8")

    # Replace PULSE(...) values for V1 and V2 with parameterized DC values
    # Regex matches SYMATTR Value PULSE(...) specifically associated with V1/V2 blocks
    

    # Alternatively, perform direct line replacement if symbol ordering varies
    lines = content.splitlines()
    

    # Robust fallback line-by-line replacement for standard LTspice format
    for i in range(len(lines) - 1):

        if (
            lines[i].startswith("SYMATTR Value ")
            and lines[i + 1].startswith("SYMATTR InstName V1")
        ):
            lines[i] = "SYMATTR Value DC {VIN1}"

        elif (
            lines[i].startswith("SYMATTR Value ")
            and lines[i + 1].startswith("SYMATTR InstName V2")
        ):
            lines[i] = "SYMATTR Value DC {VIN2}"

    content = "\n".join(lines)

    # Append .param VIN1=0 and .param VIN2=0 if not present
    if not re.search(r"\.param\s+VIN1\b", content, re.IGNORECASE):
        content += "\nTEXT -32 32 Left 0 !.param VIN1=0\n"
    if not re.search(r"\.param\s+VIN2\b", content, re.IGNORECASE):
        content += "\nTEXT -32 32 Left 0 !.param VIN2=0\n"

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(content, encoding="utf-8")
    return dest_path


def format_time(seconds: float) -> str:
    """Format seconds into a human-readable duration string."""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{int(h)}h {int(m)}m {int(s)}s"
    elif m > 0:
        return f"{int(m)}m {int(s)}s"
    else:
        return f"{seconds:.1f}s"


# ==============================================================================
# MAIN WORKFLOW
# ==============================================================================
def main():
    out_dir = Path(OUTPUT_DIRECTORY)
    out_dir.mkdir(parents=True, exist_ok=True)

    source_schematic_path = Path(SCHEMATIC)
    param_schematic_path = out_dir / "parameterized.asc"

    print("--- Preparing Parameterized Schematic ---")
    prepare_parameterized_schematic(source_schematic_path, param_schematic_path)

    # Generate sweep values
    num_steps = int(round((STOP - START) / STEP)) + 1
    vin_range = [round(START + i * STEP, 6) for i in range(num_steps)]

    sweep_points = [(v1, v2) for v1 in vin_range for v2 in vin_range]
    total_sims = len(sweep_points)

    runner = LTSpiceRunner(LTSPICE)

    results = []
    start_time = time.time()

    print(f"\nStarting characterization sweep across {total_sims} total points...")
    print(f"Sweep Range: [{START}, {STOP}], Step: {STEP}\n")
    generated_dir = out_dir / "generated"
    generated_dir.mkdir(exist_ok=True)
    for idx, (v1_val, v2_val) in enumerate(sweep_points, start=1):
        sim_start_time = time.time()

        # Parameter Editor directly handles setting parameters on destination file
        generated_schematic = generated_dir / f"sim_{idx:05d}.asc"
        
        editor = ParameterEditor(param_schematic_path)
        editor.set_parameter("VIN1", str(v1_val))
        editor.set_parameter("VIN2", str(v2_val))
        editor.save(generated_schematic)
        
        vout_final = np.nan
        
        try:
            sim_res = runner.run(generated_schematic)
            raw_path = sim_res["raw"]

            # Parse trace output
            parser = LTSpiceParser(raw_path)

            # Try common node naming variations for Vout
            vout_trace_name = None

            for trace in parser.list_traces():
                if "vout" in trace.lower():
                    vout_trace_name = trace
                    break

            if vout_trace_name:
                v_wave = parser.get_trace(vout_trace_name)
                vout_final = float(v_wave[-1])
            else:
                available = parser.list_traces()
                print(f"Warning: V(Vout) trace not found.")
                print("Available traces:")
                print(available)
        except Exception as e:
            print(f"Simulation failed for VIN1={v1_val}, VIN2={v2_val}: {e}")
            vout_final = np.nan

        # Categorize
        if np.isnan(vout_final):
            cls_val = np.nan
        else:
            cls_val = 1 if vout_final >= THRESHOLD else 0

        results.append(
            {
                "VIN1": v1_val,
                "VIN2": v2_val,
                "VOUT": vout_final,
                "CLASS": cls_val,
            }
        )

        # Progress reporting
        elapsed = time.time() - start_time
        pct = (idx / total_sims) * 100
        avg_per_sim = elapsed / idx
        eta = avg_per_sim * (total_sims - idx)

        print(
            f"Current simulation: VIN1={v1_val:.2f}V, VIN2={v2_val:.2f}V | "
            f"[{idx}/{total_sims}] {pct:.1f}% Complete | "
            f"Elapsed: {format_time(elapsed)} | ETA: {format_time(eta)}"
        )

    total_execution_time = time.time() - start_time

    # Construct DataFrame
    df = pd.DataFrame(results)

    # Save CSV
    csv_path = out_dir / "characterization.csv"
    df.to_csv(csv_path, index=False)
    print(f"\nSaved CSV: {csv_path}")

    # Reshape for Heatmaps
    pivot_activation = df.pivot(index="VIN2", columns="VIN1", values="VOUT")
    pivot_classification = df.pivot(index="VIN2", columns="VIN1", values="CLASS")

    # Generate Activation Heatmap
    plt.figure(figsize=(8, 6))
    plt.imshow(
        pivot_activation.values,
        extent=[START, STOP, START, STOP],
        origin="lower",
        aspect="auto",
        interpolation="nearest",
        cmap="viridis",
    )
    plt.colorbar(label="VOUT (V)")
    plt.title("Neuron Activation Heatmap (Continuous VOUT)")
    plt.xlabel("VIN1 (V)")
    plt.ylabel("VIN2 (V)")
    activation_heatmap_path = out_dir / "activation_heatmap.png"
    plt.tight_layout()
    plt.savefig(activation_heatmap_path, dpi=300)
    plt.close()

    # Generate Classification Heatmap
    plt.figure(figsize=(8, 6))
    plt.imshow(
        pivot_classification.values,
        extent=[START, STOP, START, STOP],
        origin="lower",
        aspect="auto",
        interpolation="nearest",
        cmap="coolwarm",
    )
    plt.colorbar(label=f"Class (Threshold = {THRESHOLD}V)")
    plt.title("Neuron Classification Heatmap (Binary Output)")
    plt.xlabel("VIN1 (V)")
    plt.ylabel("VIN2 (V)")
    classification_heatmap_path = out_dir / "classification_heatmap.png"
    plt.tight_layout()
    plt.savefig(classification_heatmap_path, dpi=300)
    plt.close()

    # Calculate statistics for the report
    valid_vout = df["VOUT"].dropna()
    max_vout = float(valid_vout.max()) if not valid_vout.empty else np.nan
    min_vout = float(valid_vout.min()) if not valid_vout.empty else np.nan
    mean_vout = float(valid_vout.mean()) if not valid_vout.empty else np.nan

    # Generate Markdown Report
    report_content = f"""# Characterization Report

## Executive Summary
- **Total Simulations:** {total_sims}
- **Sweep Range:** {START}V to {STOP}V
- **Step Size:** {STEP}V
- **Classification Threshold:** {THRESHOLD}V
- **Total Execution Time:** {format_time(total_execution_time)}

## Output Statistics
- **Maximum Output (VOUT):** {max_vout:.4f} V
- **Minimum Output (VOUT):** {min_vout:.4f} V
- **Mean Output (VOUT):** {mean_vout:.4f} V

## Generated Artifacts
- Data File: `characterization.csv`
- Continuous Activation Map: `activation_heatmap.png`
- Binary Classification Map: `classification_heatmap.png`
"""
    report_path = out_dir / "characterization_report.md"
    report_path.write_text(report_content, encoding="utf-8")
    print(f"Saved Report: {report_path}")
    print("\nNeuron characterization complete!")


if __name__ == "__main__":
    main()