from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any

import polars as pl
import yaml
from profilek.constants import POLARS_TYPES_MAPPING

from profilek.exceptions import InvalidSchemaException

@dataclasses.dataclass(slots=True)
class PluginConfig:
    path: str
    mapping: list[dict[str, str]]

@dataclasses.dataclass(slots=True)
class Config:
    loader_options: dict[str, Any]
    plugins: PluginConfig | None = None

    def __post_init__(self):
        self.loader_options["dtypes"] = self._evaluate_schema_input(
            self.loader_options["dtypes"]
        )

    @staticmethod
    def _evaluate_schema_input(schema: dict[str, str]) -> dict[str, pl.DataType]:
        polars_schema = {}
        for col_name, col_stringified_type in schema.items():
            try:
                polars_schema[col_name] = POLARS_TYPES_MAPPING[col_stringified_type]
            except KeyError:
                raise InvalidSchemaException(f"Unexpected datatype: {col_stringified_type}")

        return polars_schema

    @classmethod
    def from_yaml(cls, file_path: str) -> Config:
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"The file: {file_path} does not exist")

        with open(file_path, "r") as file:
            try:
                dict_config = yaml.safe_load(file)
            except (yaml.scanner.ScannerError, yaml.parser.ParserError) as err:
                raise NotImplementedError(
                    "Incorrectly formatted yaml file, check traceback"
                ) from err

        return cls(**dict_config)
