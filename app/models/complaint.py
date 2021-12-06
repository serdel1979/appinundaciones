from flask_sqlalchemy import Model

from app import login_manager, db
from sqlalchemy import Column, String, Integer, ForeignKey, text, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from app.models.user import User
from app.helpers.denuncias import EstadoDenuncias, CategoriaDenuncias
from datetime import date, datetime
# una denunca tiene muchos seguimientos
# un seguimiento tiene un solo autor
class FollowUp(db.Model):
    __tablename__ = "follow_up"
    id = Column(Integer, primary_key=True)
    description = Column(db.String(2000))
    created_at = db.Column(db.DateTime, server_default=func.now())
    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship("User", backref=backref("follow_ups"))
    complaint_id = Column(Integer, ForeignKey("complaint.id"))
    complaint = relationship("Complaint", backref=backref("follow_ups", cascade='all,delete', uselist=True))
        
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get_follow_ups_for_complaint(cls, complaint_id,order_by):
        return cls.query.filter_by(complaint_id=complaint_id).order_by(text(order_by))

    @classmethod
    def all(cls, order_by):
        return cls.query.order_by(text(order_by))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete(cls, id):
        location = cls.query.get(id)
        db.session.delete(location)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

class Complaint(db.Model):
    __tablename__ = "complaint"
    id = Column(Integer, primary_key=True)
    title = Column(db.String(30))
    desc = Column(db.String(2000))
    latitude = db.Column(db.String(30), unique=False)
    longitude = db.Column(db.String(30), unique=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    surname = Column(db.String(30))
    name = Column(db.String(30))
    phone = Column(db.String(50))
    email = Column(db.String(255))
    category = Column(db.Integer(), unique=False)
    status = Column(db.Integer(), unique=False)
    closed_date = db.Column(db.DateTime)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User, backref=backref("complaints", uselist=True))

    def __init__(self, title=None, desc=None,
                 latitude=None, longitude=None,
                 surname=None, name=None,
                 phone=None, email=None, category=None, status=None, user=None):
        self.title = title
        self.desc = desc
        self.latitude = latitude
        self.longitude = longitude
        self.surname = surname
        self.name = name
        self.phone = phone
        self.email = email
        self.created_at = datetime.now()
        values = [item.value for item in CategoriaDenuncias]
        if category in values:
            self.category = category
        if status is None:
            self.status = EstadoDenuncias.SinConfirmar.value
        else:
            self.status = status
        self.user_id = user

    def __repr__(self): 
        f"""< {self.title}, {self.desc}, {self.latitude}, {self.longitude},
        denunciante: {self.name}, {self.surname}, {self.phone}, {self.email},
        asignado a: {str(self.user_id)}>"""

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


    def set_user(self, user):
        self.user_id = user
    def get_user(self):
        return User.get_by_id(self.user_id)

    def as_dict(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}

    def close_complaint(self):
        self.status = EstadoDenuncias.Cerrada.value
        self.closed_date = datetime.now()
        self.save()

    def update_status(self, status):
        self.status = status 
        self.save()

    def add_user(self, user):
        self.user_id = user 
        self.save()

    @classmethod
    def delete(cls, id):
        db.session.delete(id)
        db.session.commit()

    @classmethod
    def get_follow_ups(self, id):
        return FollowUp().query.filter_by(id=id)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_status(cls, status, order_by):
        return cls.query.filter_by(status=status).order_by(text(order_by))

    @classmethod
    def find_by_title(cls, title, order_by):
        return cls.query.filter(cls.title.like(f"%{title}%")).order_by(
            text(order_by))

    @classmethod
    def find_by_created_at_range(cls, from_at, to_at, order_by):
        return cls.query.filter(func.date(Complaint.created_at) <= to_at,
                                   func.date(Complaint.created_at) >= from_at).order_by(text(order_by))

    @classmethod
    def all(cls, order_by):
        return cls.query.order_by(text(order_by))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete(cls, id):
        location = cls.query.get(id)
        db.session.delete(location)
        db.session.commit()
