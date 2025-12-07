import hashlib
from errors import WeakPasswordError

users_db = {}

hash_password = lambda password: hashlib.sha256(password.encode()).hexdigest()


def check_password(psw: str):
    if not len(psw) >= 7:
        raise WeakPasswordError("пароль закороткий (< 7 символів)")
    if not any(map(lambda x: x.isdigit(), psw)):
        raise WeakPasswordError("немає цифр")
    if not any(map(lambda x: x in "!@#$%^&*", psw)):
        raise WeakPasswordError("немає спеціальних символів(!@#$%^&*)")
    if not any(map(lambda x: x.isupper(), psw)):
        raise WeakPasswordError("немає великих літер")


def user_register(username: str, password: str) -> bool:
    # Додаємо первинні перевірки паролю
    check_password(password)
    if username in users_db:
        print(f"Логін вже зайнятий")
    else:
        users_db[username] = hash_password(password)
        return True
    return False


def user_login(username: str, password: str) -> bool:
    # Додаємо первинні перевірки паролю
    if username not in users_db:
        print(f"Логіну не існує")
    elif users_db[username] == hash_password(password):
        print(f"Привіт, {username}!")
        return True
    else:
        print("Невірний логін або пароль.")
    return False
