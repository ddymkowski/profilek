from pathlib import Path

from profilek.data_loaders._csv import CSVDataLoader
from profilek.data_loaders.base import BaseDataLoader
from profilek.exceptions import UnsupportedFileTypeException


class DataLoaderFactory:
    @staticmethod
    def create(path: Path) -> BaseDataLoader:
        extension_loader_mapping = {".csv": CSVDataLoader}

        loader: BaseDataLoader | None = extension_loader_mapping.get(path.suffix)

        if not loader:
            raise UnsupportedFileTypeException(
                f"Given file format is not supported. Supported types are: {' '.join(list(extension_loader_mapping.keys()))}."
            )

        return loader
