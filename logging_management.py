import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="finance_app.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_error(msg: str) -> None: logging.error(msg, exc_info=True)
def log_event(msg: str) -> None: logging.debug(msg, exc_info=True)
def log_tx(id:str,amount:float,note:str,categories,time:str) -> None: logging.info(f'Додана нова транзакція. id: {id} кількість: {amount} нотатка: {note} категорії: {categories} час транзакції: {time}', exc_info=True)