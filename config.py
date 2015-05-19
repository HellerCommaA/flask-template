import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'qowiuhrf097q8ywrf0978whe0r87hfw0e8rgh79w8e7bvos8d7hfvkjahsgdf987GFIUYSDGFouysdbfa98sdgfyaos8d7fOSYDg'

# Connect to the database
# Use this for AWS RDB
# SQLALCHEMY_DATABASE_URI = 'mysql://user:PASSWORD@RDS.AWS.COM/mydb'
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

BROKER_URL = 'sqla+sqlite:///' + os.path.join(basedir, 'celerydb.sqlite')

# Change this to project root directory
# UPLOAD_FOLDER = basedir + "/uploads/" # LOCAL USE ONLY
# UPLOAD_FOLDER = '/root/flask-template/app/uploads' # LIVE SERVER USE