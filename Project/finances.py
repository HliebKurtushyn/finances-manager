import datetime
from json_funcs import dump_to_json
from random import randint

def save_transactions(transactions_db: dict):
    dump_to_json('transactions', transactions_db)

def generate_transaction_id(transactions_db: dict, receiver_username: str) -> int:
    while True:
        transaction_id = randint(1, 100_000)
        if transaction_id not in transactions_db.get(receiver_username, {}).get("incoming", {}):
            return transaction_id

def add_transaction(transactions_db: dict, sender_username: str, receiver_username: str, amount: float, category="N/A") -> int:
    transaction_id = generate_transaction_id(transactions_db, receiver_username)

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transaction_data = {
        "sender": sender_username,
        "receiver": receiver_username,
        "amount": amount,
        "category": category,
        "date": current_time
    }

    for user in (sender_username, receiver_username):
        if user not in transactions_db:
            transactions_db[user] = {"incoming": {}, "outgoing": {}}

    transactions_db[sender_username]["outgoing"][transaction_id] = transaction_data
    transactions_db[receiver_username]["incoming"][transaction_id] = transaction_data

    save_transactions(transactions_db)
    return transaction_id

def view_transactions(transactions_db: dict, username: str, transaction_type: str) -> str | None:
    user_transactions = transactions_db.get(username)
    if not user_transactions:
        print("User not found or no transactions available.")
        return

    transactions_data = user_transactions.get(transaction_type, {})
    if not transactions_data:
        print(f"No {transaction_type} transactions found.")
        return

    result = [f"\n{transaction_type.title()} transactions for {username}:\n"]
    for tid, details in transactions_data.items():
        sender = details.get("sender", "N/A")
        receiver = details.get("receiver", "N/A")
        amount = details.get("amount", 0.0)
        category = details.get("category", "N/A")
        date = details.get("date", "N/A")

        result.append(
            f"ID: {tid} | Sender: {sender} | Receiver: {receiver} | "
            f"Amount: {amount:.2f} EUR | Category: {category} | Date: {date}"
        )

    print("\n".join(result))
    return

def edit_transaction(transactions_db: dict, username: str):
    view_transactions(transactions_db, username, 'incoming')
    view_transactions(transactions_db, username, 'outgoing')

    tid = input("\nEnter transaction ID you want to edit (0 to exit):\n")
    if tid == "0":
        print("Exit...")
        return

    try:
        tid = int(tid)
    except ValueError:
        print("Transaction ID must be a number.")
        return

    transaction_type = None
    if tid in transactions_db.get(username, {}).get("incoming", {}):
        transaction_type = "incoming"
    elif tid in transactions_db.get(username, {}).get("outgoing", {}):
        transaction_type = "outgoing"
    else:
        print(f"No transaction with ID {tid} found.")
        return

    transaction = transactions_db[username][transaction_type][tid]

    print("\nEnter new values. If you want to leave a field unchanged, just press Enter.")
    sender = input(f"Sender [{transaction.get('sender', '')}]: ").strip()
    receiver = input(f"Receiver [{transaction.get('receiver', '')}]: ").strip()
    category = input(f"Category [{transaction.get('category', '')}]: ").strip()
    date = input(f"Date [{transaction.get('date', '')}]: ").strip()

    if sender:
        transaction["sender"] = sender
    if receiver:
        transaction["receiver"] = receiver
    if category:
        transaction["category"] = category
    if date:
        transaction["date"] = date

    save_transactions(transactions_db)
    print("\nTransaction updated successfully!")
