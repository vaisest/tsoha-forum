from flask_login import UserMixin
from .. import db, login_manager
from sqlalchemy.sql import text


class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        print("a", user_id)
        sql = text("SELECT id, username, password_hash FROM accounts WHERE id = :id LIMIT 1")
        result = db.session.execute(sql, {"id": user_id}).first()
        return None if not result else User(result[0], result[1], result[2])

    @staticmethod
    def get_by_username(username):
        sql = text(
            "SELECT id, username, password_hash FROM accounts WHERE username = :username LIMIT 1"
        )
        result = db.session.execute(sql, {"username": username}).first()
        return None if not result else User(result[0], result[1], result[2])

    def __str__(self):
        return f"User(Id={self.id}, username={self.username})"


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
