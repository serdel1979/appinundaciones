import numbers

from app import db
from sqlalchemy import text
from dataclasses import dataclass


class Location(db.Model):
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    status = db.Column(db.String(255), unique=False)
    address = db.Column(db.String(255), unique=True)
    telephone = db.Column(db.String(255), unique=True)
    latitude = db.Column(db.String(30), unique=False)
    longitude = db.Column(db.String(30), unique=False)

    def set_attributes(self, name, email, status, address, telephone, lat, long):
        self.name = name
        self.email = email
        self.status = status
        self.address = address
        self.telephone = telephone
        self.latitude = lat
        self.longitude = long
        return self

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete(cls, id):
        location = cls.query.get(id)
        db.session.delete(location)
        db.session.commit()

    @classmethod
    def search_location(cls, name, order_by, published=True):
        status = "publicado" if published else "despublicado"
        return cls.query.filter((cls.name.startswith(name)) & (cls.status == status)).order_by(text(order_by))

    @classmethod
    def all_locations(cls, order_by, published=True):
        status = "publicado" if published else "despublicado"
        return cls.query.filter_by(status=status).order_by(text(order_by))


@dataclass
class Coordinate:
    latitude: numbers
    longitude: numbers
