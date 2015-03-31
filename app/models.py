from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from dictalchemy import DictableModel
from sqlalchemy import Column, Integer, String, Date, PickleType
from app import db, app
from flask.ext.login import UserMixin
from datetime import datetime
import flask.ext.whooshalchemy as whooshalchemy
from collections import OrderedDict

# class Item(db.Model):
#     __tablename__ = "Item"
#     __searchable__ = ['serial', 'title', 'desc', 'owner', 'borrower', 'location', 'notes']

#     id = db.Column(db.Integer, primary_key=True)
#     serial = db.Column(db.String()) # serial
#     title = db.Column(db.String()) # device title
#     desc = db.Column(db.String()) # description
#     owner = db.Column(db.String()) # who owns this device
#     borrower = db.Column(db.String()) # who is borrowing this device
#     location = db.Column(db.String()) # location fo device
#     notes = db.Column(db.String()) # notes

#     @property
#     def serialize(self):
#        """Return object data in easily serializeable format"""
#        return {
#            'id': self.id, 'serial': self.serial, 'title': self.title,
#            'desc': self.desc, 'owner': self.owner, 'borrower': self.borrower,
#            'location': self.location, 'notes': self.notes
#            }
#            # This is an example how to deal with Many2Many relations
#            #'many2many'  : self.serialize_many2many
           
#     @property
#     def serialize_many2many(self):
#        """
#        Return object's relations in easily serializeable format.
#        NB! Calls many2many's serialize property.
#        """
#        return [ item.serialize for item in self.many2many]

#     def __repr__(self):
#         return "WR Item "+self.title+" @ serial "+self.serial

# whooshalchemy.whoosh_index(app, Item)

class User(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(20), unique=True , index=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(50),unique=True , index=True)
    # photo = db.Column(db.String(120), default="default.png")
    # registered_on = db.Column('registered_on' , db.DateTime)
    # level = db.Column(db.String(10), default="1")
    # wants = db.Column(db.String(10), default="1")
 
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        # self.level = level
        # self.registered_on = datetime.utcnow()
        # self.wants = wants
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)