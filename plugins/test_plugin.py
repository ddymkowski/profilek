import polars as pl

from profilek.profiles import BaseProfile
from profilek.profiles.utils import metric


class TestPluginProfile(BaseProfile):
    @staticmethod
    @metric("test plugin metric")
    def test_metric(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(column_name).count()
