import os
from pathlib import Path

from profilek.constants import DEFAULT_SAVE_PATH
from profilek.storage.base import BaseStorage
from profilek.storage.data import OutputModel


class FileSystemStorage(BaseStorage):
    def __init__(self, save_path: Path = DEFAULT_SAVE_PATH) -> None:
        super().__init__()
        self._save_path = save_path

        if not os.path.exists(self._save_path):
            os.makedirs(self._save_path)

    def save_profile_results(self, data: OutputModel) -> None:
        file_name = f"{data.start_time}_{data.run_id}.json"
        full_path = self._save_path / file_name

        with open(full_path, "w") as f:
            f.write(data.to_json())
