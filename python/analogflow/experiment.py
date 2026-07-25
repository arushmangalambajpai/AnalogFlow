from pathlib import Path

from analogflow.parameter_editor import ParameterEditor
from analogflow.runner import LTSpiceRunner
from analogflow.parser import LTSpiceParser
from analogflow.exporter import CSVExporter


class Experiment:

    def __init__(
        self,
        *,
        source_schematic,
        output_directory,
        parameter,
        value,
        ltspice_path,
    ):

        self.source = Path(source_schematic)
        self.output = Path(output_directory)

        self.parameter = parameter
        self.value = value

        self.runner = LTSpiceRunner(ltspice_path)

    # ------------------------------------------------------------

    def run(self):

        generated_dir = self.output / "generated"

        raw_dir = self.output / "raw"

        csv_dir = self.output / "csv"

        generated_dir.mkdir(parents=True, exist_ok=True)
        raw_dir.mkdir(parents=True, exist_ok=True)
        csv_dir.mkdir(parents=True, exist_ok=True)

        asc_name = f"{self.parameter}_{self.value}.asc"

        generated_asc = generated_dir / asc_name

        editor = ParameterEditor(self.source)

        editor.set_parameter(self.parameter, self.value)

        editor.save(generated_asc)

        self.runner.run(generated_asc)

        raw_file = generated_asc.with_suffix(".raw")

        parser = LTSpiceParser(raw_file)

        exporter = CSVExporter(parser)

        csv_file = csv_dir / f"{self.parameter}_{self.value}.csv"

        exporter.export(csv_file)

        return {
            "schematic": generated_asc,
            "raw": raw_file,
            "csv": csv_file,
        }