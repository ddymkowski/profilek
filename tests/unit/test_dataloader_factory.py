from pathlib import Path

import pytest

from profilek.data_loaders.factory import DataLoaderFactory
from profilek.data_loaders._csv import CSVDataLoader
from profilek.exceptions import UnsupportedFileTypeException

RESOURCES_DIR = Path("tests/resources")


def test_dataloader_factory() -> None:
    loader = DataLoaderFactory.create(path=(RESOURCES_DIR / "example.csv"))

    assert isinstance(loader(), CSVDataLoader)


def test_dataloader_factory_unsupported_filetype() -> None:
    with pytest.raises(UnsupportedFileTypeException):
        DataLoaderFactory.create(path=(RESOURCES_DIR / "example.mp3"))
