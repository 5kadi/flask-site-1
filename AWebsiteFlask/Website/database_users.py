import sqlite3 as sq
from database_mod import get_db

def add_user(username, password):
    db = get_db()
    cur = db.cursor()
    cur.execute("BEGIN")
    try:
        cur.execute(f"SELECT username FROM users WHERE username IN('{username}')")
        res = cur.fetchone()
        if res == None:
            cur.execute(f"INSERT INTO users(username, password) VALUES ('{username}', '{password}')")
            cur.execute("COMMIT")
            return True
        else:
            return False
    except sq.Error as error:
        print("add_user error:", error)
        cur.execute("ROLLBACK")
        return False
    
def match_user(table, username, password):
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(f"SELECT * FROM {table} WHERE username IN('{username}') AND password IN('{password}')")
        res = cur.fetchone()
        if res == None:
            return False
        else:
            return True
    except sq.Error as error:
        print("match_user error:", error)
        return False
    
def select_user(table, username, column):
    db = get_db()
    cur = db.cursor()
    try: 
        cur.execute(f"SELECT {column} FROM {table} WHERE username IN('{username}')")
        res = cur.fetchone()
        if res:
            return res
    except sq.Error as error:
        print("select_user error:", error)
        return "yaebaalflask"
    
