from pathlib import Path
import json
import logging


def get_file(name: str) -> Path:
    return Path(__file__).resolve().parent / name


def get_data():
    with get_file("data.json").open(encoding="utf-8") as f:
        try:
            data: dict[str, str] = json.load(f)
        except json.decoder.JSONDecodeError:
            logging.error("JSON is invalid")
            return
    return data


def save_data(data: dict[str, str]):
    with get_file("data.json").open("w", encoding="utf-8") as f:
        json.dump(data, f)
