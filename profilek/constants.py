from pathlib import Path
import polars as pl

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SAVE_PATH = ROOT_DIR / "profiling_results"


POLARS_TYPES_MAPPING = {
    "String": pl.String,
    "Int8": pl.Int8,
    "Int16": pl.Int16,
    "Int32": pl.Int32,
    "Int64": pl.Int64,
    "Float32": pl.Float32,
    "Float64": pl.Float64,
    "Boolean": pl.Boolean,
    "Date": pl.Date,
    "Datetime": pl.Datetime,
}