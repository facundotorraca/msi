import os
import json


def save_bin_file(data: bytes, path: str) -> str:
    """
    Save the given data to the specified file path.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as file:
        file.write(data)

    return path


def save_json_file(data: dict, path: str) -> str:
    """
    Save the given data as a JSON file to the specified file path.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as file:
        json.dump(data, file, indent=4)

    return path


def safe_delete_file(path: str):
    """
    Delete the file at the given path.
    """
    if os.path.exists(path):
        os.remove(path)
