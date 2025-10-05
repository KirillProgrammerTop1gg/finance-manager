import hashlib

users_db = {}

hash_password = lambda password: hashlib.sha256(password.encode()).hexdigest()

def user_register(username, password):
    # Додаємо первинні перевірки паролю
    if username in users_db:
        print(f"Логін вже зайнятий")
    else:
        users_db[username] = hash_password(password)
        
def user_login(username, password):
    # Додаємо первинні перевірки паролю
    if username not in users_db:
        print(f"Логіну не існує")
    elif users_db[username] == hash_password(password):
        print(f"Привіт, {username}!")
        return True
    else:
        print("Невірний логін або пароль.")
    return False