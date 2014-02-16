import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'thisismykeytherearemanylikeitbuthtisoneisminetakeitlearnfromiteatfromit'

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'mysql://roboteam:thisis123321pass@mydb.cbm4dvakskrt.us-east-1.rds.amazonaws.com/mydb'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

UPLOAD_FOLDER = '/Users/adam/Desktop/Projects/botlog/app/uploads/' # LOCAL USE ONLY
# UPLOAD_FOLDER = '/root/botloger/app/uploads' # LIVE SERVER USE

# BASIC_AUTH_USERNAME = 'admin'
# BASIC_AUTH_PASSWORD = 'MTGRrocks'

SHAHAR_LOGIN = 'shahar'
SHAHAR_PASSWORD = 'Ckqex9ApP'

CALEB_LOGIN = 'caleb'
CALEB_PASSWORD = 'H753GQdf13'

SHANE_LOGIN = 'shane'
SHANE_PASSWORD = 'suckit'

BRIAN_LOGIN = 'brian'
BRIAN_PASSWORD = '872ibKJHA'

GEORGIA_LOGIN = 'georgia'
GEORGIA_PASSWORD = 'kjbawe78fh'

SAM_LOGIN = 'sam'
SAM_PASSWORD = 'nb2k34luith'

ADMIN_LOGIN = 'admin'
ADMIN_PASSWORD = 'MTGRrocks'

ADAM_LOGIN = 'adam'
ADAM_PASSWORD = 'uKJHBjy657afUGF'

ELAD_LOGIN = 'elad'
ELAD_PASSWORD = 'KJHYg1jhb2jhb'

ELI_LOGIN = 'eli'
ELI_PASSWORD = 'qiwuhe8f7'

GAL_LOGIN = 'gal'
GAL_PASSWORD = 'LKkjqnwe23f'

JASON_LOGIN = 'jason'
JASON_PASSWORD = '86tUAVuyv'

JEFF_LOGIN = 'jeff'
JEFF_PASSWORD = 'Ka7huAjib937fb'

KYLE_LOGIN = 'kyle'
KYLE_PASSWORD = 'KJB41uiba'

MEL_LOGIN = 'mel'
MEL_PASSWORD = 'kuHi2j3f*&G8'

SEAN_LOGIN = 'sean'
SEAN_PASSWORD = 'jniU!ibefjnsf^!'

SUPPORT_LOGIN = 'support'
SUPPORT_PASSWORD = 'Robo@678'

YOSI_LOGIN = 'yosi'
YOSI_PASSWORD = 'ibhi2bIUAf1'

JP_LOGIN = 'jp'
JP_PASSWORD = 'KJfiub*!eoi'



MAIL_SERVER = 'smtp.office365.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'support@roboteam.onmicrosoft.com'
MAIL_PASSWORD = 'robo@678'
DEFAULT_MAIL_SENDER = 'support@robo-team.com'

#  flask-Uploads
# UPLOAD_FOLDER = '/tmp/'
# ALLOWED_EXTENSIONS = set(['jpg'])
# config['UPLOAD_FOLDER'] = UPLOAD_FOLDER