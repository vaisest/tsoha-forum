from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from .. import db_service
from ..main.forms import CommentForm, CreateSubForm, SubmitPostForm

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    """Route for main view with posts from all subs."""
    posts = db_service.get_posts(current_user_id=current_user.id)
    subs = db_service.get_subs()
    # print(f"{posts=}")

    return render_template("main/index.html", posts=posts, subs=subs)


@main_blueprint.route("/t/<sub_name>/")
def sub_index(sub_name):
    """Route for sub view where only posts from specificed sub are shown."""
    posts = db_service.get_posts(for_sub=sub_name)
    subs = db_service.get_subs()
    sub = next(sub for sub in subs if sub.name == sub_name)

    if not sub:
        flash("Subtsohit does not exist", "error")
        return redirect(url_for("main.index"))

    # print(f"{posts=} in {sub=}")

    return render_template("main/index.html", posts=posts, sub=sub, subs=subs)


@main_blueprint.route("/t/<sub_name>/<post_id>", methods=["POST", "GET"])
def single_post(sub_name, post_id):
    """Route for single post view. Shows post and its comments."""

    post, comments = db_service.get_post_and_comments_by_id(post_id)
    subs = db_service.get_subs()
    sub = next(sub for sub in subs if sub.name == sub_name)

    form = CommentForm()

    if not sub:
        flash("Subtsohit does not exist", "error")
        return redirect(url_for("main.index"))

    if not post:
        flash("Post does not exist", "error")
        return redirect(url_for("main.sub_index", sub_name=sub_name))

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You are not logged in", "error")
            return redirect(url_for("main.single_post", sub_name=sub_name, post_id=post_id))

        body = form.body.data

        db_service.insert_comment(body, post.id, current_user.id)
        return redirect(url_for("main.single_post", sub_name=sub_name, post_id=post_id))

    return render_template(
        "main/post.html", form=form, post=post, comments=comments, sub=sub, subs=subs
    )


@main_blueprint.route("/submit", methods=["GET", "POST"])
@login_required
def submit():
    """Route for showing both a post submission form and handling its POST."""
    form = SubmitPostForm()

    subs = db_service.get_subs()

    form.sub.choices = [(sub.id_str, sub.name) for sub in subs]
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        sub_id = form.sub.data

        db_service.insert_post(title, body, current_user.id, sub_id)

        return redirect("/")
    return render_template("main/submit.html", form=form)


@main_blueprint.route("/subs/create", methods=["GET", "POST"])
@login_required
def create_sub():
    """Route for showing both a sub creation form and handling its POST."""
    form = CreateSubForm()

    if form.validate_on_submit():
        name = form.name.data
        title = form.title.data

        created = db_service.create_sub_if_unique(name, title, current_user.id)
        if not created:
            flash("Subtsohit with same name already exists", "error")
            return redirect(url_for("main.create_sub"))

        return redirect(url_for("main.sub_index", sub_name=name))
    return render_template("main/create_sub.html", form=form)


@main_blueprint.get("/vote_post/<int:post_id>/<action>")
@login_required
def vote_post(post_id, action):
    if action not in ("upvote", "downvote"):
        flash("Vote action invalid", "error")
        return redirect(url_for("main.index"))

    value = 1 if action == "upvote" else -1

    if not db_service.insert_post_vote(current_user.id, post_id, value):
        flash("Vote failed. Post_id is incorrect.", "error")
        return redirect(url_for("main.index"))

    return redirect(url_for("main.index"))
