
def save_transactions(*args):
    ...

def add_transaction(categories_db, category, sender_username, amount, transactions_db):
    if categories_db and category:
        if category not in categories_db.get(sender_username, {}):
            categories_db[sender_username][category] = {"budget": None, "summary": 0}
        categories_db[sender_username][category]["summary"] += amount
        save_transactions(transactions_db, categories_db, amount)
    else:
        save_transactions(transactions_db)