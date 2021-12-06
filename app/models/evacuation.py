from app import login_manager, db
from sqlalchemy import Column, String, Integer, ForeignKey, text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import random



class Way(db.Model):
    __tablename__ = "way"
    id = Column(Integer, primary_key=True)
    name = Column(db.String(255), unique=True)
    description = Column(db.String(255))
    published = Column(db.Boolean, server_default='1', default=True)

    def amount_points(self):
        return len(self.points)

    def get_points(self):
        latlong=[]
        cantidad = len(self.points)
        for i in range(cantidad):
            punto = []
            punto.append(str(self.points[i].get_latitude()))
            punto.append(str(self.points[i].get_longitude()))
            latlong.append(punto)
        return latlong

    def save(self):
        db.session.add(self)
        db.session.commit()
    
   
    def set_description(self, description):
        self.description = description

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def all(cls, published, order_by):
        return cls.query.filter_by(published=published).order_by(text(order_by))

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=bytes(name, 'utf-8')).first()

    @classmethod
    def by_name(cls,name, active, order_by):
       return cls.query.filter((cls.name.like("%{}%".format(name))) & (cls.published == active)).order_by(text(order_by))

    def toggle(self):
        self.published = not self.published
        self.save()

    @classmethod
    def delete(cls, id):
        way = cls.query.get(id)
        points = way.points
        for p in points:
            p.delete()
        db.session.delete(way)
        db.session.commit()

    def delete_points(self):
        points = self.points
        for p in points:
            p.delete()

class WayPoint(db.Model):
    __tablename__ = "waypoint"
    id = Column(Integer, primary_key=True)
    latitude = Column(db.String(30))
    longitude = Column(db.String(30))
    way_id = Column(Integer, ForeignKey("way.id"))
    route = relationship(Way, backref=backref("points", uselist = True))


    def get_latitude(self):
        return str(self.latitude)
    
    def get_longitude(self):
        return str(self.longitude)

    def get_way_id(self):
        return str(self.way_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()