import uuid
from typing import Optional, Union, Dict, List
import time

transactions: Dict[str, Dict[str, Union[int, float, str, List[str]]]] = {}
currencies: Dict[str, float] = {}

def add_transaction(balance_change: float, note: str, currency: str = 'USD', categories: Optional[List[str]] = None) -> str:
    id = str(uuid.uuid4())
    if categories == None: categories = []
    categories.append('income' if balance_change > 0 else 'outcome')
    transactions[id] = {
        'time': int(time.time()),
        'balance_change': balance_change,
        'note': note,
        'categories': categories
    }
    return id
    
def edit_transaction(id: str, **upds) -> None:
    for upd, val in upds.items():
        transactions[id][upd] = val
        
def del_transaction(id: str) -> Optional[str]:
    if transactions.get(id, None) == None: return 'Invalid id'
    transactions.pop(id)
    
def sum_txs(txs_list: List[Dict[str, Union[int, float, str, List[str]]]], category: Optional[List[str]] = None) -> float: return (txs_list[0]['balance_change'] if (category in txs_list[0]['categories'] or category == None) else 0) + sum_txs(txs_list[1:], category) if len(txs_list) else 0
    
y = add_transaction(10, 'Super ', categories=['turtle'])
x = add_transaction(-5, 'Test', categories=['b'])
x = add_transaction(36, 'Test', categories=['turtle', 'b'])
print(transactions)
# edit_transaction(x, balance_change = -9, note = 'fu')
# print(transactions)
print(sum_txs(list(transactions.values())))
print(sum_txs(list(transactions.values()),'b'))