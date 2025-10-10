from user_managment import user_login, user_register, users_db
from finance import add_tx, edit_tx, del_txs, change_currency, del_currency, sum_txs, txs, exchange_rates, sum_txs_by_time
from categories import add_category, del_categories, categories, add_tracker, trackers, del_trackers, backup_tracker
from errors import WeakPasswordError
from InquirerPy import inquirer
from InquirerPy.base import Choice
from help_funcs import valid_float, check_any_obj, leave_mode, valid_time, valid_int
from logging_management import log_error, log_event, log_tx
from datetime_management import from_ts_to_str, all_week_timestamp, all_day_timestamp, all_month_timestamp
from reports import create_report, export_report_to_file
import sys, time, json

print('Вас вітає програма по обліку фінансів')

try:
    with open('backup.json', mode='r') as f:
        data = f.read().strip()
        if data:
            backup = json.loads(data)
            users_db.update(backup['users_db'])
            txs.update(backup['txs'])
            exchange_rates.update(backup['exchange_rates'])
            categories.clear()
            categories.extend(backup['categories'])
            for cat, data in backup['trackers'].items():
                backup_tracker(cat, float(data[0]), float(data[1]))
except FileNotFoundError:
    pass
except Exception as e:
    print(f'Виникла невідома помилка при завантажені бекапа: {e}')

isLogin = True
# while True:
#     isLogin = inquirer.select(
#         message="Спочатку залогіньтесь або зареєструйтесь: ",
#         choices=[
#             {'name': 'Логін', 'value': True},
#             {'name': 'Реєстрація', 'value': False},
#             {'name': 'Вихід', 'value': None}
#         ],
#         default=isLogin,
#     ).execute()
#     if isLogin == None:
#         print('Допобачення!')
#         sys.exit()
#     try:
#         login = input('Введіть логін: ')
#         print('Пароль має бути довжиною більше 6 символів, мати велику літеру, спеціальний символ(!@#$%^&*), цифру')
#         password = input('Введіть пароль: ')
#         if user_login(login, password) if isLogin else user_register(login, password): break
#     except WeakPasswordError as e:
#         print(f'Помилка: пароль, {e}')
#     except Exception as e:
#         print(f'Виникла невідома помилка: {e}')

while True:
    mode = inquirer.select(
        message="Оберіть яким модулем ви хочете керувати: ",
        choices=[
            {'name': 'Транзакції', 'value': 0},
            {'name': 'Курси валют', 'value': 1},
            {'name': 'Категорії/трекери', 'value': 2},
            {'name': 'Вихід', 'value': None}
        ],
        default=0,
    ).execute()
    if mode == None:
        with open('backup.json', mode="w") as f:
            f.write(json.dumps({
                'users_db': users_db,
                'txs': txs,
                'exchange_rates': exchange_rates,
                'categories': categories,
                'trackers': {k: trackers[k][3]() for k in trackers}
            }))
        print('Допобачення!')
        sys.exit()
    elif mode == 0:
        while True:
            action = inquirer.select(
                message="Оберіть яку дію ви хочете зробити щодо транзакцій: ",
                choices=[
                    {'name': 'Вивести усі транзакції', 'value': 0},
                    {'name': 'Додати транзакцію', 'value': 1},
                    {'name': 'Змінити транзакцію', 'value': 2},
                    {'name': 'Видалити транзакцію', 'value': 3},
                    {'name': 'Порахувати суму всіх транзакцій', 'value': 4},
                    {'name': 'Порахувати суму транзакцій за категорією', 'value': 5},
                    {'name': 'Порахувати суму транзакцій у межах за часом', 'value': 6},
                    {'name': 'Створити звіт за часом та категоріями', 'value': 7},
                    {'name': 'Вихід', 'value': None}
                ],
                default=0,
            ).execute()
            if leave_mode(action, 'Вихід з модулю транзакцій!'): break
            elif action == 0:
                if check_any_obj(len(txs) == 0, 'Додайте хоча-б одну транзакцію!'): continue
                tx = inquirer.select(
                    message="Оберіть транзакцію для детальнішого просмотру: ",
                    choices=[{'name': f'{id} --- {from_ts_to_str(txs[id]['time'])} - {txs[id]['balance_change']} USD', 'value': id} for id in txs.keys()]+[{'name': 'вихід', 'value': None}],
                    default=list(txs.keys())[0],
                ).execute()
                if tx == None: continue
                print(f'''
Транзакція {tx}
Дата: {from_ts_to_str(txs[tx]['time'])}
Змінення балансу у USD: {txs[tx]['balance_change']}
Нотатка: {txs[tx]['note']}
Категорії: {''.join([f'\n- {x}' for x in txs[tx]['categories']])}
                \n''')
            elif action == 1:
                if check_any_obj(len(categories) == 2, 'Спочатку додайте хоча-б одну категорію!'): continue
                amount = valid_float('К-сть валюти (>0 - якщо дохід, <0 - якщо витрати): ')
                currency = inquirer.select(
                    message="Оберіть валюту транзакції: ",
                    choices=list(exchange_rates.keys()),
                    default='USD',
                ).execute()
                tx_categories = []
                while tx_categories == []:
                    print('Додайте хоча-б одну категорію')
                    tx_categories = inquirer.checkbox(
                        message="Оберіть категорії (пробіл - додати/зняти вибір, ентер - пітвердити): ",
                        choices=list(filter(lambda x: not x in ['дохід', 'витрати'] , categories)),
                        
                    ).execute()
                note = input('Нотатка: ')
                tx_time, tx_timestamp = valid_time('Час транзакції (dd.mm.yyyy hh:mm): ')
                id, am = add_tx(amount, note, currency, tx_categories, tx_timestamp)
                print(f'Транзакція успішно додана з id: {id}, {amount} {currency} = {am} USD у {tx_time}')
                log_tx(id,am,note,tx_categories,tx_time)
            elif action == 2:
                if check_any_obj(len(txs) == 0, 'Додайте хоча-б одну транзакцію!'): continue
                tx = inquirer.select(
                    message="Оберіть транзакцію для подальшої змінги: ",
                    choices=[{'name': f'{id} --- {from_ts_to_str(txs[id]['time'])} - {txs[id]['balance_change']} USD', 'value': id} for id in txs.keys()]+[{'name': 'вихід', 'value': None}],
                    default=list(txs.keys())[0],
                ).execute()
                if tx == None: continue
                upds_act = inquirer.checkbox(
                    message="Оберіть що ви хочете змінити (пробіл - додати/зняти вибір, ентер - пітвердити): ",
                    choices=[
                        {'name': 'к-сть USD', 'value': 0},
                        {'name': 'категорії', 'value': 1},
                        {'name': 'нотатку', 'value': 2},
                        {'name': 'час', 'value': 3}
                    ],
                ).execute()
                for upd in upds_act:
                    if upd == 0:
                        print(f'Зараз к-сть: {txs[tx]['balance_change']} USD')
                        amount = valid_float('К-сть валюти (>0 - якщо дохід, <0 - якщо витрати): ')
                        edit_tx(tx, balance_change = amount)
                    elif upd == 1:
                        new_categories = []
                        print(list(filter(lambda x: not x in ['дохід', 'витрати'] , categories)))
                        print(list(filter(lambda x: not x in ['дохід', 'витрати'] , txs[tx]['categories'])))
                        while new_categories == []:
                            new_categories = inquirer.checkbox(
                                message="Змініть категорії (пробіл - додати/зняти вибір, ентер - пітвердити): ",
                                choices=list(map(lambda x: Choice(x, enabled=True if x in txs[tx]['categories'] else False), filter(lambda x: not x in ['дохід', 'витрати'] , categories))),
                            ).execute()
                        edit_tx(tx, categories=new_categories)
                    elif upd == 2:
                        print(f'Зараз нотатка: {txs[tx]['note']}')
                        new_note = input('Введіть нову нотатку: ')
                        edit_tx(tx, note = new_note)
                    elif upd == 3:
                        print(f'Зараз час: {from_ts_to_str(txs[tx]['time'])}')
                        new_time, new_timestamp = valid_time('Введіть новий час транзакції  (dd.mm.yyyy hh:mm): ')
                        edit_tx(tx, time=new_timestamp)
            elif action == 3:
                if check_any_obj(len(txs) == 0, 'Додайте хоча-б одну транзакцію!'): continue
                txs2del = []
                while txs2del == []:
                    print('Оберіть хоча-б одну транзакцію для видалення')
                    txs2del = inquirer.checkbox(
                        message="Оберіть транзакції для видалення (пробіл - додати/зняти вибір, ентер - пітвердити): ",
                        choices=[{'name': f'{id} - {txs[id]['balance_change']} USD', 'value': id} for id in txs.keys()]+[{'name': 'вихід', 'value': None}],
                        
                    ).execute()
                if not None in txs2del: print(del_txs(txs2del))
            elif action == 7:
                opts = []
                while opts == []:
                    opts = inquirer.checkbox(
                        message="Оберіть за якими даними хотіти зробити звіт (пробіл - додати/зняти вибір, ентер - пітвердити): ",
                        choices=[{'name': 'За часом', 'value': 0}, {'name': 'За категоріями', 'value': 1}]
                    ).execute()
                selected_timestamp_1 = 0
                selected_timestamp_2 = 2114373600
                selected_categories = None
                for opt in opts:
                    if opt:
                        while selected_categories == [] or selected_categories == None:
                            print('Додайте хоча-б одну категорію')
                            selected_categories = inquirer.checkbox(
                                message="Оберіть категорії (пробіл - додати/зняти вибір, ентер - пітвердити): ",
                                choices=categories,
                            ).execute()
                    else:
                        time_assistance_mode = inquirer.select(
                            message='За який період сформувати звіт: ',
                            choices=[
                                {'name': 'Ввести самому', 'value': 0},
                                {'name': 'За цей місяць', 'value': 1},
                                {'name': 'За цей тиждень', 'value': 2},
                                {'name': 'За цей день', 'value': 3},
                                {'name': 'За весь період', 'value': 4},
                            ]
                        ).execute()
                        if time_assistance_mode == 0:
                            while True:
                                selected_time_1, selected_timestamp_1 = valid_time('Рахувати транзакції від (dd.mm.yyyy hh:mm): ')
                                selected_time_2, selected_timestamp_2 = valid_time('Рахувати транзакції до (dd.mm.yyyy hh:mm): ')
                                if selected_timestamp_1 < selected_timestamp_2: break
                                else: print('Час до повинен бути більшим за час від!')
                        elif time_assistance_mode == 1:
                            selected_timestamp_1, selected_timestamp_2 = all_month_timestamp()
                        elif time_assistance_mode == 2:
                            selected_timestamp_1, selected_timestamp_2 = all_week_timestamp()
                        elif time_assistance_mode == 3:
                            selected_timestamp_1, selected_timestamp_2 = all_day_timestamp()
                txs_amount = valid_int('Введіть скільки треба останіх транзакцій показати: ')
                report = create_report(selected_timestamp_1, selected_timestamp_2, txs_amount, selected_categories)
                if not report:
                    print("Нічого не знайдено!")
                    continue
                print(f'\n{report}\n')
                isSave = inquirer.select(
                    message="Хочете зберігти звіт у файл: ",
                    choices=[
                        {'name': 'Так', 'value': True},
                        {'name': 'Ні', 'value': False},
                    ]
                ).execute()
                if isSave:
                    filename = input('Введіть назву файла: ')
                    export_report_to_file(filename, report[:-14])
                    print(f'Файл збережн успішно: {filename}.txt')
            else:
                selected_categories = None
                if action == 5: 
                    while selected_categories == [] or selected_categories == None:
                        print('Додайте хоча-б одну категорію')
                        selected_categories = inquirer.checkbox(
                            message="Оберіть категорії (пробіл - додати/зняти вибір, ентер - пітвердити): ",
                            choices=categories,
                        ).execute()
                elif action == 6:
                    while True:
                        selected_time_1, selected_timestamp_1 = valid_time('Рахувати транзакції від (dd.mm.yyyy hh:mm): ')
                        selected_time_2, selected_timestamp_2 = valid_time('Рахувати транзакції до (dd.mm.yyyy hh:mm): ')
                        if selected_timestamp_1 < selected_timestamp_2: break
                        else: print('Час до повинен бути більшим за час від!')
                if action == 6: sum = sum_txs_by_time(list(txs.values()), selected_timestamp_1, selected_timestamp_2)
                else: sum = sum_txs(list(txs.values()), selected_categories)
                print(f'Сума всіх транзакцій{f' за категоріями' if selected_categories else ''}: {'+' if sum >= 0 else '-'}{sum} USD')
    elif mode == 1:
        while True:
            action = inquirer.select(
                message="Оберіть яку дію ви хочете зробити щодо валют: ",
                choices=[
                    {'name': 'Подивитись усі валюти', 'value': 0},
                    {'name': 'Додати валюту та її курс к USD', 'value': 1},
                    {'name': 'Змінити курс у валюти', 'value': 2},
                    {'name': 'Видалити валюту', 'value': 3},
                    {'name': 'Вихід', 'value': None}
                ],
                default=0,
            ).execute()
            if leave_mode(action, 'Вихід з модулю курсів валют!'): break
            elif action == 0:
                if len(exchange_rates) == 1: print('Нічого дивитись! Додайте валюти!')
                for currency, ex_rate in exchange_rates.items(): print(f'{ex_rate} {currency} = 1 USD') if currency != 'USD' else None
            elif action == 3:
                if check_any_obj(len(exchange_rates) == 1, 'Нічого видаляти! Додайте валюти!'): continue
                currencies = []
                while currencies == []:
                    print('Оберіть хоча-б одну валюту для видалення')
                    currencies = inquirer.checkbox(
                        message="Оберіть валюту: ",
                        choices=list(filter(lambda x: x != 'USD', exchange_rates.keys())),
                    ).execute()
                del_currency(currencies)
                print('Валюта видалена успішно!')
            else:
                if check_any_obj(len(exchange_rates) == 1 and action != 1, 'Нічого замінювати! Додайте валюти!'): continue
                currency = input('Символ нової валюти: ').upper() if action == 1 else inquirer.select(
                    message="Оберіть валюту: ",
                    choices=list(filter(lambda x: x != 'USD', exchange_rates.keys())),
                    default=list(exchange_rates.keys())[0],
                ).execute()
                price = valid_float(f'Введіть курс нової валюти {currency} к USD: ' if action == 1 else f'Введіть новий курс {currency} к USD: ')
                change_currency(currency, price)
                print(f'Валюта {'додана' if action == 1 else 'змінена'} успішно!')
    elif mode == 2:
        while True:
            action = inquirer.select(
                message="Оберіть яку дію ви хочете зробити щодо категорій: ",
                choices=[
                    {'name': 'Подивитись усі категорії', 'value': 0},
                    {'name': 'подивитись усі трекери', 'value': 1},
                    {'name': 'Додати категорію', 'value': 2},
                    {'name': 'Видалити категорії', 'value': 3},
                    {'name': 'Змінити трекер', 'value': 4},
                    {'name': 'Видалити трекери', 'value': 5},
                    {'name': 'Вихід', 'value': None}
                ],
                default=0,
            ).execute()
            if leave_mode(action, 'Вихід з модулю категорії!'): break
            elif action == 0:
                print('\nНаявні категорії:')
                for category in categories:
                    print(f'    - {category}')
                print()
            elif action == 1:
                if check_any_obj(len(trackers) == 0, 'Нічого дивитись! Додайте трекери к категоріям'): continue
                print('\nНаявні трекери бюджету категорій:')
                for tracker in trackers.values():
                    print(f'    -{tracker[1]()}')
                print()
            elif action == 2:
                new_cat = input('Введіть нову категорію: ')
                add_category(new_cat)
                isTracker = inquirer.select(
                    message="Бажаєте додати трекер(ліміт бюджету) до категорії: ",
                    choices=[{'name': 'Так', 'value': True}, {'name': 'Ні', 'value': False}]
                ).execute()
                if isTracker:
                    budget_limit = valid_float(f'Введіть ліміт бюджету у категорії {new_cat} у USD: ')
                    add_tracker(new_cat, budget_limit)
                    print('Трекер додано успішно')
            elif action == 3:
                if check_any_obj(len(categories) == 2, 'Нічого видаляти! Додайте категорії'): continue
                categories2del = inquirer.checkbox(
                    message="Оберіть категорії для видалення (пробіл - додати/зняти вибір, ентер - пітвердити): ",
                    choices=list(filter(lambda x: not x in ['дохід', 'витрати'] , categories)),
                ).execute()
                del_categories(categories2del)
                print('Категорії видалені успішно')
            elif action == 4:
                if check_any_obj(len(trackers) == 0, 'Нічого змінювати! Додайте трекери к категоріям'): continue
                tracker2edit = inquirer.select(
                    message="Оберіть трекер для змінення: ",
                    choices=list(trackers.keys()),
                    default=list(trackers.keys())[0]
                ).execute()
                print(f'Трекер зараз: {trackers[tracker2edit][1]()}')
                new_limit = valid_float('Введіть новий ліміт у USD: ')
                trackers[tracker2edit][2](new_limit)
                print('Трекер змінені успішно')
            elif action == 5:
                if check_any_obj(len(trackers) == 0, 'Нічого видаляти! Додайте трекери к категоріям'): continue
                trackers2del = inquirer.checkbox(
                    message="Оберіть трекери для видалення (пробіл - додати/зняти вибір, ентер - пітвердити): ",
                    choices=list(trackers.keys()),
                ).execute()
                del_trackers(trackers2del)
                print('Трекери видалені успішно')