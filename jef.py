from typing import Any
import json
from observer import Observer
from util import load_or_create
from os import path


def subjectify(file_path: str) -> Observer:
    """
    Creates a new observer that live-updates a given json file (where the file is "subjected" to updates within the observer).
    """
    content = load_or_create(file_path)

    # Write the current state to the loaded file when a change happens
    def callback(root: Observer, name: str, value: Any) -> bool:
        with open(file_path, 'w+') as file:
            json.dump(root.to_dict(), file)
    return Observer(content, callback, path.splitext(path.basename(file_path))[0])
