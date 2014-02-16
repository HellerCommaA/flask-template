from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from app import db
from flask.ext.login import UserMixin

class System(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serialsystem = db.Column(db.String(120)) # system serial
    location = db.Column(db.String(120), default="") # location
    fsrpoc = db.Column(db.String(120), default="") # fsr email
    partsused = db.Column(db.String(1200), default="") #parts assigned by S/N
    filename = db.Column(db.String(120), default="")

class Subsystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    system_id = db.Column(db.String(120)) # what SN system it is linked with
    sub_type = db.Column(db.String(120)) #ROCU or Manip or Robot ETC
    firmware = db.Column(db.String(120)) # Firmware Version
    software = db.Column(db.String(120), default ="N/A") # software version
    serialsub = db.Column(db.String(120)) # serial of subsystem
    partsused = db.Column(db.String(1200), default="") #parts assigned

class Parts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invid = db.Column(db.String(120)) # Inventory ID
    name = db.Column(db.String(120)) # part name
    num = db.Column(db.String(120)) # part number
    serial = db.Column(db.String(120), default = "") # serial, if applicable
    note = db.Column(db.String(120)) # note
    price = db.Column(db.String(120)) # price per unit
    quan = db.Column(db.String(120)) # quantity in stock
    location = db.Column(db.String(120)) # location of part
    low_stock = db.Column(db.String(120)) # low stock

class ServiceCall(db.Model):
    ticket = db.Column(db.Integer, primary_key = True) # ticket number, assigned by us
    location = db.Column(db.String(120)) # location of unit calling request
    who = db.Column(db.String(120)) # who is opening ticket
    phone = db.Column(db.String(120)) # phone number
    email = db.Column(db.String(120)) # email address
    org = db.Column(db.String(120)) # org who owns the bot
    serial = db.Column(db.String(120)) # serial number of problem system
    env = db.Column(db.String(120)) # environment, urban,offroad,gravel,mountain
    product = db.Column(db.String(120)) # product, mtgr,rocu,manipulator,mpu,other
    ptype = db.Column(db.String(120)) # type of problem, electrical,mechanical,accessories,software,other
    date = db.Column(db.String(120)) # date reported
    time = db.Column(db.String(120)) # time reported
    problem = db.Column(db.String(120)) # problem description
    filename = db.Column(db.String(120), default="") # filename of uploaded files
    solution = db.Column(db.String(120), default="") # solution for when ticket is closed
    status = db.Column(db.String(120), default="1") # status, 1 open, 2 wait, 3 closed by fsr, 4 closed by admin
    statusdate = db.Column(db.String(120)) # Date last edited
    postauthor = db.Column(db.String(120), default=",") # post author
    posttime = db.Column(db.String(120), default=",") # post time
    postdate = db.Column(db.String(120), default=",") # post date
    postmessage = db.Column(db.String(120), default=",") # post message
    totalmessages = db.Column(db.Integer, default=0) # total number of posts
    partsused = db.Column(db.String(1200), default="") # parts used 
    # message = db.Column(db.String) # message append in AUTHOR, MESSAGE, DATE, TIME: 0,1,2,3
    # author = db.Column(db.String, default="|!@#|") # last to edit ticket

class WarrantyClaimForm(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(120)) # date wcf opened
    location = db.Column(db.String(120)) # location of system
    name = db.Column(db.String(120)) # name of reporter
    env = db.Column(db.String(120)) # tag cloud of types of enviornment
    org = db.Column(db.String(120)) # org IE 702EOD
    product = db.Column(db.String(120)) # system type MTGR, ROCU, MPU
    serialwcf = db.Column(db.String(120)) # serial for prodcut
    wcftype = db.Column(db.String(120)) # type of failure
    status = db.Column(db.String(120)) # status of WCF, open, close, pending
    primarycat = db.Column(db.String(120)) # primary failure category
    secondarycat = db.Column(db.String(120)) # secondary failure category
    description = db.Column(db.String(120)) # description of problem
    resolution = db.Column(db.String(120)) # problem's resolution
    filename = db.Column(db.String(120)) # file name of associated images
    servicecall = db.Column(db.String(120)) # associated servicecall

class SurveyMaster(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    key = db.Column(db.String(120)) # unique key assigned by FSR
    date = db.Column(db.String(120)) # date

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    key = db.Column(db.String(120)) # unique key assigned by FSR
    name = db.Column(db.String(120)) # name of person doing survey
    role = db.Column(db.String(120)) # Team member, team sgt
    unit = db.Column(db.String(120)) # unit name
    location = db.Column(db.String(120)) # location of training
    date = db.Column(db.String(120)) # date of training
    eodsof = db.Column(db.String(120)) # EOD or SOF
    thours = db.Column(db.String(120)) # total training hours
    fsr = db.Column(db.String(120)) # FSR giving class
    mdescript = db.Column(db.String(120)) # mission description
    terrain = db.Column(db.String(120)) # terrain, urban offroad gravel mountain desert
    los = db.Column(db.String(120)) # LOS used 1 yes 0 no
    mesh = db.Column(db.String(120)) # mesh used 1 yes 0 no
    manip = db.Column(db.String(120)) # manip used 1 yes 0 no
    timeofday = db.Column(db.String(120)) # 1 day 0 night
    q1 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q2 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q3 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q4 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q5 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q6 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q7 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q8 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q9 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q10 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q11 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q12 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q13 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q14 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q15 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q16 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q17 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q18 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q19 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q20 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q21 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q22 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q23 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q24 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    q25 = db.Column(db.String(120)) # -2 strongly disagree, -1 disagree 0 not observed +1 agree +2 strongly agree
    comments = db.Column(db.String(120)) # additional comments

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(120))
    email = db.Column(db.String(120))
    password = db.Column(db.String(30))

# class Bugs(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     bug_sn = db.Column(db.Integer, default=0) # what serial number this specific bug is attached to
#     description = db.Column(db.String(120)) # description