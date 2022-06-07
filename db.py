import sqlite3
from datetime import timedelta,datetime

def get_bus_numbers():
    bus_number_list = []
    with sqlite3.connect('database.db') as DB:
        select_query = f"SELECT number FROM bus;"
        cursor = DB.cursor()
        cursor.execute(select_query)
        DB.commit()
        for bus_number in cursor:
            bus_number_list.append(int(bus_number[0]))
    bus_number_list.sort()
    return bus_number_list

def get_bus_name(number):
    with sqlite3.connect('database.db') as DB:
        select_query = f"SELECT name FROM bus WHERE number={number};"
        cursor = DB.cursor()
        cursor.execute(select_query)
        DB.commit()
        for name in cursor:
            return name[0]

def get_bus_stations(number):
    station_list = []
    with sqlite3.connect('database.db') as DB:
        select_query = f"SELECT station FROM bus{number};"
        cursor = DB.cursor()
        cursor.execute(select_query)
        DB.commit()
        for station in cursor:
            station_list.append(station[0])
    return station_list

def create_user(id,username,name):
    with sqlite3.connect('database.db') as DB:
        try:
            insert_query = f"INSERT INTO users (id, username, name, active, sub, deactDate) VALUES ({id},'{username}','{name}', 1, 0, 0)"
            cursor = DB.cursor()
            cursor.execute(insert_query)
            DB.commit()
        except:
            print(f'Пользователь {id} уже создан, задаю активность = 1')
            update_query = f"UPDATE users SET active = 1 WHERE id={id}"
            cursor = DB.cursor()
            cursor.execute(update_query)
            DB.commit()

def get_active_users_list():
    user_list = []
    with sqlite3.connect('database.db') as DB:
        select_query = f"SELECT id FROM users WHERE active = 1"
        cursor = DB.cursor()
        cursor.execute(select_query)
        DB.commit()
        for user in cursor:
            user_list.append(user[0])
    return user_list

def get_admin_id():
    with sqlite3.connect('database.db') as DB:
        select_query = f"SELECT id FROM users WHERE admin=1"
        cursor = DB.cursor()
        cursor.execute(select_query)
        DB.commit()
        for user in cursor:
            return user[0]

def get_user_info(id):
    user_info = ''
    with sqlite3.connect('database.db') as DB:
        select_query = f"SELECT * FROM users WHERE id={id}"
        cursor = DB.cursor()
        cursor.execute(select_query)
        DB.commit()
        for user in cursor:
            user_info = (f'Id: {user[0]}\n'
                        f'Ник: {user[1]}\n'
                        f'Имя: {user[2]}\n')
            if user[5]==1:
                user_info += (f'Подписка: активна\n')
                user_info += (f'Дата окончания подписки: {user[6]}\n')
            else:
                user_info+=(f'Подписка: не активна')
            print(user_info)
            return user_info

def deactivate_user(id):
    with sqlite3.connect('database.db') as DB:
        update_query = f"UPDATE users SET active = 0 WHERE id={id}"
        cursor = DB.cursor()
        cursor.execute(update_query)
        DB.commit()

def get_sub(id):
    with sqlite3.connect('database.db') as DB:
        select_query = f"SELECT sub FROM users WHERE id={id}"
        cursor = DB.cursor()
        cursor.execute(select_query)
        DB.commit()
        for sub in cursor:
            if int(sub[0])==1:
                return True
            else:
                return False

def sub_activate(id):
    date_in_one_month = datetime.now() + timedelta(days=30)
    deact_date = f'{date_in_one_month.day}.{date_in_one_month.month}.{date_in_one_month.year}'
    with sqlite3.connect('database.db') as DB:
        update_query = f"UPDATE users SET sub = 1, deactDate = '{deact_date}' WHERE id={id}"
        cursor = DB.cursor()
        cursor.execute(update_query)
        DB.commit()

def sub_deactivate(id):
    with sqlite3.connect('database.db') as DB:
        update_query = f"UPDATE users SET sub = 0 WHERE id={id}"
        cursor = DB.cursor()
        cursor.execute(update_query)
        DB.commit()

def get_date_deactivate(id):
    with sqlite3.connect('database.db') as DB:
        select_query = f"SELECT deactDate FROM users WHERE id={id}"
        cursor = DB.cursor()
        cursor.execute(select_query)
        DB.commit()
        for date in cursor:
            return date[0]