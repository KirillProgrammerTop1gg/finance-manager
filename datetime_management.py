from datetime import datetime, date, timedelta
import time

from_ts_to_str = lambda ts: time.strftime('%d.%m.%Y %H:%M', time.localtime(ts))

def all_month_timestamp():
    today = date.today()
    before = int(datetime.strptime(f'01.{today.month}.{today.year}', '%d.%m.%Y').timestamp())
    after = int((datetime(today.year + (today.month == 12), (today.month % 12) + 1, 1) - timedelta(days=1)).timestamp())
    return before, after

def all_week_timestamp():
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    before = int(datetime.combine(start_of_week, datetime.min.time()).timestamp())
    after = int(datetime.combine(end_of_week, datetime.max.time()).timestamp())
    return before, after


def all_day_timestamp():
    today = date.today()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    before = int(start_of_day.timestamp())
    after = int(end_of_day.timestamp())
    return before, after