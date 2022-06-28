"""
This file contains a sort of a service that contains the parts
of the app that interact directly with the database.
All of the project's SQL code (except for the schema) is
located here. Currently this contains one big service,
but as a TODO it could be split into several smaller services.
"""
from dataclasses import dataclass
from datetime import datetime

from psycopg2.errors import ForeignKeyViolation
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from . import db
from .auth.manager import User
from .util import relative_date_format


@dataclass
class Post:
    """Dataclass that represents a Tsohit post."""

    id: int
    title: str
    body: str
    username: str
    creation_date: datetime
    relative_date: str
    sub_name: str = None
    comment_count: int = None
    user_vote: bool = None
    score: int = 0


def get_posts(for_sub=None, current_user_id=None):
    """
    Gets all posts from DB, or only for a specific sub if kwarg for_sub is defined.
    Returns data as Post instances.
    """

    sql = text(
        """
        SELECT p.post_id, p.title, p.body, a.username, p.creation_date, s.sub_name,
            cc.comment_count,
            vs.vote_sum,
            (SELECT vote_value
                FROM votes tv
                WHERE
                    tv.account_id = :acc_id AND p.post_id = tv.post_id)
            AS liked_by_account
        FROM posts AS p
        JOIN accounts a ON p.author_id = a.account_id
        JOIN subtsohits s ON p.parent_sub_id = s.sub_id
            AND (:for_sub IS NULL OR s.sub_name = :for_sub)
        JOIN (SELECT p.post_id, COUNT(c) AS comment_count
                FROM posts p
                LEFT JOIN comments c ON c.post_id = p.post_id
                GROUP BY p.post_id) cc
                    ON p.post_id = cc.post_id
        JOIN (SELECT p.post_id, GREATEST(SUM(v.vote_value), 0) AS vote_sum
                FROM posts p
                LEFT JOIN votes v ON p.post_id = v.post_id
                GROUP BY p.post_id) vs
                    ON p.post_id = vs.post_id
        WHERE p.deleted = 'f'
        ORDER BY p.creation_date DESC;
        """
    )
    res = db.session.execute(sql, {"for_sub": for_sub, "acc_id": current_user_id}).all()
    posts = [
        Post(
            item[0],
            item[1],
            item[2],
            item[3],
            item[4],
            relative_date_format(item[4]),
            item[5],
            comment_count=item[6],
            user_vote=item[8],
            score=item[7],
        )
        for item in res
    ]

    return posts


@dataclass
class Comment:
    """Dataclass that represents a comment."""

    id: int
    parent_id: int
    body: str
    author: str
    creation_date: datetime
    relative_date: str
    score: int
    user_vote: int


def get_post_and_comments_by_id(post_id, current_user_id=None):
    """
    Gets a single post from the database based on a
    post_id. Returns it as a Post instance.
    """

    post_sql = text(
        """
        SELECT p.post_id, p.title, p.body, a.username, p.creation_date, cc.comment_count, vs.vote_sum,
            (SELECT vote_value
                FROM votes tv
                WHERE
                    tv.account_id = :acc_id AND p.post_id = tv.post_id)
            AS liked_by_account
        FROM posts AS p
        JOIN accounts a ON p.author_id = a.account_id
        JOIN (SELECT p.post_id, COUNT(c) AS comment_count
                FROM posts p
                LEFT JOIN comments c ON c.post_id = p.post_id
                GROUP BY p.post_id) cc
                    ON p.post_id = cc.post_id
        JOIN (SELECT p.post_id, GREATEST(SUM(v.vote_value), 0) AS vote_sum
                FROM posts p
                LEFT JOIN votes v ON p.post_id = v.post_id
                GROUP BY p.post_id) vs
                    ON p.post_id = vs.post_id
        WHERE p.post_id = :post_id
        ORDER BY p.creation_date DESC;
        """
    )
    post_res = db.session.execute(
        post_sql, {"post_id": post_id, "acc_id": current_user_id}
    ).first()

    if not post_res:
        return None, None

    post = Post(
        post_res[0],
        post_res[1],
        post_res[2],
        post_res[3],
        post_res[4],
        relative_date_format(post_res[4]),
        comment_count=post_res[5],
        score=post_res[6],
        user_vote=post_res[7],
    )

    comment_sql = text(
        """
        SELECT c.comment_id, c.parent_id, c.body, a.username, c.creation_date, vs.vote_sum AS score, uv.vote_value AS user_vote
        FROM comments c
            JOIN accounts a ON c.author_id = a.account_id
            JOIN posts ON c.post_id = posts.post_id
            JOIN (SELECT ct.comment_id, GREATEST(SUM(v.vote_value), 0) AS vote_sum
                FROM comments ct
                LEFT JOIN votes v ON ct.comment_id = v.comment_id
                GROUP BY ct.comment_id) vs
                    ON c.comment_id = vs.comment_id
            LEFT JOIN (SELECT tv.comment_id, tv.vote_value
                    FROM votes tv
                    WHERE
                        tv.account_id = :acc_id) uv
                        ON c.comment_id = uv.comment_id
            WHERE c.post_id = :post_id;
        """
    )
    comment_res = db.session.execute(
        comment_sql, {"post_id": post_id, "acc_id": current_user_id}
    ).all()
    comments = [
        Comment(
            item[0],
            item[1],
            item[2],
            item[3],
            item[4],
            relative_date_format(item[4]),
            item[5],
            item[6],
        )
        for item in comment_res
    ]

    return post, comments


def insert_comment(body, post_id, author_id):
    """
    Inserts comment into database, based on arguments body, post_id, and author_id.
    Returns the id of the inserted post.
    """

    sql = text(
        """
            INSERT INTO comments (body, post_id, author_id)
                VALUES (:body, :post_id, :author_id)
                RETURNING comment_id
            """
    )
    res = db.session.execute(sql, {"body": body, "post_id": post_id, "author_id": author_id})
    new_id = res.first()[0]
    db.session.commit()

    insert_vote(author_id, 1, comment_id=new_id)

    return new_id


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

    insert_vote(author_id, 1, post_id=new_id)

    return new_id


def insert_vote(account_id, value, post_id=None, comment_id=None):
    """
    Inserts a new vote into DB, based on author_id, post_id, and value.
    If the vote exists, the value is updated.
    Returns False on failure, and True on success.
    """

    post_sql = text(
        """
            INSERT INTO votes (account_id, post_id, vote_value)
                VALUES (:account_id, :post_id, :value)
                ON CONFLICT
                    ON CONSTRAINT votes_account_id_post_id_key
                DO
                    UPDATE SET vote_value = :value;
        """
    )

    # ON CONFLICT ON CONSTRAINT can't check multiple constraints so need separate query:
    comment_sql = text(
        """
            INSERT INTO votes (account_id, comment_id, vote_value)
                VALUES (:account_id, :comment_id, :value)
                ON CONFLICT
                    ON CONSTRAINT votes_account_id_comment_id_key
                DO
                    UPDATE SET vote_value = :value;
        """
    )
    try:
        if post_id:
            db.session.execute(
                post_sql, {"account_id": account_id, "post_id": post_id, "value": value}
            )
        elif comment_id:
            db.session.execute(
                comment_sql,
                {"account_id": account_id, "comment_id": comment_id, "value": value},
            )

        db.session.commit()
        return True
    except IntegrityError as e:
        if isinstance(e.orig, ForeignKeyViolation):
            return False
        else:
            raise e


def delete_vote(account_id, post_id=None, comment_id=None):
    """
    Removes a vote from the database based on account_id and post_id.
    """

    sql = text(
        """
            DELETE FROM votes
                WHERE account_id = :account_id
                    AND
                        (post_id = :post_id
                        OR comment_id = comment_id)
        """
    )
    db.session.execute(
        sql, {"account_id": account_id, "post_id": post_id, "comment_id": comment_id}
    )
    db.session.commit()


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
