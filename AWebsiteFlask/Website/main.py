from flask import Flask, render_template, request, flash, session, redirect, url_for, abort, g, make_response
import os
import sqlite3 as sq
import database_mod
import database_avatars
from user_manager import UserLogin
from admin.admin import admin
from user.user import user
from view.view import view

app = Flask(__name__)
SECRET_KEY = "73"
DATABASE = "/templates/database.db"
DEBUG = True
MAX_CONTENT_LENGTH = 1024 * 1024
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, "database.db")))

app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(view, url_prefix="/view")

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "db"):
        print("Database closed.")
        g.db.close()

@app.route("/home", methods = ["GET", "POST"])
@app.route("/", methods = ["GET", "POST"])
def home():
    return redirect("/view/") 
    
@app.route("/avatar/<username>", methods = ["GET", "POST"])
def avatar(username):
    if database_avatars.select_avatar(username) != None:
        img = database_avatars.select_avatar(username)[0]
        resp = make_response(img)
        resp.headers["Content-Type"] = "image/png"
        return resp
    else:
        abort(404)

@app.route("/secret")
def secret():
    return "обед уютненько"

if __name__ == "__main__":
    with app.app_context():
        database_mod.create_db()
        app.run(debug=True)
    
    

    
