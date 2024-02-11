import dataclasses
import json
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID


class ResultsJSONEncoder(json.JSONEncoder):
    def default(self, o) -> Any:
        if isinstance(o, (Path, UUID)):
            return str(o)

        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)

        return json.JSONEncoder.default(self, o)


@dataclasses.dataclass
class OutputModel:
    input_file_path: Path
    columns: list[str]
    rows_count: int
    start_time: datetime
    end_time: datetime
    run_id: UUID
    results: list[dict]

    def to_json(self) -> str:
        return json.dumps(self, cls=ResultsJSONEncoder, indent=4)
