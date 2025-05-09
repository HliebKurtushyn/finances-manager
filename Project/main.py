import os
from time import sleep

from json_funcs import set_data_files
from auth import register, login, setup_user_settings
from transactions import transaction
from finances import view_transactions, edit_transaction
from json_funcs import load_from_json, set_currencies, save_session, load_session, clear_session

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    logged = False
    username = ""

    saved_user = load_session()
    if saved_user:
        logged = True
        username = saved_user
        print(f"Auto-logged in as {username}")
        sleep(1)

    while not (logged and username):
        clear()
        print("                     ---Welcome to the Finances Manager App---")
        print("                                    Log in (1)\n")
        print("         Not already in? Sign up! (2)            Exit (3)")
        choice = input("> ")

        if choice == "1":
            clear()
            logged, username = login(users_db)
            if logged and username:
                print(f"Successfully logged in as {username}")
                sleep(1)
        elif choice == "2":
            clear()
            logged, username = register(users_db)
            if logged and username:
                print(f"Successfully registered and logged in as {username}")
                sleep(1)
        elif choice == "3":
            print("Goodbye!")
            sleep(1)
            return
        else:
            print("Invalid input. Please enter 1, 2, or 3.")
            sleep(1)

    # User settings setup
    get_user_settings = setup_user_settings()
    users_card, users_iban = get_user_settings(currencies_db, users_details_db, transactions_db, balances_db, username)

    # Main menu loop
    while logged and username:
        clear()
        print(f"Welcome, {username}!")
        print(f"Your balance: {balances_db.get(users_card, 0)} EUR")
        print("\nMain Menu:")
        print("1 - Make a transaction")
        print("2 - View transactions")
        print("3 - Edit a transaction")
        print("4 - Log out")
        print("5 - Exit")
        choice = input("> ")

        if choice == "1":
            transaction(
                currencies_db, users_db, balances_db, users_card, username, logged,
                user_settings.get("transactions_without_password", False),
                user_settings.get("default_currency", "EUR"),
                users_details_db, transactions_db
            )
        elif choice == "2":
            view_transactions(transactions_db, username, "incoming")
            view_transactions(transactions_db, username, "outgoing")
            input("\nPress Enter to return to the main menu...")
        elif choice == "3":
            edit_transaction(transactions_db, username)
        elif choice == "4":
            clear_session()
            logged = False
            username = ""
            print("Logged out successfully!")
            sleep(1)
        elif choice == "5":
            print("Goodbye!")
            sleep(1)
            return
        else:
            print("Invalid input. Please enter a valid option.")
            sleep(1)


if __name__ == "__main__":
    set_data_files()
    set_currencies()

    users_db = load_from_json('users')
    balances_db = load_from_json('balances')
    transactions_db = load_from_json('transactions')
    currencies_db = load_from_json("currencies")
    users_details_db = load_from_json('users_details')
    user_settings = load_from_json('user_settings')

    main()
