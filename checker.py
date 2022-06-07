import sqlite3, schedule
from datetime import timedelta,datetime
from threading import Thread

def check(id, deact_date, DB):
    date_now = f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year}'
    print(date_now,deact_date)
    if date_now==deact_date:
        update_query = f"UPDATE users SET sub = 0, deactDate = '0' WHERE id={id}"
        cursor = DB.cursor()
        cursor.execute(update_query)
        DB.commit()
        #print(f"Деактивирую подписку {id}")
    else:
        pass
        #print(f"У {id} подписка пока ативна")

def сycle_chech():
    with sqlite3.connect('database.db') as DB:
        select_query = f"SELECT id, deactDate FROM users"
        cursor = DB.cursor()
        cursor.execute(select_query)
        DB.commit()
        for line in cursor:
            if line[1]!=str(0):
                check(line[0],line[1], DB)

def new_thread():
    schedule.every(1).seconds.do(сycle_chech)
    #schedule.every(6).hours.do(сycle_chech)
    while True:
        schedule.run_pending()

def create_and_start_thread():
    thread = Thread(target=new_thread)
    return thread

def main_core_check():
    thr = create_and_start_thread()
    thr.start()