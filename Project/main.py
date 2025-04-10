import os
from auth import register, login, setup_user_settings
from transactions import transaction
from finances import view_transactions, edit_transaction
from json_funcs import load_from_json, set_currencies


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    set_currencies()
    users_db = load_from_json('users')
    balances_db = load_from_json('balances')
    transactions_db = load_from_json('transactions')
    currencies_db = load_from_json("currencies")
    users_details_db = load_from_json('users_details')

    print("Welcome to the Finance Management System!")
    while True:
        print("\nMain Menu:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            while True:
                print("\n\n0 - Back\n")
                username = input("Enter a username: ")
                password = input("Enter a password: ")
                if username == "0" or password == "0":
                    break
                if register(username, password, users_db):
                    print("Registration successful!")
                    break

        elif choice == "2":
            if login(users_db):
                print("Login successful!")
                user_settings = setup_user_settings()(currencies_db)
                username = input("Enter your username again to proceed: ")
                user_card = input("Enter your card number: ")

                while True:
                    print("\nUser Menu:")
                    print("1. Make a Transaction")
                    print("2. View Transactions")
                    print("3. Edit Transactions")
                    print("4. Logout")
                    user_choice = input("Enter your choice: ")

                    if user_choice == "1":
                        transaction(
                            currencies_db, users_db, balances_db,
                            user_card, username, True,
                            user_settings.get('transactions_without_password', False),
                            user_settings.get('default_currency', 'EUR'),
                            users_details_db, transactions_db
                        )
                    elif user_choice == "2":
                        transaction_type = input("Enter transaction type (incoming/outgoing): ")
                        view_transactions(transactions_db, username, transaction_type)
                    elif user_choice == "3":
                        edit_transaction(transactions_db, username)
                    elif user_choice == "4":
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Login failed!")

        elif choice == "3":
            print("Exiting the system. Goodbye!")
            break  # Exit the main loop

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()



# Зупинився на тому що хочу щробити щоб воно робило users_details для транзакцій і кращий інтерфейс