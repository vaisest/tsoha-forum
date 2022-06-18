"""
This file contains a sort of a service that contains the parts
of the app that interact directly with the database.
All of the project's SQL code (except for the schema) is
located here. Currently this contains one big service,
but as a TODO it could be split into several smaller services.
"""
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import text

from . import db
from .auth.manager import User
from .util import relative_date_format


@dataclass
class Post:
    """Dataclass that represents a Tsohit post."""

    id: str
    title: str
    body: str
    username: str
    creation_date: datetime
    relative_date: str
    sub_name: str = None


def get_posts(for_sub=None):
    """
    Gets all posts from DB, or only for a specific sub if kwarg for_sub is defined.
    Returns data as Post instances.
    """

    sql = text(
        """
        SELECT post_id, title, body, username, creation_date, sub_name FROM posts
            JOIN accounts ON posts.author_id = accounts.account_id
            JOIN subtsohits ON posts.parent_sub_id = subtsohits.sub_id
                AND (:for_sub IS NULL OR subtsohits.sub_name = :for_sub)
        """
    )
    res = db.session.execute(sql, {"for_sub": for_sub}).all()

    posts = [
        Post(
            item[0], item[1], item[2], item[3], item[4], relative_date_format(item[4]), item[5]
        )
        for item in res
    ]

    return posts


@dataclass
class Comment:
    """Dataclass that represents a comment."""

    body: str
    username: str
    creation_date: datetime
    relative_date: str


def get_post_and_comments_by_id(post_id):
    """
    Gets a single post from the database based on a
    post_id. Returns it as a Post instance.
    """

    sql = text(
        """
        SELECT post_id, title, body, username, creation_date FROM posts
            JOIN accounts ON posts.author_id = accounts.account_id
            WHERE posts.post_id = :post_id
        """
    )
    res = db.session.execute(sql, {"post_id": post_id}).first()

    post = Post(res[0], res[1], res[2], res[3], res[4], relative_date_format(res[4]))

    return post


def insert_post(title, body, author_id, sub_id):
    """
    Inserts post into database, based on arguments title, body, author_id, sub_id.
    Returns the id of the inserted post.
    """

    sql = text(
        """
            INSERT INTO posts (title, body, author_id, parent_sub_id)
                VALUES (:title, :body, :author_id, :sub_id)
                RETURNING post_id
            """
    )
    res = db.session.execute(
        sql, {"title": title, "body": body, "author_id": author_id, "sub_id": sub_id}
    )
    new_id = res.first()[0]
    db.session.commit()

    return new_id


@dataclass
class Sub:
    """Dataclass that represents a subtsohit."""

    id_: int
    id_str: str
    name: str
    title: str


def get_subs():
    """
    Gets all subs from DB.
    Returns data as Sub instances.
    """

    sql = text("SELECT sub_id, sub_name, sub_title FROM subtsohits")
    res = db.session.execute(sql).all()

    subs = [Sub(sub[0], str(sub[0]), sub[1], sub[2]) for sub in res]

    return subs


def get_sub_by_name(name):
    """
    Gets a specific sub from DB based on name.
    Returns the item as a Sub instance, or None if it wasn't found.
    """

    sql = text("SELECT sub_id, sub_name, sub_title FROM subtsohits WHERE sub_name = :name")
    res = db.session.execute(sql, {"name": name}).first()

    if not res:
        return None

    sub = Sub(res[0], str(res[0]), res[1], res[2])

    return sub


def create_sub_if_unique(name, title, creator_id):
    """
    Inserts sub into database, based on arguments name, title, and creator_id
    after checking that it is unique.
    Returns True if it was added, and False if it wasn't.
    """

    check_sql = text("SELECT EXISTS (SELECT 1 FROM subtsohits WHERE sub_name = :name)")
    exists = db.session.execute(check_sql, {"name": name}).first()[0]

    if exists:
        return False

    insert_sql = text(
        """
        INSERT INTO subtsohits (sub_name, sub_title, creator_id)
            VALUES (:name, :title, :creator_id)
        """
    )
    db.session.execute(insert_sql, {"name": name, "title": title, "creator_id": creator_id})
    db.session.commit()

    return True


def user_exists(username):
    """
    Queries the database for an username.
    Returns True if the username exists, and False if it doesn't.
    """

    check_sql = text("SELECT EXISTS (SELECT 1 FROM accounts WHERE username = :username)")
    exists = db.session.execute(check_sql, {"username": username}).first()[0]

    return exists


def create_user(username, password_hash):
    """
    Inserts user into database, based on arguments usename and password_hash.
    Returns the new user as a Flask-Login User class instance.
    """

    sql = text(
        """
            INSERT INTO accounts (username, password_hash)
            VALUES
                (:username, :password_hash)
            RETURNING account_id
            """
    )

    result = db.session.execute(sql, {"username": username, "password_hash": password_hash})
    new_id = result.first()[0]
    db.session.commit()

    return User(new_id, username, password_hash)


def get_user_by_id(user_id):
    """
    Gets a specific user from DB based on its id.
    Returns the item as a Flask-Login User instance, or None if it wasn't found.
    """

    sql = text(
        "SELECT account_id, username, password_hash FROM accounts WHERE account_id = :id LIMIT 1"
    )
    result = db.session.execute(sql, {"id": user_id}).first()

    if not result:
        return None

    user = User(result[0], result[1], result[2])

    return user


def get_user_by_username(username):
    """
    Gets a specific user from DB based on its username.
    Returns the item as a Flask-Login User instance, or None if it wasn't found.
    """

    sql = text(
        "SELECT account_id, username, password_hash FROM accounts WHERE username = :username LIMIT 1"
    )
    result = db.session.execute(sql, {"username": username}).first()

    if not result:
        return None

    user = User(result[0], result[1], result[2])

    return user
