#----------------------------------------------------------------------------#
# Imports.
#----------------------------------------------------------------------------#
import os, logging
from flask import Flask, render_template, flash, redirect, session, url_for, request, g, send_from_directory, jsonify
from app import app, db, login_manager
from sqlalchemy import desc, insert
from flask.ext.sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
from models import *
from flask.ext.login import login_user, logout_user, current_user, login_required

from werkzeug import secure_filename
import hashlib

import flask.ext.whooshalchemy

from datetime import date
import time

login_manager.login_view = 'login'


PER_PAGE = 5

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user

@app.route('/register' , methods=['GET','POST'])
def register():

    if request.method == 'GET':
        return render_template('pages/login/register.html')
    m = hashlib.md5()
    m.update(request.form['password'] + "thisIsMyHash")
    m = m.hexdigest()
    password = m

    user = User(username = request.form['username'], password = password, email = request.form['email'])
    db.session.add(user)
    print "user commit"
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('home'))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('pages/login/login.html')
    elif request.method == 'POST':
        print "in post"
        print request.form['username']
        username = request.form['username']
        password = request.form['password']
        m = hashlib.md5()
        m.update(password + "thisIsMyHash")
        m = m.hexdigest()
        password = m
        registered_user = User.query.filter_by(username=username,password=password).first()
        if registered_user is None:
            flash('Username or Password is invalid' , 'error')
            return redirect(url_for('login'))
        login_user(registered_user)
        # flash('Logged in successfully')
        session['logged_in'] = True
        print "username %s" % username
        return redirect(request.args.get('next') or url_for('home'))

@app.route('/logout')
def logout():
    logout_user()
    session.pop('logged_in', None)
    return redirect(url_for('home'))

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    # sesconn.list_verified_email_addresses()
    return render_template('pages/home.html')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    today = date.today()
    return send_from_directory(app.config['UPLOAD_FOLDER'] + str(today), filename)

@app.route('/uploads/<key>/<path:filename>')
def uploaded_photos(filename, key):
    return send_from_directory(app.config['UPLOAD_FOLDER'] + str(key), filename)

#----------------------------------------------------------------------------#
# Search
#----------------------------------------------------------------------------#

@app.route('/search/all', methods = ['POST'])
@login_required
def search():
    if request.method == 'POST':
        if "[)>" in request.form['search']:
            serial = serialfilter(request.form['search'])
            device = Device.query.filter_by(serial = serial).first()
            devices = Device.query.whoosh_search(serial)
            events = Event.query.filter_by(is_active = True).all()
            return render_template('pages/search/results.html', result = request.form['search'][13:],\
                devices = devices, device = device, events = events)   
        device = Device.query.whoosh_search(request.form['search'])
        #qr = QRCode.query.whoosh_search(request.form['search'])
        return render_template('pages/search/results.html', result = request.form['search'], devices = device)#, qrs = qr)


#----------------------------------------------------------------------------#
# User Managment
#----------------------------------------------------------------------------#

@app.route('/usermanager')
@login_required
def usermanager():
    thetime = time.strftime("%H:%M")
    today = date.today()
    users = User.query.all()

    return render_template('pages/usermanager/usermanager.html', thetime = thetime, today = today, users = users)

@app.route('/usermanager/<editme>', methods = ['POST'])
@login_required
def useredit(editme):

    edits = User.query.filter_by(username = editme).first_or_404()
    edits.username = request.form['username']
    edits.email = request.form['email']
    edits.level = request.form['level']
    db.session.add(edits)
    db.session.commit()

    return redirect(url_for('usermanager'))

#----------------------------------------------------------------------------#
# Profile Managment
#----------------------------------------------------------------------------#

@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def myprofile():
    thetime = time.strftime("%H:%M")
    today = date.today()

    if request.method == 'POST':
        photo = request.files['file']
        print photo
        if photo:
            username = g.user.username
            user = User.query.filter_by(username = username).first()
            filename = secure_filename(photo.filename)
            try:
                os.makedirs(app.config['UPLOAD_FOLDER'] + "user" + "photos")
            except:
                pass

            photo.save(os.path.join(app.config['UPLOAD_FOLDER'] + "user" + "photos", filename))
            user.photo = filename
            db.session.add(user)
            db.session.commit()
            flash('success')
            return render_template('pages/profile/myprofile.html', thetime = thetime, today = today)
        else:
            flash('No file chosen')
            return render_template('pages/profile/myprofile.html', thetime = thetime, today = today)


    return render_template('pages/profile/myprofile.html', thetime = thetime, today = today)

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