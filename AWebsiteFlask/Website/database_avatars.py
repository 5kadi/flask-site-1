import sqlite3 as sq
from database_mod import get_db

def convert_image(img):
    with open(img, "rb") as f:
        data = f.read()
    return data

def decode_image(img):
    img = str(img)
    img.replace()
    
def add_avatar(username, img, mode="dir"):
    db = get_db()
    cur = db.cursor()
    cur.execute("BEGIN")
    try:
        converted_img = convert_image(img) if mode == "dir" else sq.Binary(img)
        data_tuple = (username, converted_img)
        cur.execute(f"DELETE FROM user_avatar WHERE user_id IN((SELECT id FROM users WHERE username LIKE '{username}'))")
        cur.execute(f"INSERT INTO user_avatar VALUES((SELECT id FROM users WHERE username LIKE ?), ?)", data_tuple)
        cur.execute("COMMIT")
    except sq.Error as error:
        cur.execute("ROLLBACK")
        print("add_avatar error:", error)
        return []
    
def select_avatar(username):
    db = get_db()
    cur = db.cursor()
    try: 
        cur.execute(f"SELECT avatar FROM user_avatar WHERE user_id IN((SELECT id FROM users WHERE username LIKE '{username}'))")
        res = cur.fetchone()
        if res:
            return res
    except sq.Error as error:
        print("select_avatar error:", error)
        return False