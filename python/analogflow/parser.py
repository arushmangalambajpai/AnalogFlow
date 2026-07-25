from pathlib import Path
from PyLTSpice import RawRead


class LTSpiceParser:
    """
    Reads LTspice RAW files.
    """

    def __init__(self, raw_file: str | Path):

        self.raw_file = Path(raw_file)

        if not self.raw_file.exists():
            raise FileNotFoundError(self.raw_file)

        self.raw = RawRead(str(self.raw_file))

    # --------------------------------------------------

    def list_traces(self):

        return self.raw.get_trace_names()

    # --------------------------------------------------

    def get_trace(self, name):

        return self.raw.get_trace(name).get_wave(0)

    # --------------------------------------------------

    def get_time(self):

        return self.raw.get_trace("time").get_wave(0)