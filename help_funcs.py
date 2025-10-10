from typing import Optional, Tuple
from datetime import datetime
from logging_management import log_error

def valid_float(placeholder: str) -> float:
    while True:
        try:
            num = float(input(placeholder))
            if num == 0:
                print('Введіть не нульове число')
                log_error('[valid_float] Введено нульове число')
                continue
            return num
        except ValueError:
            print('Введіть не нульове число')
            log_error('[valid_float] Помилка: некоректне число')
        except Exception as e:
            print(f'Невідома помилка: {e}')
            log_error(f'[valid_float] Невідома помилка: {e}')

def valid_int(placeholder: str) -> int:
    while True:
        try:
            num = int(input(placeholder))
            if num <= 0:
                print('Введіть не нульове натуральне число')
                log_error('[valid_int] Введено нульове число')
                continue
            return num
        except ValueError:
            print('Введіть не нульове натуральне число')
            log_error('[valid_int] Помилка: некоректне число')
        except Exception as e:
            print(f'Невідома помилка: {e}')
            log_error(f'[valid_int] Невідома помилка: {e}')

def valid_time(placeholder: str) -> Tuple[str, int]:
    while True:
        try:
            tx_time = input(placeholder)
            tx_timestamp = int(datetime.strptime(tx_time, '%d.%m.%Y %H:%M').timestamp())
            return tx_time, tx_timestamp
        except ValueError:
            print('Введіть дані у правильному форматі!!! 09.10.2025 13:40')
            log_error('[valid_time] Помилка: невірний формат дати/часу')
        except Exception as e:
            print(f'Невідома помилка: {e}')
            log_error(f'[valid_time] Невідома помилка: {e}')

def check_any_obj(condition_result: bool, placeholder: str) -> bool:
    print(placeholder)
    if not condition_result:
        log_error(f'[check_any_obj] Помилка: {placeholder}')
    return condition_result

def leave_mode(action: Optional[int], placeholder: str) -> bool:
    if action == None:
        print(placeholder)
        return True
    return False