import datetime
from json_funcs import dump_to_json, load_from_json
from random import randint

def load_transactions(): # Tested
    try:
        load_from_json('transactions')
    except FileNotFoundError:
        return {}

def save_transactions(transactions_db: dict): # Tested
    dump_to_json('transactions', transactions_db)

def generate_transaction_id(transactions_db: dict, receiver_username: str) -> int: # Tested
    while True:
        transaction_id = randint(1, 100000)
        if transaction_id not in transactions_db.get(receiver_username, {}).get("incoming", {}):
            return transaction_id

def add_transaction(transactions_db: dict, sender_username: str, receiver_username: str, amount: float, *category: str) -> int: # Tested
    transaction_id = generate_transaction_id(transactions_db, receiver_username)

    if not category: category = "N/A"

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transaction_data = {
        "sender": sender_username,
        "receiver": receiver_username,
        "amount": amount,
        "category": category,
        "date": current_time
    }

    if sender_username not in transactions_db:
        transactions_db[sender_username] = {"incoming": {}, "outgoing": {}}
    if receiver_username not in transactions_db:
        transactions_db[receiver_username] = {"incoming": {}, "outgoing": {}}

    transactions_db[sender_username]["outgoing"][transaction_id] = transaction_data
    transactions_db[receiver_username]["incoming"][transaction_id] = transaction_data

    save_transactions(transactions_db)
    return transaction_id

def see_transactions_list(transactions_db: dict, username: str) -> str or None: # Tested
    while True:
        transaction_type_input = input("Incoming - 0\nOutgoing - 1\n ").strip()

        if transaction_type_input == "0":
            transaction_type = "incoming"
            break
        elif transaction_type_input == "1":
            transaction_type = "outgoing"
            break
        else:
            print("Invalid input. Please enter 0 for incoming or 1 for outgoing.")

    user_transactions = transactions_db.get(username, {})
    if user_transactions == {}:
        print("User not found or no transactions available.")
        return

    transactions_data = user_transactions.get(transaction_type, {})

    if transactions_data == {}:
        print(f"No {transaction_type} transactions found.")
        return

    result = [f"\n{transaction_type.title()} transactions for {username}:\n"]
    for tid, details in transactions_data.items():
        sender = details.get("sender", "N/A")
        receiver = details.get("receiver", "N/A")
        amount = details.get("amount", "N/A")
        category = details.get("category", "N/A")
        date = details.get("date", "N/A")
        result.append(f"ID: {tid} | Sender: {sender} | Receiver: {receiver} | Amount: {amount:.2f} EUR | Category: {category} | Date: {date}")

    print("\n".join(result))
    return