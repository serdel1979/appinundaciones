from app import db
from sqlalchemy import func, text

"""
Este es el modelo de usuario pendiente, donde se representa a los 
registros pendientes
"""


class UserPending(db.Model):
    __tablename__ = "pending"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    def __init__(self, username, first_name, last_name, email):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=bytes(username, 'utf-8')).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def search_pending(cls, email, order_by):
        return cls.query.filter(cls.email.startswith(email)).order_by(text(order_by))

    @classmethod
    def all_pendings(cls, order_by):
        return cls.query.order_by(text(order_by))

    @classmethod
    def delete(cls, id):
        user_pending = cls.query.get(id)
        db.session.delete(user_pending)
        db.session.commit()
