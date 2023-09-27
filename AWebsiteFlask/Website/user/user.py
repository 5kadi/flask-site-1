from flask import Blueprint, request, render_template, redirect, url_for, flash, session, abort
import database_mod
import database_avatars
import database_users
import database_posts
from forms import login_form, signup_form

user = Blueprint("user", __name__, template_folder="templates", static_folder="static")

@user.before_request
def connect():
    global dbase_menu
    dbase_menu = database_mod.menu_select(1, 3, 4)

@user.route("/")
@user.route("/home")
def homepage():
    return render_template("user/home.html", menu=dbase_menu)  

@user.route("/login")
def profile():
    if "userLogged" in session:
        return redirect(f"/user/users/{session['userLogged']}")
    else:
        return redirect("/view/login")

@user.route("/logout")
def logout():
    if "userLogged" in session:
        session.pop("userLogged")
        return redirect("/view/login")
    else:
        return redirect("/view/login")
    
@user.route("/users/<username>", methods=["GET", "POST"])
def users(username):
    if "userLogged" not in session or session["userLogged"] != username:
        abort(401)
    else:
        return render_template("user/users.html", menu=dbase_menu, username=username)
    
@user.route("/posts", methods=["POST", "GET"])
def posts():
    if "userLogged" not in session:
        abort(401)
    else:
        return render_template("user/posts.html", menu=dbase_menu, posts=database_posts.get_posts())

@user.route("/createpost/<username>", methods = ["POST", "GET"])
def createpost(username):
    if "userLogged" not in session or session["userLogged"] != username:
        abort(401)
    else:
        if request.method == "POST":
            database_posts.create_post(session["userLogged"], request.form["post_text"])
            flash("Post created successfully!", category="True")
    return render_template("user/createpost.html", menu=dbase_menu, username=username)

@user.route("/post/<post_id>", methods=["POST", "GET"])
def post(post_id):
    if "userLogged" not in session:
        abort(401)
    else:
        return render_template("user/post.html", menu=dbase_menu, post=database_posts.select_post(post_id)[0])
   
@user.route("/addavatar/<username>", methods=["POST", "GET"])
def addavatar(username):
    if session["userLogged"] != username or "userLogged" not in session:
        abort(401)
    else:
        if request.method == "POST":
            try:
                file = request.files["avatar"]
                img = file.read()
                database_avatars.add_avatar(username, img, mode="bin")
                flash("Uploaded successfully", category="True")
                return redirect(f"/user/users/{username}")
            except:
                flash("Failed to upload!", category="False")
        return render_template("user/addavatar.html", menu=dbase_menu, username=username)
    
@user.errorhandler(401)
def error401(error):
    return render_template("user/error401.html", menu=dbase_menu)

@user.errorhandler(404)
def error404(error):
    return render_template("user/error404.html", menu=dbase_menu)

