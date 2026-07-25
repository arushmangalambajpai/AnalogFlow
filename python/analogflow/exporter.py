from pathlib import Path
import pandas as pd


class CSVExporter:

    def __init__(self, parser):
        self.parser = parser

    def export(self, filename):

        data = {}

        for trace in self.parser.list_traces():
            data[trace] = self.parser.get_trace(trace)

        df = pd.DataFrame(data)

        Path(filename).parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(filename, index=False)

        return df