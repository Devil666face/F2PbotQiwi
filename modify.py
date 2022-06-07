import pytz
from datetime import datetime
from db import get_admin_id

def get_number_from_str(text):
    try:
        number = [int(number) for number in str.split(text) if number.isdigit()]
        return int(number[0])
    except:
        return int(0)

def add_null(number):
    if len(str(number)) == 1:
        return f'0{str(number)}'
    else:
        return number

def get_time():
    tz = pytz.timezone('Europe/Moscow')
    cur_time = datetime.now(tz)
    return f'{add_null(cur_time.hour)}:{add_null(cur_time.minute)}, {add_null(cur_time.day)}.{add_null(cur_time.month)}.{cur_time.year}'

def flag_admin(id):
    if id == get_admin_id():
        return True
    else:
        return False