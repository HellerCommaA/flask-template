import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'thisismykeytherearemanylikeitbuthtisoneisminetakeitlearnfromiteatfromit'

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'mysql://user:PASSWORD@RDS.AWS.COM/mydb'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

UPLOAD_FOLDER = '/Users/adam/Desktop/Projects/flask-template/app/uploads/' # LOCAL USE ONLY
# UPLOAD_FOLDER = '/root/flask-template/app/uploads' # LIVE SERVER USE

BASIC_AUTH_USERNAME = 'admin'
BASIC_AUTH_PASSWORD = 'password'