from typing import Callable, List, Tuple

categories: List[str] = ["дохід", "витрати"]
trackers = {}


def add_category(category: str) -> None:
    categories.append(category)


def del_categories(categories2del: List[str]) -> None:
    for category in categories2del:
        categories.remove(category)


def budget_tracker(category: str, limit: float, spent: float = 0) -> List[Callable]:
    spent = spent
    limit = limit

    def create_tracker(qty: float) -> None:
        nonlocal spent
        spent += qty
        print(
            f"Ви перевисели бюджет у категорії {category} {spent}/{limit} USD"
            if spent > limit
            else f"Бюджет категорії {category} - {spent}/{limit} USD"
        )

    def get_tracker() -> str:
        nonlocal spent
        return f"Бюджет у категорії {category}{' перевищино' if spent > limit else ', ще не перевищино'} {spent}/{limit} USD"

    def update_tracker(new_limit: float) -> None:
        nonlocal limit
        limit = new_limit

    def save_tracker() -> List[float]:
        return [limit, spent]

    return [create_tracker, get_tracker, update_tracker, save_tracker]


def add_tracker(category: str, limit: float) -> None:
    trackers[category] = budget_tracker(category, limit)


def backup_tracker(category: str, limit: float, spent: float = 0) -> None:
    trackers[category] = budget_tracker(category, limit, spent)


def del_trackers(trackers2del: List[str]) -> None:
    for tracker in trackers2del:
        trackers.pop(tracker)
