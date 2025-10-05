from user_managment import user_login, user_register
from finance import add_tx, edit_tx, del_tx, change_currency, sum_txs
from budget import add_budget_tracker
from errors import WeakPasswordError
from InquirerPy import inquirer

# user_register(input('Log: '), input('Pass: '))
# user_login(input('Log: '), input('Pass: '))

print('Вас вітає програма по обліку фінансів')
isLogin = inquirer.select(
    message="Спочатку залогіньтесь або зареєструйтесь: ",
    choices=[{'name': 'Логін', 'value': True}, {'name': 'Реєстрація', 'value': False}],
    default="Нет",
    pointer="👉",
).execute()
while True:
    try:
        login = input('Введіть логін: ')
        print('Пароль має бути довжиною більше 9 символів, мати велику літеру, спеціальний символ(!@#$%^&*), цифру')
        password = input('Введіть пароль: ')
        if user_login(login, password) if isLogin else user_register(login, password): break
    except WeakPasswordError as e:
        print(f'Помилка: пароль, {e}')
    except Exception as e:
        print(f'Виникла невідома помилка: {e}')

print('Вітаємо у системі!')