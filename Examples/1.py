import hashlib
users_db = {}
def hash_password (password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def register_user(username, password):
    if username in users_db:
        print("Цей логін уже використовується. Оберіть інший.")
    else:
        users_db [username] = hash_password (password)
        print("Користувача {username} успішно зареєстровано.")
