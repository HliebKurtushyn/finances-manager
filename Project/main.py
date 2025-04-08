from subprocess import run
from json_funcs import dump_to_json, load_from_json, create_settings, restore_settings
from auth import register, login
from transactions import transaction
from finances import view_transactions, edit_transaction

currencies_db = load_from_json('currencies')
users_db = load_from_json('users')
balances_db = load_from_json('balances')
users_card = "1234567890123456"
username = 'gleb'
logged = True
safe_transactions = True
users_currency = 'EUR'
users_details_db = load_from_json('users_details')
transactions_db = load_from_json('transactions')

transaction(currencies_db, users_db, balances_db, users_card, username, logged, safe_transactions, users_currency, users_details_db, transactions_db)