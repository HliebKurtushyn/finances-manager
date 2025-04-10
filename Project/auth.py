from hashlib import sha256
from json import dump
from json_funcs import dump_to_json, load_from_json

def check_password(password: str) -> str | bool:
    special_symbols = "@#$%&*!?^~-_+=<>/\\|{}"

    try:
        if len(password) < 8:
            return 'Password is too short!'
        if not any(char.isdigit() for char in password):
            return 'There must be at least one number!'
        if not any(char.isalpha() for char in password):
            return 'There must be at least one letter!'
        if not any(char.islower() for char in password) or not any(char.isupper() for char in password):
            return 'There must be at least one lower and one upper case letter!'
        if not any(char in special_symbols for char in password):
            return 'There must be at least one special symbol!'
    except Exception as e:
        return f'Unexpected error in password validation: {e}'

    return True

def register(username: str, password: str, users: dict) -> bool:
    if username in users:
        print("User already exists!")
        return False

    valid_password = check_password(password)
    if valid_password is True:
        users[username] = sha256(password.encode()).hexdigest()
        dump_to_json('users', users)
        return True
    else:
        print(valid_password)
        return False

def login(users_db: dict) -> bool:
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username not in users_db:
        print("User is not found!")
        return False

    hashed_password = sha256(password.encode()).hexdigest()
    if users_db[username] == hashed_password:
        try:
            with open('data/is_logged.txt', 'w') as file:
                file.write(username)
        except Exception as e:
            print(f"Error updating login status: {e}")
            return False
        return True
    else:
        print("Invalid password!")
        return False

def setup_user_settings():
    user_settings = load_from_json('user_settings')

    def get_or_set_settings(currencies_db: dict):
        nonlocal user_settings

        if not user_settings:
            auto_login = input("Do you want to auto login next time? (0 - Yes | Else - No):\n") == '0'

            print("Please, select your default currency:")
            for currency, rate in currencies_db.items():
                print(f"    {currency}:   {rate} UAH")

            while True:
                default_currency = input()
                if default_currency in currencies_db:
                    break
                else:
                    print("Invalid currency. Please try again:")

            safe_transactions = input(
                "Do you want to make transactions without entering password? (not safe): (0 - Yes | Else - No)\n"
            ) == '0'

            user_settings = {
                'auto_login': auto_login,
                'default_currency': default_currency,
                'transactions_without_password': safe_transactions
            }
            dump_to_json('user_settings', user_settings)

        return user_settings

    return get_or_set_settings
