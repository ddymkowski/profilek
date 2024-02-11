import logging
from abc import ABC, abstractmethod
from pathlib import Path

import polars as pl


class BaseDataLoader(ABC):
    def __init__(self) -> None:
        self._logger: logging.Logger = logging.getLogger(self.__class__.__qualname__)

    @abstractmethod
    def load(path: Path, **kwargs) -> pl.DataFrame:
        pass
