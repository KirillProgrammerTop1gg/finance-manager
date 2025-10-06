from typing import Optional, Union, Dict, List

def valid_float(placeholder: str) -> float:
    num = 0
    while num == 0:
        try:
            num = float(input(placeholder))
        except ValueError:
            print('Введіть не нульове число')
    return num

def check_any_obj(condition_result: bool, placeholder: str) -> bool:
    print(placeholder)
    return condition_result

def leave_mode(action: Optional[int], placeholder: str) -> bool:
    if action == None:
        print(placeholder)
        return True
    return False