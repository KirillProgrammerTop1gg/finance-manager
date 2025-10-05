import uuid
from typing import Optional, Union, Dict, List
import time

txs: Dict[str, Dict[str, Union[int, float, str, List[str]]]] = {}
exchange_rates: Dict[str, float] = {
    'USD': 1,
}
# add tx
def add_tx(balance_change: float, note: str, currency: str = 'USD', categories: Optional[List[str]] = None) -> str:
    id = str(uuid.uuid4())
    if categories == None: categories = []
    categories.append('income' if balance_change > 0 else 'outcome')
    txs[id] = {
        'time': int(time.time()),
        'balance_change': round(balance_change/exchange_rates[currency], 2),
        'note': note,
        'categories': categories
    }
    return id
# edit tx by id with upds
def edit_tx(id: str, **upds) -> str:
    if txs.get(id, None) == None: return 'Транзакція для редагування не знайдена'
    for upd, val in upds.items():
        txs[id][upd] = val
    return 'Транзакція відредагована успішно'
# del tx by id
def del_tx(id: str) -> str:
    if txs.get(id, None) == None: return 'Транзакція для видалення не знайдена'
    txs.pop(id)
    return 'Транзакція видалена успішно'

# overvall sum or sum by category
def sum_txs(txs_list: List[Dict[str, Union[int, float, str, List[str]]]], categories: Optional[List[str]] = None) -> float: return round((txs_list[0]['balance_change'] if (all(category in txs_list[0]['categories'] for category in categories) if categories != None else True) else 0) + sum_txs(txs_list[1:], categories) if len(txs_list) else 0, 2)
# change or add currency with price
def change_currency(currency: str, price: float) -> None: exchange_rates[currency] = price
if __name__ == '__main__':
    change_currency('UAH', 42.3)
    y = add_tx(10, 'Super ', categories=['turtle'])
    x = add_tx(-5, 'Test', categories=['b'])
    x = add_tx(36, 'Test', categories=['turtle', 'b'])
    add_tx(-3500, 'Iphone SE 2', 'UAH', ['binance'])
    print(txs)
    # edit_tx(x, balance_change = -9, note = 'fu')
    # print(txs)
    print(sum_txs(list(txs.values())))
    print(sum_txs(list(txs.values()),['turtle']))
    print(sum_txs(list(txs.values()),['b', 'turtle']))