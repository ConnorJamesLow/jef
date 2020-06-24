import json
from os import path


def load_or_create(file_path: str) -> dict:
    if not path.exists(file_path):
        with open(file_path, 'w+') as file:
            json.dump({}, file)
            return {}
    with open(file_path) as file:
        return json.load(file)
