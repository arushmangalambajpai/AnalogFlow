from pathlib import Path
import re


class ParameterEditor:
    """
    Creates modified copies of LTspice schematics by updating .param values.
    The source schematic is never modified.
    """

    def __init__(self, schematic):

        self.source = Path(schematic)

        if not self.source.exists():
            raise FileNotFoundError(self.source)

        self.text = self.source.read_text(encoding="utf-8")

    # ---------------------------------------------------------

    def set_parameter(self, parameter, value):

        pattern = rf"(\.param\s+{re.escape(parameter)}\s*=\s*)([^\s]+)"

        if not re.search(pattern, self.text, flags=re.IGNORECASE):
            raise ValueError(f"Parameter '{parameter}' not found.")

        self.text = re.sub(
            pattern,
            rf"\g<1>{value}",
            self.text,
            flags=re.IGNORECASE,
        )

    # ---------------------------------------------------------

    def save(self, filename):

        filename = Path(filename)

        filename.parent.mkdir(parents=True, exist_ok=True)

        filename.write_text(self.text, encoding="utf-8")

        return filename