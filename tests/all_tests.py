from user_managment import user_login, user_register

assert user_register("test", "Test34$") == True, "Не реєструє користувача"
assert user_register("test", "Test35$") == False, "Не перевіряє наявність логінів у бд"
assert user_login("test", "Test35$") == False, "Не перевіряє пароль"
assert user_login("est", "Test34$") == False, "Не перевіряє наявність користувача у бд"
assert user_login("test", "Test34$") == True, "Не логінізує користувача"

print("Тести логіна пройдено успішно!")

from datetime_management import (
    from_ts_to_str,
    all_month_timestamp,
    all_day_timestamp,
    all_week_timestamp,
)

day_before, day_after = all_day_timestamp()
assert type(day_before) == int, "all_day_timestamp: before не int"
assert type(day_after) == int, "all_day_timestamp: after не int"
assert day_before <= day_after, "all_day_timestamp: before > after"

week_before, week_after = all_week_timestamp()
assert type(week_before) == int, "all_week_timestamp: before не int"
assert type(week_after) == int, "all_week_timestamp: after не int"
assert week_before <= week_after, "all_week_timestamp: before > after"

month_before, month_after = all_month_timestamp()
assert type(month_before) == int, "all_month_timestamp: before не int"
assert type(month_after) == int, "all_month_timestamp: after не int"
assert month_before <= month_after, "all_month_timestamp: before > after"

print("Тести з часом пройдені")
