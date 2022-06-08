from flask import Blueprint, redirect, render_template
from flask_login import current_user, login_required
from sqlalchemy import text

from app.util import relative_date_format

from .. import db
from ..main.forms import SubmitPostForm

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    sql = text(
        "SELECT title, body, username, creation_date FROM posts JOIN accounts ON posts.author_id = accounts.id"
    )
    res = db.session.execute(sql).all()
    posts = [(row[0], row[1], row[2], relative_date_format(row[3])) for row in res]
    print(f"{posts=}")

    return render_template("index.html", posts=posts)


@main_blueprint.route("/submit", methods=["GET", "POST"])
@login_required
def submit():
    form = SubmitPostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data

        sql = text(
            "INSERT INTO posts (title, body, author_id) VALUES (:title, :body, :author_id)"
        )
        db.session.execute(sql, {"title": title, "body": body, "author_id": current_user.id})
        db.session.commit()

        return redirect("/")
    return render_template("submit.html", form=form)
