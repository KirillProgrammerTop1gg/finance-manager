import uuid
from typing import Optional, Union, Dict, List
import time
from categories import trackers

txs: Dict[str, Dict[str, Union[int, float, str, List[str]]]] = {}
exchange_rates: Dict[str, float] = {
    "USD": 1,
}


# add tx
def add_tx(
    balance_change: float,
    note: str,
    currency: str = "USD",
    categories: Optional[List[str]] = None,
    tx_time: int = int(time.time()),
) -> str:
    id = str(uuid.uuid4())
    if categories == None:
        categories = []
    amount = round(balance_change / exchange_rates[currency], 2)
    categories.append("дохід" if balance_change > 0 else "витрати")
    txs[id] = {
        "time": tx_time,
        "balance_change": amount,
        "note": note,
        "categories": categories,
    }
    for category in categories:
        if trackers.get(category, None) != None:
            trackers[category][0](amount)
    return id, amount


# edit tx by id with upds
def edit_tx(id: str, **upds) -> str:
    if txs.get(id, None) == None:
        return "Транзакція для редагування не знайдена"
    for upd, val in upds.items():
        txs[id][upd] = val
    return "Транзакція відредагована успішно"


# del tx by id
def del_txs(ids: str) -> str:
    for id in ids:
        if txs.get(id, None) == None:
            return f"Транзакція {id} для видалення не знайдена"
        txs.pop(id)
    return "Транзакції видалена успішно"


# overvall sum or sum by category
def sum_txs(
    txs_list: List[Dict[str, Union[int, float, str, List[str]]]],
    categories: Optional[List[str]] = None,
) -> float:
    return round(
        (
            (
                txs_list[0]["balance_change"]
                if (
                    all(
                        category in txs_list[0]["categories"] for category in categories
                    )
                    if categories != None
                    else True
                )
                else 0
            )
            + sum_txs(txs_list[1:], categories)
            if len(txs_list)
            else 0
        ),
        2,
    )


def sum_txs_by_time(
    txs_list: List[Dict[str, Union[int, float, str, List[str]]]], ts1: int, ts2: int
) -> float:
    return round(
        (
            (
                txs_list[0]["balance_change"]
                if int(ts2) >= int(txs_list[0]["time"])
                and int(txs_list[0]["time"]) >= int(ts1)
                else 0
            )
            + sum_txs_by_time(txs_list[1:], ts1, ts2)
            if len(txs_list)
            else 0
        ),
        2,
    )


# change or add currency with price
def change_currency(currency: str, price: float) -> None:
    exchange_rates[currency] = price


# del currency
def del_currency(currencies: str) -> str:
    for currency in currencies:
        if exchange_rates.get(currency, None) == None:
            return f"Валюта {currency} для видалення не знайдена"
        exchange_rates.pop(currency)
    return "Валюта видалена успішно"
