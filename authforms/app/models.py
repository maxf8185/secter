from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional


class User(UserMixin, db.Model):
    id: int = sa.Column(sa.Integer, primary_key=True)
    username: str = sa.Column(sa.String(60), unique=True, nullable=False)
    email: str = sa.Column(sa.String(60), unique=True, nullable=False)
    password_hash: Optional[str] = sa.Column(sa.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
