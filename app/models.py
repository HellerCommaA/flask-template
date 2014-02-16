from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from app import db

class System(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serialsystem = db.Column(db.String(120)) # system serial
    location = db.Column(db.String(120), default="") # location
    fsrpoc = db.Column(db.String(120), default="") # fsr email
    partsused = db.Column(db.String(1200), default="") #parts assigned by S/N
    filename = db.Column(db.String(120), default="")