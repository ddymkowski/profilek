import logging
import time
from collections import OrderedDict
from pathlib import Path
from typing import Any
from uuid import uuid4

import polars as pl

from profilek.data_loaders.base import BaseDataLoader
from profilek.data_loaders.factory import DataLoaderFactory
from profilek.exceptions import InputFileNotFoundException
from profilek.profiles.base import BaseProfile
from profilek.profiles.factory import ProfileFactory
from profilek.storage.base import BaseStorage
from profilek.storage.data import OutputModel
from profilek.storage.fs import FileSystemStorage


class Profilek:
    def __init__(
        self,
        user_mapping: dict[pl.DataType, BaseProfile] | None = None,
        loader_factory: DataLoaderFactory | None = None,
        profile_factory: ProfileFactory | None = None,
        storage: BaseStorage | None = None,
    ) -> None:
        self._user_mapping = user_mapping if user_mapping else {}
        self._logger: logging.Logger = logging.getLogger(self.__class__.__qualname__)
        self._loader_factory: DataLoaderFactory = (
            loader_factory if loader_factory else DataLoaderFactory()
        )
        self._profile_factory: ProfileFactory = (
            profile_factory if profile_factory else ProfileFactory(self._user_mapping)
        )
        self._storage: BaseStorage = storage if storage else FileSystemStorage()

        self._logger.info(f"User profiles mapping: {user_mapping}")

    @staticmethod
    def _validate_file_exists(file_path: str) -> Path:
        path = Path(file_path)

        if not path.exists():
            raise InputFileNotFoundException(f"Passed file: {file_path} does not exist")

        return path

    def _load_data(self, data_path: str, **kwargs) -> tuple[Path, pl.DataFrame]:
        data_file_path: Path = self._validate_file_exists(data_path)
        loader: BaseDataLoader = self._loader_factory.create(data_file_path)
        dataframe: pl.DataFrame = loader.load(path=data_file_path, **kwargs)
        return data_file_path, dataframe

    def _run_profiles(
        self, data: pl.DataFrame, schema: dict[str, pl.DataType]
    ) -> list[dict]:
        results = []
        for column_name, dtype in schema.items():
            profile = self._profile_factory.create(dtype)()
            column_profile_results: pl.DataFrame = profile.run_all(data, column_name)
            jsonified_column_profile_results: dict[
                str, float | int | dict[str, str]
            ] = column_profile_results.to_dicts()[0]
            jsonified_column_profile_results["Column details"] = {
                "Column name": column_name,
                "Column type": dtype.__class__.__name__,
                "Profile Name": profile.__class__.__name__,
            }
            results.append(jsonified_column_profile_results)

        return results

    def profile(self, file_path: str, loader_options: dict[str, Any]) -> None:
        run_id = uuid4()
        self._logger.info(f"Starting profiling job: {run_id}")
        start = int(time.time())
        path, data = self._load_data(data_path=file_path, **loader_options)

        columns: list[str] = data.columns
        schema: OrderedDict[str, str] = data.schema
        rows_count: int = data.height

        results = self._run_profiles(data=data, schema=schema)

        end = int(time.time())
        data = OutputModel(
            input_file_path=path.absolute(),
            columns=columns,
            rows_count=rows_count,
            start_time=start,
            end_time=end,
            run_id=run_id,
            results=results,
        )

        self._storage.save_profile_results(data)
