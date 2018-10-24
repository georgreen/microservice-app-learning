from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# instantiate the db
db = SQLAlchemy()


class User(db.Model):

    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def to_json(self):
        return {
            'id': self.uid,
            'username': self.username,
            'email': self.email,
            'active': self.active
        }
