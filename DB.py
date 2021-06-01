import sqlite3
from DB_creation import create_table
import printnode_connection
import logging


LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

def db_connect():
    con = sqlite3.connect('beteavon.db', check_same_thread=False)
    return con


create_table()
con = db_connect()


def insert_new_user(name, nickname, hashed_pass):
    cur = con.cursor()
    cur.execute(f'''insert into users (name, nickname, hashed_pass) 
                VALUES('{name}', '{nickname}', '{hashed_pass}')''')
    con.commit()


def check_if_user_exist(nick):
    cur = con.cursor()
    cur.execute(f'''select hashed_pass from users where nickname = '{nick}' ''')
    res = cur.fetchone()
    return res


def insert_api_key(name, api_key):
    cur = con.cursor()
    cur.execute(f'''insert into api_keys (nickname, api_key) 
                VALUES('{name}', '{api_key}')''')
    con.commit()


def get_api(name, one_api=False):
    cur = con.cursor()
    cur.execute(f"select api_key from api_keys where nickname = '{name}'")
    if one_api:
        res = cur.fetchone()
        return res
    res = cur.fetchall()
    return res


def insert_printers(printers_list):
    cur = con.cursor()
    cur.executemany("INSERT OR IGNORE into printers (id, name, api_key) values (?, ?, ?)", printers_list)
    con.commit()


def update_printers(printer_id, nickname=None, active=None):
    cur = con.cursor()
    if nickname and active in ['true', 'false']:
        cur.execute(f"update printers set nickname = '{nickname}', active = '{active}' where id = {printer_id} ")
    elif nickname:
        cur.execute(f"update printers set nickname = '{nickname}' where id = {printer_id} ")
    elif active in ['true', 'false']:
        cur.execute(f"update printers set active = '{active}' where id = {printer_id} ")
    con.commit()


def get_printers(api_key):
    printers_list = printnode_connection.get_printers(api_key)
    insert_printers(printers_list)
    cur = con.cursor()
    cur.execute(f"select id, name, nickname, active from printers where api_key = '{api_key}' ")
    res = cur.fetchall()
    return res


def get_printer(printer_id):
    cur = con.cursor()
    cur.execute(f"select id, name, nickname, active from printers where id = {printer_id} ")
    res = cur.fetchone()
    return res


def get_active_printers(api_key):
    cur = con.cursor()
    cur.execute(f"select id from printers where api_key = '{api_key}' and active = 'true' ")
    res = cur.fetchall()
    if res:
        res = [x[0] for x in res]
        return res
    return []


def insert_order(time, name, address, comments, owner):
    cur = con.cursor()
    cur.execute(f"""insert into orders (time, name, address, comments, owner) 
                values( '{time}', '{name}', '{address}', '{comments}', '{owner}') """)
    con.commit()


def get_orders(owner):
    cur = con.cursor()
    cur.execute(f"select time, name, address, comments from orders where owner = '{owner}'")
    res = cur.fetchall()
    return res



# l = printnote_try.get_printers('FEGj7XvW5hWAiU44d6qN7wxdNdrxNpO6WOxPZsvxsoU')
# print(l)
# cur = con.cursor()
# insert_printers(l)
# cur.execute("INSERT  into printers (id, name) values (?, ?)")
# con.commit()
#
# res = cur.execute('select * from orders')
# print(res.fetchall())
# update_printers('70376628', active=True)
# print(get_printers('FEGj7XvW5hWAiU44d6qN7wxdNdrxNpO6WOxPZsvxsoU'))
# print(get_printer(70387557))