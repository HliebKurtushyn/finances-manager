from json import dump, load
from os import makedirs
from os.path import exists

def dump_to_json(file_name: str, obj: object): # Tested
    folder = 'data'
    path_to_file = f'{folder}/{file_name}.json'

    makedirs(folder, exist_ok=True)

    with open(path_to_file, "w") as file:
        dump(obj, file, indent=3)
        return True

def load_from_json(file_name: str): # Tested
    folder = 'data'
    path_to_file = f'{folder}/{file_name}.json'

    makedirs(folder, exist_ok=True)

    if not exists(path_to_file):
        return {}

    if exists(path_to_file) and open(path_to_file, 'r').read().strip() == "":
        return {}

    with open(path_to_file, "r") as file:
        return load(file)

def create_settings(): # Tested
    path_to_file = 'data/settings.json'

    default_settings = {
        "default_currency": "EUR",
    }

    makedirs('data', exist_ok=True)

    if not exists(path_to_file):
        dump_to_json('settings', default_settings)

    current_settings = load_from_json('settings')

    return True

def restore_settings(): # Tested
    default_settings = {
        "default_currency": "EUR",
    }
    dump_to_json('settings', default_settings)
    return True
