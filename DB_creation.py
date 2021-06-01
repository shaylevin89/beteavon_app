import sqlite3

con = sqlite3.connect('beteavon.db', check_same_thread=False)


def create_table():
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS orders (ID INTEGER PRIMARY KEY AUTOINCREMENT, time TIMESTAMP NOT NULL,
                        name varchar NOT NULL,  address varchar NOT NULL, comments varchar, owner varchar NOT NULL );''')
    cur.execute('''CREATE TABLE IF NOT EXISTS printers ( id integer NOT NULL UNIQUE, name varchar NOT NULL, 
                        nickname varchar , active varchar DEFAULT 'false' NOT NULL, api_key varchar NOT NULL );''')
    cur.execute('''CREATE TABLE IF NOT EXISTS users ( name varchar NOT NULL,
                        nickname varchar NOT NULL UNIQUE, hashed_pass varchar NOT NULL );''')
    cur.execute('''CREATE TABLE IF NOT EXISTS api_keys ( nickname varchar NOT NULL, api_key varchar NOT NULL );''')
    con.close()

