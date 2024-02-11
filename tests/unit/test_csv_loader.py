from pathlib import Path
import polars as pl
from profilek.data_loaders._csv import CSVDataLoader

RESOURCES_DIR = Path("tests/resources")


def test_csv_loader() -> None:
    schema = {
        "Name": pl.String,
        "Salary": pl.Int64,
        "Height": pl.Float32,
        "IsMarried": pl.Boolean,
        "DOB": pl.Date,
        "InsertionTimestamp": pl.Datetime,
    }

    df = CSVDataLoader.load(path=(RESOURCES_DIR / "example.csv"), dtypes=schema)

    assert isinstance(df, pl.DataFrame)
