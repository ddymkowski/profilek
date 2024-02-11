from pathlib import Path
from profilek.config import Config


RESOURCES_DIR = Path("tests/resources")


def test_config():
    cfg = Config.from_yaml(RESOURCES_DIR / "cfg.yaml")
    assert isinstance(cfg, Config)
