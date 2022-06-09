from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db_service
from ..auth.forms import LoginForm, RegisterForm
from ..auth.manager import User

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
            flash("Incorrect username or password", "error")
            return redirect(url_for("auth.login"))

        login_user(user, remember=remember_me)
        flash("You were succesfully logged in", "success")
        return redirect(url_for("main.index"))
    return render_template("auth/login.html", form=form)


@auth_blueprint.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        exists = db_service.user_exists(username)

        if exists:
            flash("Username already exists", "error")
            print(f"Existing user {username=}")
            return redirect(url_for("auth.register"))

        password_hash = generate_password_hash(password)

        user = db_service.create_user(username, password_hash)

        login_user(user)

        print(f"New user {user=}")
        flash("User succesfully created", "success")
        return redirect(url_for("main.index"))
    return render_template("auth/register.html", form=form)


@auth_blueprint.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("main.index"))
