#----------------------------------------------------------------------------#
# Imports.
#----------------------------------------------------------------------------#
import os, logging
from flask import Flask, render_template, flash, redirect, url_for, request, g, send_from_directory, jsonify
from app import app, db, basic_auth, mail
from sqlalchemy import desc, insert
from flask.ext.sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
from models import System, Subsystem, Parts, ServiceCall, WarrantyClaimForm, Survey, SurveyMaster
from flask.ext.mail import Message
from werkzeug import secure_filename
from types import *
import hashlib
# IMPORTING BOTO FOR SNS PUSH
import boto
from boto import sns
# IMPORTS FOR DATE TIME
from datetime import date
import time
# IMPORTS FOR PYCHART
from pygooglechart import PieChart2D, QRChart

#----------------------------------------------------------------------------#
# MISC.
#----------------------------------------------------------------------------#

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
@basic_auth.required
def home():
    thetime = time.strftime("%H:%M")
    today = date.today()

    return render_template('pages/home.html', thetime = thetime, today = today)# , parts = parts)


#----------------------------------------------------------------------------#
# Error Handling
#----------------------------------------------------------------------------#

@app.errorhandler(500)
def internal_error(error):
    thetime = time.strftime("%H:%M")
    today = date.today()
    #db_session.rollback()
    return render_template('errors/500.html', thetime = thetime, today = today), 500

@app.errorhandler(404)
def internal_error(error):
    thetime = time.strftime("%H:%M")
    today = date.today()
    return render_template('errors/404.html', thetime = thetime, today = today), 404