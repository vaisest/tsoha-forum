from app import db
from app.auth.forms import LoginForm, RegisterForm
from app.auth.manager import User
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.before_app_request
def before_request():
    if current_user.is_authenticated:
        redirect(url_for("main.index"))


@auth_blueprint.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        remember_me = form.remember_me.data

        user = User.get_by_username(username)
        if not user or not check_password_hash(user.password_hash, password):
            return redirect(url_for("auth.login"))

        login_user(user, remember=remember_me)
        flash("You were succesfully logged in", "success")
        print(user, username, password, remember_me)
        return redirect(url_for("main.index"))
    return render_template("login.html", form=form)


@auth_blueprint.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        password_hash = generate_password_hash(password)

        check_sql = text("SELECT EXISTS (SELECT 1 FROM accounts WHERE username = :username)")
        exists = db.session.execute(check_sql, {"username": username}).first()[0]

        if exists:
            flash("Username already exists", "error")
            print(f"Existing user {username=}")
            return redirect(url_for("auth.register"))

        sql = text(
            """
            INSERT INTO accounts (username, password_hash)
            VALUES
                (:username, :password_hash)
            RETURNING id
            """
        )
        result = db.session.execute(
            sql, {"username": username, "password_hash": password_hash}
        )
        new_id = result.first()[0]
        db.session.commit()

        login_user(User(new_id, username, password_hash))

        print(f"New user {new_id=}, {username=}")
        flash("User succesfully created", "success")
        return redirect(url_for("main.index"))
    return render_template("register.html", form=form)


@auth_blueprint.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("main.index"))


# @main_blueprint.route("/")
# def index():
#     sql = text("SELECT * FROM posts;")
#     res = db.session.execute(sql).all()
#     posts = [row[1:] for row in res]
#     print(f"{posts=}")

#     return render_template("index.html", posts=posts)


# @main_blueprint.route("/submit", methods=["GET", "POST"])
# def submit():
#     form = SubmitPostForm()
#     if form.validate_on_submit():
#         title = form.title.data
#         body = form.body.data

#         sql = text("INSERT INTO posts (title, body) VALUES (:title, :body)")
#         db.session.execute(sql, {"title": title, "body": body})
#         db.session.commit()

#         return redirect("/")
#     return render_template("submit.html", form=form)