def add_budget_tracker(category: str, limit: float):
    spent = 0
    def tracker(qty: float) -> None:
        nonlocal spent
        spent += qty
        print(f'Ви перевисели бюджет у категорії {category} {spent}/{limit}' if spent > limit else f'Бюджет категорії {category} - {spent}/{limit}')
    return tracker