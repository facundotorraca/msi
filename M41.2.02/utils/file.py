import os


def save_file(data: bytes, path: str):
    """
    Save the given data to the specified file path.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as file:
        file.write(data)
