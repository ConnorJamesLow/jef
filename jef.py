from typing import Any
import json
from observer import Observer
from os import path


def sync(file_path: str) -> Observer:
    """
    Create a new Observer that live-updates a given json file.
    """
    content = {}
    with open(file_path) as file:
        content = json.load(file)

    # Write the current state to the loaded file when a change happens
    def callback(root: Observer, name: str, value: Any) -> bool:
        with open(file_path, 'w+') as file:
            json.dump(root.to_dict(), file)

    
    return Observer(content, callback, path.basename(file_path))
