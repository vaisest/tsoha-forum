from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import text

from . import db
from .auth.manager import User
from .util import relative_date_format


@dataclass
class Post:
    """Dataclass that represents a Tsohit post."""

    title: str
    body: str
    username: str
    creation_date: datetime
    relative_date: str
    sub_name: str


def get_posts(for_sub=None):
    sql = text(
        """
        SELECT title, body, username, creation_date, sub_name FROM posts
            JOIN accounts ON posts.author_id = accounts.account_id
            JOIN subtsohits ON posts.parent_sub_id = subtsohits.sub_id
                AND (:for_sub IS NULL OR subtsohits.sub_name = :for_sub)
        """
    )
    res = db.session.execute(sql, {"for_sub": for_sub}).all()

    posts = [
        Post(item[0], item[1], item[2], item[3], relative_date_format(item[3]), item[4])
        for item in res
    ]

    return posts


def insert_post(title, body, author_id, sub_id):
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
    sql = text("SELECT sub_id, sub_name, sub_title FROM subtsohits")
    res = db.session.execute(sql).all()

    subs = [Sub(sub[0], str(sub[0]), sub[1], sub[2]) for sub in res]

    return subs


def get_sub_by_name(name):
    sql = text("SELECT sub_id, sub_name, sub_title FROM subtsohits WHERE sub_name = :name")
    res = db.session.execute(sql, {"name": name}).first()

    if not res:
        return None

    sub = Sub(res[0], str(res[0]), res[1], res[2])

    return sub


def create_sub_if_unique(name, title, creator_id):
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
    check_sql = text("SELECT EXISTS (SELECT 1 FROM accounts WHERE username = :username)")
    exists = db.session.execute(check_sql, {"username": username}).first()[0]

    return exists


def create_user(username, password_hash):
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
    sql = text(
        "SELECT account_id, username, password_hash FROM accounts WHERE account_id = :id LIMIT 1"
    )
    result = db.session.execute(sql, {"id": user_id}).first()

    if not result:
        return None

    user = User(result[0], result[1], result[2])

    return user


def get_user_by_username(username):
    sql = text(
        "SELECT account_id, username, password_hash FROM accounts WHERE username = :username LIMIT 1"
    )
    result = db.session.execute(sql, {"username": username}).first()

    if not result:
        return None

    user = User(result[0], result[1], result[2])

    return user
