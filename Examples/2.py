users_db = {
    'Gleb': '1234a'
}

def authenticate_user(username: str, password: str) -> tuple[bool, str | object] | bool:
    if username in users_db:
        if users_db[username] == password:
            return True, username
        else:
            print("ERROR: Invalid password")
            return False, None
    else:
        print("ERROR: User not found")
        return False, None

logged_in, username = authenticate_user('Gleb', '1234a')

if logged_in:
    print(f"Welcome, {username}!")
else:
    print("Login failed.")