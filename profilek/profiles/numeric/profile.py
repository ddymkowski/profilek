import polars as pl

from profilek.profiles.base import BaseProfile
from profilek.profiles.utils import metric


class NumericProfile(BaseProfile):
    @staticmethod
    @metric("Average")
    def average(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(column_name).mean()

    @staticmethod
    @metric("Minimum")
    def minimum(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(column_name).min()

    @staticmethod
    @metric("Maximum")
    def maximum(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(column_name).max()

    @staticmethod
    @metric("Standard deviation")
    def standard_deviation(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(column_name).std()

    @staticmethod
    @metric("Quantile 0.25")
    def q25(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(column_name).quantile(0.25)

    @staticmethod
    @metric("Quantile 0.50")
    def q50(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(column_name).quantile(0.50)

    @staticmethod
    @metric("Quantile 0.75")
    def q75(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(column_name).quantile(0.75)

    @staticmethod
    @metric("Quantile 0.99")
    def q99(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(column_name).quantile(0.99)

    @staticmethod
    @metric("Kurtosis")
    def kurtosis(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(pl.col(column_name).kurtosis())
