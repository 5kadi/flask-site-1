from flask import Blueprint, request, render_template, redirect, url_for, flash, session, abort
import database_mod
import database_avatars
import database_users
import database_posts
from forms import login_form, signup_form

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

@admin.before_request
def connect():
    global dbase_menu
    dbase_menu = database_mod.menu_select(3, 4)

@admin.route("/")
@admin.route("/home")
def homepage():
    return render_template("admin/home.html", menu=dbase_menu)  

@admin.route("/login", methods = ["GET", "POST"])
def login():
    if "adminLogged" in session:
        return redirect(f"users/{session['adminLogged']}")
    else:
        if request.method == "POST":
            if database_users.match_user("admin_users", request.form["username"], request.form["password"]) == True:
                session["adminLogged"] = request.form["username"]
                if database_avatars.select_avatar(request.form["username"]) == None:
                    database_avatars.add_avatar(request.form["username"], admin.root_path + url_for("static", filename = "/images/default_av_1.png"))
                return redirect(f"users/{session['adminLogged']}")
            else:
                flash("Incorrect username or password!")
        return render_template("admin/login.html", menu=dbase_menu, form=login_form())

@admin.route("/logout")
def logout():
    if "adminLogged" in session:
        session.pop("adminLogged")
        return redirect("/admin/login")
    else:
        return redirect("/admin/login")
    
@admin.route("/users/<username>", methods=["GET", "POST"])
def users(username):
    if "adminLogged" not in session or session["adminLogged"] != username:
        abort(401)
    else:
        return render_template("admin/users.html", menu=dbase_menu, username=username)
    
@admin.route("/posts", methods=["POST", "GET"])
def posts():
    if "adminLogged" not in session:
        abort(401)
    else:
        return render_template("admin/posts.html", menu=dbase_menu, posts=database_posts.get_posts())

@admin.route("/createpost/<username>", methods = ["POST", "GET"])
def createpost(username):
    if "adminLogged" not in session or session["adminLogged"] != username:
        abort(401)
    else:
        if request.method == "POST":
            database_posts.create_post(session["adminLogged"], request.form["post_text"])
            flash("Post created successfully!", category="True")
    return render_template("admin/createpost.html", menu=dbase_menu, username=username)

@admin.route("/post/<post_id>", methods=["POST", "GET"])
def post(post_id):
    if "adminLogged" not in session:
        abort(401)
    else:
        return render_template("admin/post.html", menu=dbase_menu, post=database_posts.select_post(post_id)[0])
    
@admin.route("/deletepost/<post_id>", methods=["POST", "GET"])
def delete_post(post_id):
    if "adminLogged" not in session:
        abort(401)
    else:
        database_posts.delete_post(post_id)
    return redirect("/admin/posts")

@admin.route("/addavatar/<username>", methods=["POST", "GET"])
def addavatar(username):
    if session["adminLogged"] != username or "adminLogged" not in session:
        abort(401)
    else:
        if request.method == "POST":
            try:
                file = request.files["avatar"]
                img  = file.read()
                database_avatars.add_avatar(username, img, mode="bin")
                flash("Uploaded successfully!", category="True")
                return redirect(f"/admin/users/{username}")
            except:
                flash("Failed to upload!", category="False")
        return render_template("admin/addavatar.html", menu=dbase_menu, username=username)
    
@admin.errorhandler(404)
def error404(error):
    return render_template("admin/error404.html", menu=dbase_menu)

@admin.errorhandler(401)
def error401(error):
    return render_template("admin/error401.html", menu=dbase_menu)

