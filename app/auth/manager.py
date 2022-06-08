from flask_login import UserMixin
from sqlalchemy.sql import text

from .. import db_service, login_manager


class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        return db_service.get_user_by_id(user_id)

    @staticmethod
    def get_by_username(username):
        return db_service.get_user_by_usernamename(username)

    def __str__(self):
        return f"User(Id={self.id}, username={self.username})"


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
