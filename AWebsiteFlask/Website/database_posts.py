import sqlite3 as sq
from database_mod import get_db

def create_post(username, post_text):
    db = get_db()
    cur = db.cursor()
    cur.execute("BEGIN")
    try:
        cur.execute(f"INSERT INTO posts(user_id, username, post_text) VALUES ((SELECT id FROM users WHERE username IN('{username}')), '{username}', '{post_text}')")
        cur.execute("COMMIT")
    except sq.Error as error:
        print("create_post error:", error)
        cur.execute("ROLLBACK")

def get_posts():
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("SELECT username, post_text, post_id FROM posts")
        res = cur.fetchall()
        if res:
            return res
        else:
            return []
    except sq.Error as error:
        print("get_posts error:", error)
        return []
    
def delete_post(post_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("BEGIN")
    try:
        cur.execute(f"DELETE FROM posts WHERE post_id IN({post_id})")
        cur.execute("COMMIT")
    except sq.Error as error:
        print("delete_post error:", error)
        cur.execute("ROLLBACK")

def select_post(post_id):
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(f"SELECT post_id, username, post_text FROM posts WHERE post_id IN({post_id})")
        res = cur.fetchall()
        if res:
            return res
        else:
            return False
    except sq.Error as error:
        print("select_post error:", error)
        return []