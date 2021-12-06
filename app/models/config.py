from app import db
from flask import Flask, request
from datetime import datetime
from sqlalchemy import func


class Configuration(db.Model): #clase singleton

    __tablename__ = "configuration"
    id = db.Column(db.Integer, primary_key=True)
    order_by = db.Column(db.Integer, unique=False, default=1)
    num_elems = db.Column(db.Integer, unique=True, default=5)
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    public_primary_color_hex = db.Column(db.String(7))
    public_secondary_color_hex = db.Column(db.String(7))
    public_terciary_color_hex = db.Column(db.String(7))
    private_primary_color_hex = db.Column(db.String(7))
    private_secondary_color_hex = db.Column(db.String(7))
    private_terciary_color_hex = db.Column(db.String(7))

    @classmethod
    def create_default(cls):
        config = Configuration()
        config.num_elems                   = 5
        config.order_by                    = 0
        config.public_primary_color_hex    = "#B744B8"
        config.public_secondary_color_hex  = "#B744B8"
        config.public_terciary_color_hex   = "#ededed"
        config.private_primary_color_hex   = "#28282a"
        config.private_secondary_color_hex = "#28282a"
        config.private_terciary_color_hex  = "#ededed"
        return config


    @classmethod
    def current(cls):
        config = cls.query.first()
        if config is None:
            config = cls.create_default()
            config.save_edit()
        return config

    @classmethod
    def update(cls, **kwargs):
        config = cls.current()
        cls.query.filter_by(id=config.id).update(dict(  order_by=kwargs["order_by"], num_elems=kwargs["num_elems"], 
                                                        public_primary_color_hex = kwargs["public_first"],
                                                        public_secondary_color_hex = kwargs["public_second"],
                                                        public_terciary_color_hex = kwargs["public_third"],
                                                        private_primary_color_hex = kwargs["private_first"],
                                                        private_secondary_color_hex = kwargs["private_second"],
                                                        private_terciary_color_hex = kwargs["private_third"]))
        db.session.commit()

    #debugging method
    @classmethod
    def has_values(cls):
        config = cls.current()
        return db.session.query(config.exists())


    @classmethod
    def get_order_by(cls):
        return cls.current().order_by

    @classmethod
    def get_num_elems(cls):
        return cls.current().num_elems

    @classmethod
    def is_ascendent(cls):
        return cls.current().order_by == 1
    
    @classmethod
    def is_descendent(cls):
        return cls.current().order_by == 0

    @classmethod
    def is_in_range(cls):
        n = cls.current().num_elems
        return n > 0 and n < 100
        
    @classmethod
    def get_private_app(cls):
        return {
                "headings": cls.current().private_primary_color_hex,
                "buttons": cls.current().private_secondary_color_hex,
                "background": cls.current().private_terciary_color_hex
                }

    @classmethod
    def get_public_app(cls):
        return {
                "headings": cls.current().public_primary_color_hex,
                "buttons": cls.current().public_secondary_color_hex,
                "background": cls.current().public_terciary_color_hex
                }

    def save(self):
        db.session.add(self)
        db.session.commit()


    def save_edit(self):
        self.updated_at = datetime.now()
        db.session.add(self)
        db.session.commit()
