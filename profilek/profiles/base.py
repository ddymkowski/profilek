import polars as pl

from profilek.profiles.utils import metric


class BaseProfile:
    @staticmethod
    @metric("Nulls count")
    def nulls_count(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(column_name).null_count()

    @staticmethod
    @metric("Uniques count")
    def uniques_count(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        return df.select(column_name).unique().count()

    def run_all(self, df: pl.DataFrame, column_name: str) -> pl.DataFrame:
        metrics_decorated = filter(
            lambda x: hasattr(x, "__metric__"),
            (getattr(self, name) for name in dir(self)),
        )

        results: list[pl.DataFrame] = []

        for metric in metrics_decorated:
            metric_df = metric(df=df, column_name=column_name)
            results.append(metric_df)

        merged_results: pl.DataFrame = pl.concat(items=results, how="horizontal")
        return merged_results
