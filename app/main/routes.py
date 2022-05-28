from flask import Blueprint, redirect, render_template
from flask_login import login_required
from app import db
from app.main.forms import SubmitPostForm
from sqlalchemy import text

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    sql = text("SELECT * FROM posts;")
    res = db.session.execute(sql).all()
    posts = [row[1:] for row in res]
    print(f"{posts=}")

    return render_template("index.html", posts=posts)


@main_blueprint.route("/submit", methods=["GET", "POST"])
@login_required
def submit():
    form = SubmitPostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data

        sql = text("INSERT INTO posts (title, body) VALUES (:title, :body)")
        db.session.execute(sql, {"title": title, "body": body})
        db.session.commit()

        return redirect("/")
    return render_template("submit.html", form=form)
