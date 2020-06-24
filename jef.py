import json
from observer import Observer
from os import path


def sync(file_path):
    content = {}
    with open(file_path) as file:
        content = json.load(file)

    def callback(root: Observer, name: str, value: any) -> bool:
        with open(file_path, 'w+') as file:
            json.dump(root.to_dict(), file)
    return Observer(content, callback, path.basename(file_path))
