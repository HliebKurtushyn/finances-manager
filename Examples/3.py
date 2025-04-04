transactions = {}

def add_transaction(transaction_id, amount, date, category, *delete):
    if transaction_id in transactions:
        print("Транзакція з таким ID вже існує.")

        if delete:
            choice = input("Бажаєте видалити? Так/ні").lower()
            if choice == 'так':
                del transactions[transaction_id]
            else:
                print('Готово.')
    else:
        transactions[transaction_id] = {
            'amount': amount,
            'date': date,
            'category': category
        }
        print(f"Транзакція {transaction_id} успішно додана.")

add_transaction(233,8000,"20/03/2025","Електроніка")
print(transactions)

add_transaction(233,8000,"20/03/2025","Електроніка", True)
print(transactions)
