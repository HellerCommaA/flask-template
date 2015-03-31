import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'asdfasdfasdfasdf'

# Connect to the database
# Use this for AWS RDB
# SQLALCHEMY_DATABASE_URI = 'mysql://user:PASSWORD@RDS.AWS.COM/mydb'
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Change this to project root directory
UPLOAD_FOLDER = '/Users/adam/Desktop/Projects/flask-template/app/uploads/' # LOCAL USE ONLY
# UPLOAD_FOLDER = '/root/flask-template/app/uploads' # LIVE SERVER USE