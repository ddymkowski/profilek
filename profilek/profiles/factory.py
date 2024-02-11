import polars as pl

from profilek.profiles import (
    BaseProfile,
    DateProfile,
    DatetimeProfile,
    NumericProfile,
    StringProfile,
)


class ProfileFactory:
    NUMERIC = {
        pl.Float32: NumericProfile,
        pl.Float64: NumericProfile,
        pl.Int8: NumericProfile,
        pl.Int16: NumericProfile,
        pl.Int32: NumericProfile,
        pl.Int64: NumericProfile,
    }

    STRING = {pl.String: StringProfile}

    DATE = {pl.Date: DateProfile}

    DATETIME = {pl.Datetime: DatetimeProfile}

    MAPPING = {**NUMERIC, **STRING, **DATE, **DATETIME}

    def __init__(self, user_mapping: dict[pl.DataType, BaseProfile]) -> None:
        self._mapping = {**self.MAPPING, **user_mapping}

    def create(self, dtype: pl.DataType) -> BaseProfile:
        return self._mapping.get(dtype, BaseProfile)
