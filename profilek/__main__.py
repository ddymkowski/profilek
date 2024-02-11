from __future__ import annotations

from pathlib import Path

import polars as pl
import argparse
import json
import logging.config
from profilek.config import Config
from profilek.constants import POLARS_TYPES_MAPPING
from profilek.exceptions import UserPluginMappingException
from profilek.plugin_loader import PluginLoader
from profilek.profiler import Profilek
from profilek.profiles.base import BaseProfile


def setup_logger(log_config_file_path: Path) -> None:
    with open(log_config_file_path) as f:
        config = json.load(f)
    logging.config.dictConfig(config)

def evaluate_user_plugin_mapping(user_mapping: list[dict[str, str]], available_plugins: dict[str, BaseProfile]) -> dict[pl.DataType, BaseProfile]:
    user_mapping_evaluated = {}
    for entry in user_mapping:
        evaluated_datatype: pl.DataType = POLARS_TYPES_MAPPING.get(entry['type'])
        evaluated_plugin: type = available_plugins.get(entry['class'])

        if not evaluated_datatype:
            raise UserPluginMappingException(f"Passed polars datatype string literal is not supported: {entry['type']}")
    
        if not evaluated_plugin:
            raise UserPluginMappingException(f"Could not find given plugin class within available plugins: {entry['class']}. Found plugins: {[available_plugins.keys()]}")
        
        user_mapping_evaluated[evaluated_datatype] = evaluated_plugin

    return user_mapping_evaluated

def main(
    input_file_path: Path,
    config_file_path: Path,
    json_logger_config_path: Path,
) -> None:
    setup_logger(json_logger_config_path)
    config = Config.from_yaml(config_file_path)
    available_plugins = PluginLoader(config.plugins['path']).plugins if config.plugins else {}
    user_mapping: dict[pl.DataType, BaseProfile] = evaluate_user_plugin_mapping(user_mapping=config.plugins['mapping'], available_plugins=available_plugins) if config.plugins else {}

    profiler = Profilek(user_mapping=user_mapping)
    profiler.profile(input_file_path, loader_options=config.loader_options)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data profiler")
    parser.add_argument("-i", "--input-path", type=Path, help="Path to input file")
    parser.add_argument("-c", "--config-path", type=Path, help="Path to config file")
    parser.add_argument(
        "-l",
        "--log-cfg-path",
        type=Path,
        help="Path to logger json config",
        default="log_cfg.json",
    )

    args = parser.parse_args()
    main(
        input_file_path=args.input_path,
        config_file_path=args.config_path,
        json_logger_config_path=args.log_cfg_path,
    )
