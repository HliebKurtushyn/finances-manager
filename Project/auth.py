from hashlib import sha256
from json import dump
from json_funcs import dump_to_json, load_from_json, save_session
from random import randint

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

def register(users: dict) -> bool and str:
    if users is None:
        users = {}

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username in users:
        print("User already exists!")
        return False, None

    valid_password = check_password(password)
    if valid_password is True:
        users[username] = sha256(password.encode()).hexdigest()
        dump_to_json('users', users)
        return True, username
    else:
        print(valid_password)
        return False, None

def login(users_db: dict) -> bool and str:
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username not in users_db:
        print("User is not found!")
        return False, None

    hashed_password = sha256(password.encode()).hexdigest()
    if users_db[username] == hashed_password:
        return True, username
    else:
        print("Invalid password!")
        return False, None

from random import randint

def setup_user_settings():
    user_settings = load_from_json('user_settings')

    def get_or_set_settings(currencies_db: dict, users_details_db: dict, transactions_db: dict, balances_db: dict, username: str):
        nonlocal user_settings

        users_details_db.setdefault('credit_cards', {})
        users_details_db.setdefault('ibans', {})
        transactions_db.setdefault(username, {"incoming": {}, "outgoing": {}})

        # Перевірка, чи користувач вже має картку та IBAN
        existing_card = next((card for card, user in users_details_db['credit_cards'].items() if user == username), None)
        existing_iban = next((iban for iban, user in users_details_db['ibans'].items() if user == username), None)

        # Якщо юзер ще не налаштований — налаштовуємо
        if not user_settings or not existing_card or not existing_iban:
            print("Settings setup\n\n")

            auto_login = input("\nDo you want to auto login next time? (0 - Yes | Else - No):\n") == '0'

            print("Please, select your default currency:")
            for currency, rate in currencies_db.items():
                print(f"    {currency}:   {rate} EUR")

            while True:
                default_currency = input("> ")
                if default_currency in currencies_db:
                    break
                print("Invalid currency. Please try again:")

            safe_transactions = input("\nDo you want to make transactions without entering password? (not safe): (0 - Yes | Else - No)\n") == '0'

            user_settings = {
                'auto_login': auto_login,
                'default_currency': default_currency,
                'transactions_without_password': safe_transactions
            }

            supported_ibans = {
                "AT": 20, "BE": 16, "BG": 22, "CY": 28, "CZ": 24,
                "DE": 22, "DK": 18, "EE": 20, "ES": 24, "FI": 18,
                "UA": 29
            }

            while True:
                users_country = input(f"\nEnter an IBAN country code from supported list:\n{', '.join(supported_ibans.keys())}\n> ")
                if users_country in supported_ibans:
                    break
                print("Invalid IBAN code!")

            # Генерація нових картки та IBAN, якщо ще нема
            if not existing_card:
                existing_card = f"4{randint(10**14, 10**15 - 1)}"
                users_details_db['credit_cards'][existing_card] = username
                balances_db.setdefault(existing_card, "0")

            if not existing_iban:
                existing_iban = f"{users_country}{randint(10**18, 10**19 - 1)}"
                users_details_db['ibans'][existing_iban] = username

            if auto_login:
                save_session(username)

            dump_to_json('users_details', users_details_db)
            dump_to_json('transactions', transactions_db)
            dump_to_json('balances', balances_db)
            dump_to_json('user_settings', user_settings)

        return existing_card, existing_iban

    return get_or_set_settings

