from flask import Flask, render_template, flash, redirect, session, url_for, request, g, send_from_directory, jsonify
from app import app, db
from sqlalchemy import desc, insert
from flask.ext.sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
from models import *
# from celery.tasks import task
# Build a system to collect data that is generated on an interval (once a minute/hour/day/etc).
# Store in a database; record time and data value. 
# Build a web app that displays a graph of the collected data with your choice of intervals.
# Add a table report of the data with column headings. The table should be placed below the graph. 

@app.route('/')
def home():
    # sesconn.list_verified_email_addresses()
    datas = FakeData.query.all()
    return render_template('pages/home.html', datas = datas)

@app.route('/api/get')
def apiGet():
    data = FakeData.query.all()
    return jsonify(json_list = [d.serialize for d in data])

@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.route('/contact')
def contact():
    return render_template('pages/contact.html')

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def internal_error(error):
    return render_template('errors/404.html'), 404