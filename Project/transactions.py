from hashlib import sha256
from json_funcs import dump_to_json
from finances import add_transaction

def check_login(logged: bool) -> bool: # Tested
    return logged

def request_password(username: str, users_db: dict, logged: bool) -> bool: # Tested
    if not check_login(logged):
        return False

    password = input("Enter your password: ")
    password = sha256(password.encode()).hexdigest()

    return users_db.get(username) == password

def transfer_to_users_currency(currencies_db: dict, balances_db: dict, users_card: str, users_currency: str) -> str: # Tested
    users_balance = balances_db.get(users_card, 0)
    if users_currency == "EUR":
        return f"{users_balance:.2f}"
    currency_rate = currencies_db.get(users_currency, 1)
    return f"{users_balance / currency_rate:.2f}"

def transaction(currencies_db: dict, users_db: dict, balances_db: dict, users_card: str, username: str, logged: bool, safe_transactions: bool, users_currency: str, users_details_db: dict, transactions_db: dict) -> bool:
    if not check_login(logged):
        return False

    while True:
        transaction_type = input("What type of transaction do you want to make?\n1 - Transfer to card\n2 - IBAN\n")
        if transaction_type in ("1", "2"):
            break

    receiver_card = None
    receiver_username = None

    if transaction_type == "1":
        while True:
            receiver_card = input("Enter the recipient's card number: ").replace(" ", "")
            if not receiver_card.isdigit() or not 12 <= len(receiver_card) <= 19:
                print("Invalid card number!")
                continue
            if receiver_card not in balances_db:
                print("Receiver not found!")
                continue

            receiver_username = users_details_db.get('credit_cards', {}).get(receiver_card)
            if not receiver_username:
                print("Receiver username not found!")
                continue
            print(f"User found: {receiver_username}")
            break

    else:
        supported_ibans = {
            "AT": 20, "BE": 16, "BG": 22, "CY": 28, "CZ": 24,
            "DE": 22, "DK": 18, "EE": 20, "ES": 24, "FI": 18,
            "UA": 29
        }
        while True:
            receiver = input("Enter recipient's IBAN: ").replace(" ", "")

            if not receiver.startswith(tuple(supported_ibans.keys())):
                print("Invalid IBAN!")
                continue
            if receiver not in users_details_db.get("ibans", {}):
                print("Receiver not found! (In users_details)")
                continue

            receiver_username = users_details_db["ibans"][receiver]
            receiver_card = {v: k for k, v in users_details_db.get("credit_cards", {}).items()}.get(receiver_username)

            if not receiver_card or receiver_card not in balances_db:
                print("Receiver not found! (In balances)")
                continue

            print(f"User found: {receiver_username}")
            break

    while True:
        try:
            user_balance = balances_db.get(users_card, 0)
            display_balance = transfer_to_users_currency(currencies_db, balances_db, users_card, users_currency)
            print(f"\nYour balance: {display_balance} {users_currency}")

            prompt = f"Enter amount you want to transfer: (Between 1 and 50.000 {users_currency})\n"
            amount = float(input(prompt))

            if not 1 <= amount <= 50000:
                print(f"Amount must be between 1 and 50.000 {users_currency}!")
                continue

            if users_currency != "EUR":
                amount *= currencies_db.get(users_currency, 1)

            if user_balance < amount:
                print("Insufficient funds!")
                continue
        except ValueError:
            print("Invalid amount!")
        else:
            break

    if not safe_transactions:
        count = 0
        while count < 5:
            if request_password(username, users_db, logged):
                break
            print("Invalid password!")
            count += 1
        else:
            print("Too many requests! Try again later!")
            return False

    balances_db[users_card] = balances_db.get(users_card, 0) - amount
    balances_db[receiver_card] = balances_db.get(receiver_card, 0) + amount

    add_category = True if input("Do you want to add a category to this transaction?\n 1 - Yes\n Else - No\n") == 1 else False
    if add_category:
        category = input("Enter a name of category you want to add: ")
        add_transaction(transactions_db, username, receiver_username, amount, category)
    else:
        add_transaction(transactions_db, username, receiver_username, amount)

    dump_to_json('balances', balances_db)
    dump_to_json('transactions', transactions_db)

    print(f"Transaction successful! You sent {amount:.2f} EUR to {receiver_card}")
    return True