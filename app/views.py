from flask import Flask, render_template, flash, redirect, session, url_for, request, g, send_from_directory, jsonify
from app import app, db
from sqlalchemy import desc, insert
from flask.ext.sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
from models import *

@app.route('/')
def home():
    return render_template('pages/home.html')

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