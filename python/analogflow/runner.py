from pathlib import Path
import subprocess


class LTSpiceRunner:
    """
    Reusable LTspice simulation runner.

    This class is intentionally independent of the CLI script
    (run_ltspice.py), which remains frozen as a verified entry point.
    """

    def __init__(self, ltspice_path):

        self.ltspice = Path(ltspice_path)

        if not self.ltspice.exists():
            raise FileNotFoundError(
                f"LTspice executable not found:\n{self.ltspice}"
            )

    # -------------------------------------------------------------

    def run(self, schematic):

        schematic = Path(schematic)

        if not schematic.exists():
            raise FileNotFoundError(
                f"Schematic not found:\n{schematic}"
            )

        print(f"\nRunning: {schematic.name}")

        subprocess.run(
            [
                str(self.ltspice),
                "-b",
                "-Run",
                str(schematic),
            ],
            check=True,
        )

        raw = schematic.with_suffix(".raw")
        log = schematic.with_suffix(".log")
        net = schematic.with_suffix(".net")

        if not raw.exists():
            raise FileNotFoundError(
                f"RAW file was not generated:\n{raw}"
            )

        return {
            "schematic": schematic,
            "raw": raw,
            "log": log,
            "net": net,
        }