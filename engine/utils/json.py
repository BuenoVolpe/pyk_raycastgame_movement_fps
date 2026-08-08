import json
from typing import Any
from engine.utils.log import log_error
from pathlib import Path
#------------------------------------#
def json_reader(path: str | Path, default: dict | None = None) -> dict:
    """Reads a JSON file and returns a dictionary safely."""
    path = Path(path)
    #------------------------------------#
    if not path.exists():
        return default or {}
    #------------------------------------#
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    #------------------------------------#
    except json.JSONDecodeError as e:
        log_error(f"Invalid JSON format: {path}")
        log_error(e)
    #------------------------------------#
    except Exception as e:
        log_error(f"Error reading JSON: {path}")
        log_error(e)

    return default or {}
#------------------------------------#
def scan_folder(base_folder: str | Path, extension: str = ".png") -> list[tuple[str, str]]:
    base_folder = Path(base_folder)

    return [
        (str(file), file.stem) #(full_path, file_name)
        for file in base_folder.rglob(f"*{extension}")
    ]
#------------------------------------#
def scan_folder_with_json(base_folder: str | Path, extension: str = ".png") -> list[dict[str, Any]]:

    base_folder = Path(base_folder)
    results = []

    for file in base_folder.rglob(f"*{extension}"):
        json_path = file.with_suffix(".json")

        metadata = json_reader(json_path)

        results.append({
            "name": file.stem,
            "file_path": str(file),
            "json_path": str(json_path) if json_path.exists() else None,
            "metadata": metadata
        })

    return results
#------------------------------------#
def scan_folder_for_json(base_folder: str | Path, extension: str = ".json") -> list[dict[str, Any]]:
    base_folder = Path(base_folder)
    results = []

    for file in base_folder.rglob(f"*{extension}"):
        try:
            data = json_reader(file)
            results.append({
                "name": file.stem,
                "json_path": str(file),
                "data": data
            })
        except Exception as e:
            log_error(f"Error processing JSON: {file}")
            log_error(e)

    return results
#------------------------------------#
def json_writer(path: str | Path, data: dict, indent: int = 4) -> None:
    path = Path(path)

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)

    except Exception as e:
        log_error(f"Error writing JSON: {path}")
        log_error(e)
#------------------------------------#

