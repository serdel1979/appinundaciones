from app import login_manager, db
from sqlalchemy import Column, String, Integer, ForeignKey, text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import random



class Zone(db.Model):
    __tablename__ = "zone"
    id = Column(Integer, primary_key=True)
    name = Column(db.String(255), unique=True)
    colour = Column(db.String(7))
    code = Column(db.String(20))
    published = Column(db.Boolean, server_default='1', default=True)

    def __init__(self, name, colour, published = True):
        self.name = name
        self.colour = colour
        self.Published = published
        self.code = str(random.randint(0,100))+str((name[:5]).replace(" ","_")).lower()

    def amount_points(self):
        return len(self.polygon)

    def get_polygon(self):
        latlong=[]
        cantidad = len(self.polygon)
        for i in range(cantidad):
            punto = []
            punto.append(str(self.polygon[i].get_latitude()))
            punto.append(str(self.polygon[i].get_longitude()))
            latlong.append(punto)
        return latlong

    def set_polygon(self,coordenadas):
        self.delete_polygon()
        puntos = coordenadas.split(sep=",")
        caracteres = "[]\"\n"
        lat=""
        lng=""
        for i in range(len(puntos)):
            if i % 2 == 0:
                lat = ''.join( x for x in puntos[i] if x not in caracteres)
            else:
                lng = ''.join( x for x in puntos[i] if x not in caracteres)
                coordenadas = Point(latitude=lat, longitude=lng,zone = self)
                coordenadas.save()

    def delete_polygon(self):
        polygon = self.polygon
        for pol in polygon:
            pol.delete()


    def save(self):
        db.session.add(self)
        db.session.commit()
    
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


    @classmethod
    def delete(cls, id):
        zona = cls.query.get(id)
        polygon = zona.polygon
        for pol in polygon:
            pol.delete()
        db.session.delete(zona)
        db.session.commit()

    def toggle(self):
        self.published = not self.published
        self.save()

class Point(db.Model):
    __tablename__ = "point"
    id = Column(Integer, primary_key=True)
    latitude = Column(db.String(30))
    longitude = Column(db.String(30))
    zone_id = Column(Integer, ForeignKey("zone.id"))
    zone = relationship(Zone, backref=backref("polygon", uselist = True))


    def get_latitude(self):
        return str(self.latitude)
    
    def get_longitude(self):
        return str(self.longitude)

    def get_zone_id(self):
        return str(self.zone_id)

   
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()