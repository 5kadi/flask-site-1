from flask import Blueprint, request, render_template, redirect, url_for, flash, session, abort
import database_mod
import database_avatars
import database_users
import database_posts
from forms import login_form, signup_form

view = Blueprint("view", __name__, template_folder="templates", static_folder="static")

@view.before_request
def start():
    global dbase_menu
    dbase_menu = database_mod.menu_select(1, 2, 7)

@view.route("/")
@view.route("/home")
def homepage():
    return render_template("view/home.html", menu=dbase_menu)

@view.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        if database_users.add_user(request.form["username"], request.form["password"]) == True:
            flash("User added!", category = "True")
        else:
            flash("This user already exists!", category = "False")
    return render_template("view/signup.html", menu=dbase_menu, form=signup_form())

@view.route("/login", methods = ["GET", "POST"])
def login():
    session.permanent = True
    if "userLogged" in session:
        return redirect(f"/user/users/{session['userLogged']}")
    else:
        if request.method == "POST":
            if database_users.match_user("users", request.form["username"], request.form["password"]) == True:
                session["userLogged"] = request.form["username"]
                if database_avatars.select_avatar(request.form["username"]) == None:
                    database_avatars.add_avatar(request.form["username"], view.root_path + url_for("static", filename = "/images/default_av_1.png"))
                return redirect(f"/user/users/{session['userLogged']}")
            else:
                flash("Incorrect username or password!")
        return render_template("view/login.html", menu=dbase_menu, form=login_form())

@view.errorhandler(401)
def error401(error):
    return render_template("view/error401.html", menu=dbase_menu)

@view.errorhandler(404)
def error404(error):
    return render_template("view/error404.html", menu=dbase_menu)