from pathlib import Path

import polars as pl

from profilek.data_loaders.base import BaseDataLoader


class CSVDataLoader(BaseDataLoader):
    def load(path: Path, **kwargs) -> pl.DataFrame:
        return pl.read_csv(source=path, **kwargs)
