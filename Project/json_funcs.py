from json import dump, load
from os import makedirs
from os.path import exists

def dump_to_json(file_name: str, obj: object) -> bool:
    folder = 'data'
    path_to_file = f'{folder}/{file_name}.json'

    makedirs(folder, exist_ok=True)

    with open(path_to_file, "w", encoding="utf-8") as file:
        dump(obj, file, indent=3)
        return True

def load_from_json(file_name: str) -> dict:
    folder = 'data'
    path_to_file = f'{folder}/{file_name}.json'

    makedirs(folder, exist_ok=True)

    if not exists(path_to_file):
        return {}

    with open(path_to_file, "r", encoding="utf-8") as file:
        content = file.read().strip()
        if not content:
            return {}
        return load(open(path_to_file, "r", encoding="utf-8"))

def create_settings() -> bool:
    path_to_file = 'data/settings.json'
    default_settings = {
        "default_currency": "EUR",
    }

    makedirs('data', exist_ok=True)

    if not exists(path_to_file):
        dump_to_json('settings', default_settings)

    _ = load_from_json('settings')
    return True

def restore_settings() -> bool:
    default_settings = {
        "default_currency": "EUR",
    }
    dump_to_json('settings', default_settings)
    return True

def set_currencies():
    currencies = {
      "EUR": 1,
      "UAH": 0.0225,
      "USD": 0.917,
      "PLN": 0.232,
      "GBP": 1.163,
      "CZK": 0.0396
    }

    dump_to_json("currencies", currencies)


def set_currencies():
    currencies = {
      "EUR": 1,
      "UAH": 0.0225,
      "USD": 0.917,
      "PLN": 0.232,
      "GBP": 1.163,
      "CZK": 0.0396
    }

    dump_to_json("currencies", currencies)

