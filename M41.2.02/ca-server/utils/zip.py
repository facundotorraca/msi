import os
import zipfile
from pathlib import Path


def zip_files(zip_path: str, files: dict[Path, str]) -> str:
    """
    Creates a zip file.

    :param zip_path: Path to the output zip file.
    :param files: A dictionary of file_path: arcname pairs.
    """
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file_path, arcname in files.items():
            zipf.write(file_path, arcname)

    return zip_path
