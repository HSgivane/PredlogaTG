import pytz
from datetime import datetime

def date_today():
    tz = pytz.timezone('Europe/Moscow')
    date = str(datetime.now(tz))
    date = date[8:10]
    return date