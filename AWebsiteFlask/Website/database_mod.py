import sqlite3 as sq
from flask import current_app, g, url_for

def connect_db():
    con = sq.connect(current_app.config["DATABASE"])
    con.row_factory = sq.Row
    return con

def create_db():
    db = connect_db()
    cur = db.cursor()
    with current_app.open_resource("sq_db.sql", mode="r") as f:
        cur.executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, "db"):
        g.db = connect_db()
        print("Database opened.")
    return g.db
      
def menu_select(*args):
    db = get_db()
    cur = db.cursor()
    try:  
        cur.execute(f"SELECT * FROM menu WHERE id IN{args}")
        res = cur.fetchall()
        if res:
            return res
    except sq.Error as error:
        print("menu_select error:", error)
        return []

    





    









    



