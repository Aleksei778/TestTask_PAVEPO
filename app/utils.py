import pytz
from datetime import datetime as dt

def moscow_time():
    return dt.now(pytz.timezone('Europe/Moscow'))