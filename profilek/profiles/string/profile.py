import polars as pl

from profilek.profiles.base import BaseProfile
from profilek.profiles.utils import metric


class StringProfile(BaseProfile):
    @staticmethod
    @metric("Average string length")
    def average(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(pl.col(column_name).str.len_chars().mean())

    @staticmethod
    @metric("Minimum string length")
    def minimum(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(pl.col(column_name).str.len_chars().min())

    @staticmethod
    @metric("Maximum string length")
    def maximum(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(pl.col(column_name).str.len_chars().max())

    @staticmethod
    @metric("Standard deviation string length")
    def standard_deviation(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(pl.col(column_name).str.len_chars().std())

    @staticmethod
    @metric("Quantile 0.25 string length")
    def q25(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(pl.col(column_name).str.len_chars().quantile(0.25))

    @staticmethod
    @metric("Quantile 0.50 string length")
    def q50(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(pl.col(column_name).str.len_chars().quantile(0.50))

    @staticmethod
    @metric("Quantile 0.75 string length")
    def q75(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(pl.col(column_name).str.len_chars().quantile(0.75))

    @staticmethod
    @metric("Quantile 0.99 string length")
    def q99(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(pl.col(column_name).str.len_chars().quantile(0.99))

    @staticmethod
    @metric("Kurtosis string length")
    def kurtosis(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(pl.col(column_name).str.len_chars().kurtosis())
