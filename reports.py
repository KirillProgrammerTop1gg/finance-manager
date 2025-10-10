from finance import txs
from datetime_management import from_ts_to_str
from typing import List, Iterator
import json

def generate_txs_report(ts1: int, ts2: int, categories: List[str] = None) -> Iterator:
    sorted_txs = dict(sorted(txs.items(), key=lambda item: item[1]['time']))
    for tx, data in sorted_txs.items():
        if ts2 >= data['time'] and data['time'] >= ts1 and (True if categories == None else all(category in data['categories'] for category in categories)): yield [tx, data]
    yield 'End', None
    
def create_report(ts1: int, ts2: int, count: int, categories: List[str] = None) -> str:
    generator = generate_txs_report(ts1, ts2, categories)
    result = ''
    for i in range(count):
        tx, data_tx = next(generator)
        if tx == 'End':
            if len(result) == 0: return False
            break
        result += f'''Транзакція {tx}
Дата: {from_ts_to_str(data_tx['time'])}
Змінення балансу у USD: {data_tx['balance_change']}
Нотатка: {data_tx['note']}
Категорії: {''.join([f'\n   - {x}' for x in data_tx['categories']])}\n'''
    result += '\nКінець списку'
    return result

def export_report_to_file(filename: str, info: str) -> None:
    with open(f'{filename}.txt', mode="w") as f:
        f.write(info)