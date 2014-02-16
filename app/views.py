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
def home():
    thetime = time.strftime("%H:%M")
    today = date.today()

    return render_template('pages/home.html', thetime = thetime, today = today)# , parts = parts)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    today = date.today()
    return send_from_directory(app.config['UPLOAD_FOLDER'] + str(today), filename)

@app.route('/test')
# @login_required
def test():
    thetime = time.strftime("%H:%M")
    today = date.today()
    return render_template('pages/test.html', thetime = thetime, today = today)

#----------------------------------------------------------------------------#
# Systems
#----------------------------------------------------------------------------#

@app.route('/addsystem', methods=['GET', 'POST'])
@basic_auth.required
def addsystem():
    thetime = time.strftime("%H:%M")
    today = date.today()
    if request.method == 'POST':
        s = System(serialsystem = request.form['serialsystem'], location = request.form['location'], fsrpoc = request.form['fsrpoc'])
        db.session.add(s)
        s1 = Subsystem(system_id = request.form['serialsystem'], sub_type = request.form['sub_type1'], firmware = request.form['firmware1'],\
            software = request.form['software1'], serialsub = request.form['serialsub1'])
        db.session.add(s1)
        s2 = Subsystem(system_id = request.form['serialsystem'], sub_type = request.form['sub_type2'], firmware = request.form['firmware2'],\
            software = request.form['software2'], serialsub = request.form['serialsub2'])
        db.session.add(s2)
        s3 = Subsystem(system_id = request.form['serialsystem'], sub_type = request.form['sub_type3'], firmware = request.form['firmware3'],\
            software = request.form['software3'], serialsub = request.form['serialsub3'])
        db.session.add(s3)
        s4 = Subsystem(system_id = request.form['serialsystem'], sub_type = request.form['sub_type4'], firmware = request.form['firmware4'],\
            software = request.form['software4'], serialsub = request.form['serialsub4'])
        db.session.add(s2)
        db.session.commit()
        flash("Success!")
    return render_template('pages/addsystem.html', thetime = thetime, today = today)

@app.route('/systems', methods=['GET', 'POST'])
@basic_auth.required
def systems():
    thetime = time.strftime("%H:%M")
    today = date.today()
    if request.method=='GET':
        return render_template('pages/systemsearch.html', thetime = thetime, today = today)

    else: #POST REQUEST
        if request.form['product'] == "MTGR":
            sys = Subsystem.query.filter_by(sub_type = "MTGR", serialsub = request.form['serial']).first_or_404()
            print sys.sub_type
            print sys.serialsub
        elif request.form['product'] == "ROCU":
            sys = Subsystem.query.filter_by(sub_type = "ROCU", serialsub = request.form['serial']).first_or_404()
            print sys.sub_type
            print sys.serialsub
        elif request.form['product'] == "Manipulator":
            sys = Subsystem.query.filter_by(sub_type = "Manipulator", serialsub = request.form['serial']).first_or_404()
            print sys.sub_type
            print sys.serialsub
        elif request.form['product'] == "MPU":
            sys = Subsystem.query.filter_by(sub_type = "MPU", serialsub = request.form['serial']).first_or_404()
            print sys.sub_type
            print sys.serialsub
        elif request.form['product'] == "System":
            
            return redirect('/systemdetail/'+request.form['serial'])
        else: 
            pass
        return render_template('pages/systemdetail.html', sys = sys, thetime = thetime, today = today)
    pass



@app.route('/deletesystem/<int:sys>', methods=['POST'])
@basic_auth.required
def deletesystem(sys):

    s = System.query.filter_by(serialsystem = sys).first_or_404()
    db.session.delete(s)
    db.session.commit()
    flash("Deleted!")
    return redirect('viewsystems')

@app.route('/systemdetail/<sys>')
@basic_auth.required
def systemdetail(sys):
    thetime = time.strftime("%H:%M")
    today = date.today()
    rocu = Subsystem.query.filter_by(sub_type = "ROCU", system_id = sys).first_or_404()
    mpu = Subsystem.query.filter_by(sub_type = "MPU", system_id = sys).first_or_404()
    mtgr = Subsystem.query.filter_by(sub_type = "MTGR", system_id = sys).first_or_404()
    manipulator = Subsystem.query.filter_by(sub_type = "Manipulator", system_id = sys).first_or_404()
    system = System.query.filter_by(serialsystem = sys).first_or_404()
    return render_template('pages/fullsystemdetail.html', rocu = rocu, mpu = mpu, mtgr = mtgr, manipulator = manipulator, system = system, thetime = thetime, today = today)

@app.route('/viewsystem/<sid>', methods=['GET', 'POST'])
@basic_auth.required
def viewsystem(s):
    pass
    s = System.query.all()
    for system in s:
        system.parts = system.parts.split(',')
        system.filename = system.filename.split(',')

    subsys = Subsystem.query.all()
    parts = Parts.query.all()
    return render_template('pages/viewsystems.html', s = s, subsys = subsys, parts = parts)

@app.route('/editsystem/<int:sys>', methods = ['POST'])
@basic_auth.required
def editsystem(sys):
    s = System.query.filter_by(serialsystem = sys).first_or_404()
    s.serialsystem = request.form['serialsystem']
    s.location = request.form['location']
    s.fsrpoc = request.form['fsrpoc']
    s.filename = s.filename
    db.session.add(s)
    db.session.commit()
    flash("Updated!")
    return redirect('/viewsystems')

@app.route('/addsysimage/<int:sys>', methods = ['POST'])
@basic_auth.required
def addsysimage(sys):

    today = date.today()
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'] + today)
    except:
        pass
    s = System.query.filter_by(serialsystem = str(sys)).first_or_404()
    # print s.serialsystem
    # print request.files['file']
    filesys = request.files['file']
    # print filesys.filename
    if filesys:
        # print "file check pass"
        # print filesys.filename
        filename = secure_filename(filesys.filename)
        filesys.save(os.path.join(app.config['UPLOAD_FOLDER'] + str(today), filename))
        s.filename += filename + ","
    db.session.add(s)
    db.session.commit()
    flash("Added image!")
    return redirect('/viewsystems')


#----------------------------------------------------------------------------#
# Sub Systems
#----------------------------------------------------------------------------#

@app.route('/addsub', methods=['GET', 'POST'])
@basic_auth.required
def addsub():
    thetime = time.strftime("%H:%M")
    today = date.today()
    return render_template('pages/addsub.html', thetime = thetime, today = today)

@app.route('/subedit/<int:sys>', methods = ['POST'])
@basic_auth.required
def subedit(sys):
    s = Subsystem.query.filter_by(system_id = sys).first_or_404()
    s.serialsub = request.form['serialsub']
    s.firmware = request.form['firmware']
    s.software = request.form['software']
    db.session.add(s)
    db.session.commit()
    flash("Updated!")
    return redirect('/viewsystems')

@app.route('/viewsub/<int:sys>')
@basic_auth.required
def viewsub(sys):
    thetime = time.strftime("%H:%M")
    today = date.today()
    s = Subsystem.query.filter_by(serialsub = sys).first_or_404()
    return render_template('pages/viewsub.html', s = s, thetime = thetime, today = today)



#----------------------------------------------------------------------------#
# Manuals
#----------------------------------------------------------------------------#


@app.route('/mtgrusermanual')
#MTGR User manual
def mtgrusermanual():
    return redirect('/static/User_Manual.pdf')

@app.route('/gta')
#MTGR GTA
def gta():
    return redirect('/static/GTA.pdf')

@app.route('/maintmanual')
#MTGR Maintenance Manual
def maintmanual():
    return redirect('/static/maintmanual.pdf')


#----------------------------------------------------------------------------#
# Parts
#----------------------------------------------------------------------------#

@app.route('/addpart', methods = ['GET', 'POST'])
@basic_auth.required
def addpart():
    thetime = time.strftime("%H:%M")
    today = date.today()
    if request.method == 'POST':
        p = Parts(invid = request.form['invid'], name = request.form['name'], num = request.form['num'], serial = request.form['serial'],\
            note = request.form['note'], price = request.form['price'], quan = request.form['quan'], location = request.form['location'],\
            low_stock = request.form['low_stock'])
        db.session.add(p)
        flash('Success!')
        db.session.commit()

    return render_template('pages/addpart.html', thetime = thetime, today = today)

@app.route('/viewparts')
@basic_auth.required
def viewparts():
    thetime = time.strftime("%H:%M")
    today = date.today()
    parts = Parts.query.all()
    return render_template('pages/viewparts.html', parts = parts, thetime = thetime, today = today)

#----------------------------------------------------------------------------#
# Service Calls
#----------------------------------------------------------------------------#

def sendsms(ticket):
    sms = boto.sns.SNSConnection()
    message = "Ticket "+str(ticket)+" was created on Bot Log. http://107.21.186.10/calldetail/"+str(ticket)
    sms.publish("arn:aws:sns:us-east-1:645348986379:bot-log",message)

def myvalidate(serial, product):
    system = System.query.all()
    for each in system:
        if product == "System":
            if serial == each.serialsystem:
                return True
                break
    subs = Subsystem.query.all()
    for each in subs:
        if product == each.sub_type:
            if serial == each.serialsub:
                return True


@app.route('/addcall', methods = ['GET', 'POST'])
def addcall():
    thetime = time.strftime("%H:%M")
    today = date.today()
    if request.method =='POST':
        if myvalidate(request.form['serial'], request.form['product']):
            

            filesup = ""

            try:
                os.makedirs(app.config['UPLOAD_FOLDER'] + str(today))
            except:
                pass

            if request.files['file'] != "":
                filesys = request.files['file']
                filename = secure_filename(filesys.filename)
            if request.files['file2'] != "":
                file2 = request.files['file2']
                filetwo = secure_filename(file2.filename)
            if request.files['file3'] != "":
                file3 = request.files['file3']
                filethree = secure_filename(file3.filename)
            if request.files['wcf'] != "":
                wcf = request.files['wcf']
                wcform = secure_filename(wcf.filename)

            if filename != "":
                filesys.save(os.path.join(app.config['UPLOAD_FOLDER'] + str(today), filename))
                filesup += filename + ","
            if filetwo != "":
                file2.save(os.path.join(app.config['UPLOAD_FOLDER'] + str(today), filetwo))
                filesup += filetwo + ","
            if filethree != "":
                file3.save(os.path.join(app.config['UPLOAD_FOLDER'] + str(today), filethree))
                filesup += filethree + ","
            if wcform != "":
                wcf.save(os.path.join(app.config['UPLOAD_FOLDER'] + str(today), wcform))
                filesup += wcform + ","
            # filename = filename + "," + filetwo + "," + filethree + ","
            s = ServiceCall(location = request.form['location'], who = request.form['who'],\
                phone = request.form['phone'], email = request.form['email'], org = request.form['org'],\
                serial = request.form['serial'], env = request.form['env'], product = request.form['product'],\
                ptype = request.form['ptype'], date = today, time = thetime,\
                problem = request.form['problem'], filename = filesup)
            
            db.session.add(s)
            db.session.commit()
            # sendsms(s.ticket)
        else:
            flash('Please enter a valid serial number!')
            return render_template('pages/addcall.html', thetime = thetime, today = today)

        flash('Service Call sent! Please wait for a response.')
        return render_template('pages/addcall.html', thetime = thetime, today = today)

    return render_template('pages/addcall.html', thetime = thetime, today = today)

@app.route('/viewcall', methods=['GET', 'POST'])
@basic_auth.required
def viewcall():
    thetime = time.strftime("%H:%M")
    today = date.today()
    servicecall = ServiceCall.query.all()
    s = System.query.all()
    for call in servicecall:
        if type(call.filename) is not NoneType:
            call.filename = call.filename.split(',')
    robot = Subsystem.query.filter_by(sub_type = "Robot")
    r = Subsystem.query.filter_by(sub_type = "ROCU")
    return render_template('pages/viewcall.html', servicecall = servicecall, s = s, robot = robot, r = r, thetime = thetime, today = today)

@app.route('/viewcallsort/', methods=['POST'])
@basic_auth.required
def filterstatus():
    thetime = time.strftime("%H:%M")
    today = date.today()
    fil = request.form['filterstatus']
    print fil
    if fil == "1":
        servicecall = ServiceCall.query.filter_by(status = "1")
        s = System.query.all()
        robot = Subsystem.query.filter_by(sub_type = "Robot")
        r = Subsystem.query.filter_by(sub_type = "ROCU")
        for call in servicecall:
            call.filename = call.filename.split(',')
        return render_template('pages/viewcall.html', servicecall = servicecall, s = s, robot = robot, r = r, thetime = thetime, today = today)
    elif fil == "2":
        servicecall = ServiceCall.query.filter_by(status = "2")
        s = System.query.all()
        robot = Subsystem.query.filter_by(sub_type = "Robot")
        r = Subsystem.query.filter_by(sub_type = "ROCU")
        for call in servicecall:
            call.filename = call.filename.split(',')
        return render_template('pages/viewcall.html', servicecall = servicecall, s = s, robot = robot, r = r, thetime = thetime, today = today)
    else:
        servicecall = ServiceCall.query.filter_by(status = "3")
        s = System.query.all()
        robot = Subsystem.query.filter_by(sub_type = "Robot")
        r = Subsystem.query.filter_by(sub_type = "ROCU")
        for call in servicecall:
            call.filename = call.filename.split(',')
        return render_template('pages/viewcall.html', servicecall = servicecall, s = s, robot = robot, r = r, thetime = thetime, today = today)

@app.route('/editsolution/<int:sys>', methods = ['POST'])
@basic_auth.required
def editsolution(sys):
    call = ServiceCall.query.filter_by(sysnum = sys).first_or_404()
    call.solution = request.form['solution']
    db.session.add(call)
    db.session.commit()
    flash('Solution Updated')
    return redirect('/viewcall')

@app.route('/callfile/<int:ticket>', methods=['POST'])
@basic_auth.required
def callfile(ticket):
    today = date.today()
    if request.method == 'POST':
        sc = ServiceCall.query.filter_by(ticket = ticket).first_or_404()
        print sc.ticket
        print request.files['file']
        filesys = request.files['file']
        print filesys.filename
        if filesys:
            print "file check pass"
            print filesys.filename
            filename = secure_filename(filesys.filename)
            try:
                os.makedirs(app.config['UPLOAD_FOLDER'] + today)
            except:
                pass
            filesys.save(os.path.join(app.config['UPLOAD_FOLDER'] + str(today), filename))
            sc.filename += filename + ","
        db.session.add(sc)
        db.session.commit()
        flash("Added image!")
        return redirect('/viewcall')

@app.route('/editcall/<ticket>', methods=['POST'])
@basic_auth.required
def editcall(ticket):
    today = date.today()
    sc = ServiceCall.query.filter_by(ticket = ticket).first_or_404()
    print 'ticket found'
    # print sc.location
    sc.location = request.form['location']
    sc.who = request.form['who']
    sc.phone = request.form['phone']
    sc.email = request.form['email']
    sc.org = request.form['org']
    sc.serial  = request.form['serial']
    sc.env = request.form['env']
    sc.product = request.form['product']
    sc.ptype = request.form['ptype']
    sc.problem = request.form['problem']
    # sc.solution = request.form['solution']
    sc.status = request.form['status']
    sc.statusdate = today
    print 'form done'
    # sc.solution = request.form['solution']
    db.session.add(sc)
    db.session.commit()
    # flash('updated!')
    return redirect('/calldetail/'+str(ticket))    
@app.route('/deletecall/<int:ticket>', methods = ['POST'])
@basic_auth.required
def deletecall(ticket):
    call = ServiceCall.query.filter_by(ticket = ticket).first_or_404()
    db.session.delete(call)
    db.session.commit()
    flash("Deleted!")
    return redirect('/viewcall')

@app.route('/calldetail/<int:ticket>', methods = ['GET', 'POST'])
@basic_auth.required
def calldetail(ticket):
    thetime = time.strftime("%H:%M")
    today = date.today()

    call = ServiceCall.query.filter_by(ticket = ticket).first_or_404()
    old = ServiceCall.query.filter_by(serial = call.serial)

    if request.method == 'POST': # if parts form used
        # print request.args.getlist(asdf)
        parts = Parts.query.all()
        for part in parts:
            part.quan = int(part.quan) - int(request.form[part.name])
            if request.form[part.name] != "0":
                if call.product == "System":
                    system = System.query.filter_by(serialsystem = call.serial).first()
                    system.partsused += "Used " + str(request.form[part.name]) + " " + str(part.name) + " on " + str(today) + ", "
                else:
                    subsystem = Subsystem.query.filter_by(sub_type = call.product, serialsub = call.serial).first()
                    subsystem.partsused += "Used " + str(request.form[part.name]) + " " + str(part.name) + " on " + str(today) + ", "
                 
                call.partsused += "Used " + str(request.form[part.name]) + " " + str(part.name) + " on " + str(today) + ", "
            db.session.commit()
        print call.partsused
            # print part.name + "-" + str(request.form[part.name])
            # part.quan -= int(request.form[part.name])
        # parts = Parts.query.all()
        # for part in parts:
        #     for each in range(0,len(parts)):
        #         print part.name + "-" + request.form['asdf'+str(each)]
        # print request.form['sdfg']
        # for part in parts:
        #     if part.id == request.form[part.id]:
        #         print request.form[part.id]
            # # thename = request.form[part.name]
            # # print thename
            # uname = str(request.form[part.name]+"-"+request.form[part.quan])
            # print uname
            # # print request.form[part.name,'-',part.quan]
            # # print request.form[part.quan]

            # # print part.name
            # # print part.invid
            # # print request.form[part.name]

            # # print request.form[part.name]

    call = ServiceCall.query.filter_by(ticket = ticket).first_or_404()
    old = ServiceCall.query.filter_by(serial = call.serial)
    call.postauthor = call.postauthor.split(',')
    call.postmessage = call.postmessage.split(',')
    call.postdate = call.postdate.split(',')
    call.posttime = call.posttime.split(',')
    # call.filename = call.filename.split(',')
    parts = Parts.query.all()


    if call.filename != "":
        call.filename = call.filename.split(',')
    a = 0
    return render_template('/pages/calldetail.html', call = call, old = old, parts = parts, thetime = thetime, today = today, a = a)

@app.route('/callmsgpost/<int:ticket>', methods =['POST'])
@basic_auth.required
def callmsgpost(ticket):
    today = date.today()
    thetime = time.strftime("%H:%M")
    if request.method == 'POST':
        # call = ServiceCall.query.filter_by(ticket = ticket).first_or_404()
        
        call = ServiceCall.query.filter_by(ticket = ticket).first_or_404()
        call.totalmessages += 1
        call.postauthor += request.authorization.username + ","
        call.postmessage += request.form['message'] + ","
        call.postdate += str(today) + ","
        call.posttime += str(thetime) + ","
        db.session.add(call)
        db.session.commit()
        return redirect('calldetail/'+str(ticket))

@app.route('/callfileup/<int:ticket>', methods = ['POST'])
@basic_auth.required
def callfileup(ticket):
    today = date.today()
    if request.method == 'POST':
        sc = ServiceCall.query.filter_by(ticket = ticket).first_or_404()
        print sc.ticket
        print request.files['file']
        filesys = request.files['file']
        print filesys.filename
        if filesys:
            print "file check pass"
            print filesys.filename
            filename = secure_filename(filesys.filename)
            try:
                os.makedirs(app.config['UPLOAD_FOLDER'] + today)
            except:
                pass
            filesys.save(os.path.join(app.config['UPLOAD_FOLDER'] + str(today), filename))
            sc.filename += filename + ","
        db.session.add(sc)
        db.session.commit()
        flash("Added image!")
        return redirect('calldetail/'+ str(ticket))



#----------------------------------------------------------------------------#
# Reports
#----------------------------------------------------------------------------#

@app.route('/weeklyreport')
@basic_auth.required
def weeklyreport():
    thetime = time.strftime("%H:%M")
    today = date.today()

    tickets = ServiceCall.query.all()
    systems = System.query.all()
    return render_template('pages/reports/weekly.html', tickets = tickets, systems = systems, thetime = thetime, today = today)
    # return render_template('pages/viewwcf.html', wcf = wcf)

@app.route('/monthlyreport')
@basic_auth.required
def monthlyreport():
    thetime = time.strftime("%H:%M")
    today = date.today()

    tickets = ServiceCall.query.all()
    systems = System.query.all()
    return render_template('pages/reports/monthly.html', tickets = tickets, systems = systems, thetime = thetime, today = today)
    # return render_template('pages/addwcf.html')

@app.route('/statusreport')
@basic_auth.required
def statusreport():
    thetime = time.strftime("%H:%M")
    today = date.today()

    tickets = ServiceCall.query.all()
    systems = System.query.all()


    return render_template('pages/reports/status.html', tickets = tickets, systems = systems, thetime = thetime, today = today)



#----------------------------------------------------------------------------#
# ADMIN STUFF
#----------------------------------------------------------------------------#

@app.route('/ticketqueue')
@basic_auth.required
def ticketqueue():
    thetime = time.strftime("%H:%M")
    today = date.today()

    tickets = ServiceCall.query.filter_by(status = "4").all()
    for each in tickets:
        print each
    return render_template('pages/ticketqueue.html', tickets = tickets, thetime = thetime, today = today)


#----------------------------------------------------------------------------#
# Surveys
#----------------------------------------------------------------------------#


# FSR CREATES NEW UNIQUE LOGIN FOR HIS CLASS
@app.route('/newsurvey', methods = ['GET', 'POST'])
@basic_auth.required
def newsurvey():
    thetime = time.strftime("%H:%M")
    today = date.today()


    if request.method == 'POST':
        check = SurveyMaster.query.all()
        for each in check:
            if each.key == request.form['key']:
                flash("Try another key.")
                return render_template('pages/survey/new.html', thetime = thetime, today = today)
        survey = SurveyMaster(key = request.form['key'], date = today)
        db.session.add(survey)
        db.session.commit()
        flash("Added new key.  Happy surveying!")
        # else:
        #     flash("Key Taken! Try a different one!")

        
    return render_template('pages/survey/new.html', thetime = thetime, today = today)


@app.route('/survey/check', methods = ['POST'])
def surveycheck():
    thetime = time.strftime("%H:%M")
    today = date.today()

    if request.method == 'POST':
        s = SurveyMaster.query.filter_by(key = request.form['key']).first()
        if type(s) is not NoneType:
            if s.key == request.form['key']:
                return redirect('/completesurvey/start/' + s.key)
        else:
            print "Failed"
            flash("Try again!")
            return render_template('pages/survey/complete.html', thetime = thetime, today = today)

# CLASS LOGS IN WITH UNIQUE CODE
@app.route('/completesurvey')
def completesurvey():
    thetime = time.strftime("%H:%M")
    today = date.today()
    return render_template('pages/survey/complete.html', thetime = thetime, today = today)
        

# FSR AND HIGHER CAN SEE RESULTS IE: NUMBER COMPLETED, FEEDBACK, STATS ETC
@app.route('/viewsurvey', methods = ['GET', 'POST'])
@basic_auth.required
def viewsurvey():
    surveys = SurveyMaster.query.all()
    thetime = time.strftime("%H:%M")
    today = date.today()
    return render_template('pages/survey/view.html', thetime = thetime, today = today, surveys = surveys)

@app.route('/completed/<key>')
@basic_auth.required
def completedsurveys(key):
    thetime = time.strftime("%H:%M")
    today = date.today()

    chart1, chart2, chart3 = PieChart2D(350, 100), PieChart2D(350, 100), PieChart2D(350, 100)
    chart4, chart5, chart6 = PieChart2D(350, 100), PieChart2D(350, 100), PieChart2D(350, 100)
    chart7, chart8, chart9 = PieChart2D(350, 100), PieChart2D(350, 100), PieChart2D(350, 100)
    chart10, chart11, chart12 = PieChart2D(350, 100), PieChart2D(350, 100), PieChart2D(350, 100)
    chart13, chart14, chart15 = PieChart2D(350, 100), PieChart2D(350, 100), PieChart2D(350, 100)
    chart16, chart17, chart18 = PieChart2D(350, 100), PieChart2D(350, 100), PieChart2D(350, 100)
    chart19, chart20, chart21 = PieChart2D(350, 100), PieChart2D(350, 100), PieChart2D(350, 100)
    chart22, chart23, chart24, chart25 = PieChart2D(350, 100), PieChart2D(350, 100), PieChart2D(350, 100), PieChart2D(350, 100)
    

    surveys = Survey.query.filter_by(key = key).all()
    if type(surveys) is type(NoneType):
        flash("No entries yet.")
        return redirect('/viewsurvey')
  
    # question1, question2, question3, question4, question5, question6, question7 = 0, 0, 0, 0, 0, 0, 0
    # question8, question9, question10, question11, question12, question13, question14 = 0, 0, 0, 0, 0, 0, 0
    # question15, question16, question17, question18, question19, question20, question21 = 0, 0, 0, 0, 0, 0, 0
    # question22, question23, question24, question25 = 0, 0, 0, 0 
    total = 0

    q1sa, q1a, q1no, q1d, q1sd = 0, 0, 0, 0, 0
    q2sa, q2a, q2no, q2d, q2sd = 0, 0, 0, 0, 0
    q3sa, q3a, q3no, q3d, q3sd = 0, 0, 0, 0, 0
    q4sa, q4a, q4no, q4d, q4sd = 0, 0, 0, 0, 0
    q5sa, q5a, q5no, q5d, q5sd = 0, 0, 0, 0, 0
    q6sa, q6a, q6no, q6d, q6sd = 0, 0, 0, 0, 0
    q7sa, q7a, q7no, q7d, q7sd = 0, 0, 0, 0, 0
    q8sa, q8a, q8no, q8d, q8sd = 0, 0, 0, 0, 0
    q9sa, q9a, q9no, q9d, q9sd = 0, 0, 0, 0, 0
    q10sa, q10a, q10no, q10d, q10sd = 0, 0, 0, 0, 0
    q11sa, q11a, q11no, q11d, q11sd = 0, 0, 0, 0, 0
    q12sa, q12a, q12no, q12d, q12sd = 0, 0, 0, 0, 0
    q13sa, q13a, q13no, q13d, q13sd = 0, 0, 0, 0, 0
    q14sa, q14a, q14no, q14d, q14sd = 0, 0, 0, 0, 0
    q15sa, q15a, q15no, q15d, q15sd = 0, 0, 0, 0, 0
    q16sa, q16a, q16no, q16d, q16sd = 0, 0, 0, 0, 0
    q17sa, q17a, q17no, q17d, q17sd = 0, 0, 0, 0, 0
    q18sa, q18a, q18no, q18d, q18sd = 0, 0, 0, 0, 0
    q19sa, q19a, q19no, q19d, q19sd = 0, 0, 0, 0, 0
    q20sa, q20a, q20no, q20d, q20sd = 0, 0, 0, 0, 0
    q21sa, q21a, q21no, q21d, q21sd = 0, 0, 0, 0, 0
    q22sa, q22a, q22no, q22d, q22sd = 0, 0, 0, 0, 0
    q23sa, q23a, q23no, q23d, q23sd = 0, 0, 0, 0, 0
    q24sa, q24a, q24no, q24d, q24sd = 0, 0, 0, 0, 0
    q25sa, q25a, q25no, q25d, q25sd = 0, 0, 0, 0, 0
    q1p, q2p, q3p, q4p, q5p = 0, 0, 0, 0, 0
    q6p, q7p, q8p, q9p, q10p = 0, 0, 0, 0, 0
    q11p, q12p, q13p, q14p, q15p = 0, 0, 0, 0, 0
    q16p, q17p, q18p, q19p, q20p = 0, 0, 0, 0, 0
    q21p, q22p, q23p, q24p, q25p = 0, 0, 0, 0, 0

    for survey in surveys:
        
        if survey.q1 == "2":
            q1sa += 1
            q1p += 1
        elif survey.q1 == "1":
            q1a += 1
            q1p += 1
        elif survey.q1 == "0":
            q1no += 1
        elif survey.q1 == "-1":
            q1d += 1
        else:
            q1sd += 1

        if survey.q2 == "2":
            q2sa += 1
            q2p += 1
        elif survey.q2 == "1":
            q2a += 1
            q2p += 1
        elif survey.q2 == "0":
            q2no += 1
        elif survey.q2 == "-1":
            q2d += 1
        else:
            q2sd += 1

        if survey.q3 == "2":
            q3sa += 1
            q3p += 1
        elif survey.q3 == "1":
            q3a += 1
            q3p += 1
        elif survey.q3 == "0":
            q3no += 1
        elif survey.q3 == "-1":
            q3d += 1
        else:
            q3sd += 1

        if survey.q4 == "2":
            q4sa += 1
            q4p += 1
        elif survey.q4 == "1":
            q4a += 1
            q4p += 1
        elif survey.q4 == "0":
            q4no += 1
        elif survey.q4 == "-1":
            q4d += 1
        else:
            q4sd += 1

        if survey.q5 == "2":
            q5sa += 1
            q5p += 1
        elif survey.q5 == "1":
            q5a += 1
            q5p += 1
        elif survey.q5 == "0":
            q5no += 1
        elif survey.q5 == "-1":
            q5d += 1
        else:
            q5sd += 1

        if survey.q6 == "2":
            q6sa += 1
            q6p += 1
        elif survey.q6 == "1":
            q6a += 1
            q6p += 1
        elif survey.q6 == "0":
            q6no += 1
        elif survey.q6 == "-1":
            q6d += 1
        else:
            q6sd += 1

        if survey.q7 == "2":
            q7sa += 1
            q7p += 1
        elif survey.q7 == "1":
            q7a += 1
            q7p += 1
        elif survey.q7 == "0":
            q7no += 1
        elif survey.q7 == "-1":
            q7d += 1
        else:
            q7sd += 1

        if survey.q8 == "2":
            q8sa += 1
            q8p += 1
        elif survey.q8 == "1":
            q8a += 1
            q8p += 1
        elif survey.q8 == "0":
            q8no += 1
        elif survey.q8 == "-1":
            q8d += 1
        else:
            q8sd += 1

        if survey.q9 == "2":
            q9sa += 1
            q9p += 1
        elif survey.q9 == "1":
            q9a += 1
            q9p += 1
        elif survey.q9 == "0":
            q9no += 1
        elif survey.q9 == "-1":
            q9d += 1
        else:
            q9sd += 1

        if survey.q10 == "2":
            q10sa += 1
            q10p += 1
        elif survey.q10 == "1":
            q10a += 1
            q10p += 1
        elif survey.q10 == "0":
            q10no += 1
        elif survey.q10 == "-1":
            q10d += 1
        else:
            q10sd += 1

        if survey.q11 == "2":
            q11sa += 1
            q11p += 1
        elif survey.q11 == "1":
            q11a += 1
            q11p += 1
        elif survey.q11 == "0":
            q11no += 1
        elif survey.q11 == "-1":
            q11d += 1
        else:
            q11sd += 1

        if survey.q12 == "2":
            q12sa += 1
            q12p += 1
        elif survey.q12 == "1":
            q12a += 1
            q12p += 1
        elif survey.q12 == "0":
            q12no += 1
        elif survey.q12 == "-1":
            q12d += 1
        else:
            q12sd += 1

        if survey.q13 == "2":
            q13sa += 1
            q13p += 1
        elif survey.q13 == "1":
            q13a += 1
            q13p += 1
        elif survey.q13 == "0":
            q13no += 1
        elif survey.q13== "-1":
            q13d += 1
        else:
            q13sd += 1

        if survey.q14 == "2":
            q14sa += 1
            q14p += 1
        elif survey.q14 == "1":
            q14a += 1
            q14p += 1
        elif survey.q14 == "0":
            q14no += 1
        elif survey.q14 == "-1":
            q14d += 1
        else:
            q14sd += 1

        if survey.q15 == "2":
            q15sa += 1
            q15p += 1
        elif survey.q15 == "1":
            q15a += 1
            q15p += 1
        elif survey.q15 == "0":
            q15no += 1
        elif survey.q15 == "-1":
            q15d += 1
        else:
            q15sd += 1

        if survey.q16 == "2":
            q16sa += 1
            q16p += 1
        elif survey.q16 == "1":
            q16a += 1
            q16p += 1
        elif survey.q16 == "0":
            q16no += 1
        elif survey.q16 == "-1":
            q16d += 1
        else:
            q16sd += 1

        if survey.q17 == "2":
            q17sa += 1
            q17p += 1
        elif survey.q17 == "1":
            q17a += 1
            q17p += 1
        elif survey.q17 == "0":
            q17no += 1
        elif survey.q17 == "-1":
            q17d += 1
        else:
            q17sd += 1

        if survey.q18 == "2":
            q18sa += 1
            q18p += 1
        elif survey.q18 == "1":
            q18a += 1
            q18p += 1
        elif survey.q18 == "0":
            q18no += 1
        elif survey.q18 == "-1":
            q18d += 1
        else:
            q18sd += 1

        if survey.q19 == "2":
            q19sa += 1
            q19p +=1 
        elif survey.q19 == "1":
            q19a += 1
            q19p += 1
        elif survey.q19 == "0":
            q19no += 1
        elif survey.q19 == "-1":
            q19d += 1
        else:
            q19sd += 1

        if survey.q20 == "2":
            q20sa += 1
            q20p += 1
        elif survey.q20 == "1":
            q20a += 1
            q20p += 1
        elif survey.q20 == "0":
            q20no += 1
        elif survey.q20 == "-1":
            q20d += 1
        else:
            q20sd += 1

        if survey.q21 == "2":
            q21sa += 1
            q21p += 1
        elif survey.q21 == "1":
            q21a += 1
            q21p += 1
        elif survey.q21 == "0":
            q21no += 1
        elif survey.q21 == "-1":
            q21d += 1
        else:
            q21sd += 1

        if survey.q22 == "2":
            q22sa += 1
            q22p += 1
        elif survey.q22 == "1":
            q22a += 1
            q22p += 1
        elif survey.q22 == "0":
            q22no += 1
        elif survey.q22 == "-1":
            q22d += 1
        else:
            q22sd += 1

        if survey.q23 == "2":
            q23sa += 1
            q23p += 1
        elif survey.q23 == "1":
            q23a += 1
            q23p += 1
        elif survey.q23 == "0":
            q23no += 1
        elif survey.q23 == "-1":
            q23d += 1
        else:
            q23sd += 1

        if survey.q24 == "2":
            q24sa += 1
            q24p += 1
        elif survey.q24 == "1":
            q24a += 1
            q24p += 1
        elif survey.q24 == "0":
            q24no += 1
        elif survey.q24 == "-1":
            q24d += 1
        else:
            q24sd += 1

        if survey.q25 == "2":
            q25sa += 1
            q25p += 1
        elif survey.q25 == "1":
            q25a += 1
            q25p += 1
        elif survey.q25 == "0":
            q25no += 1
        elif survey.q25 == "-1":
            q25d += 1
        else:
            q25sd += 1



        total += 1

    try:
        q1avg = str("%.2f" % ((float(q1p) / float(total)) * 100))
    except:
        flash("No entries submitted for this survey yet.")
        return redirect('/viewsurvey')
    q2avg = str("%.2f" % ((float(q2p) / float(total)) * 100))
    q3avg = str("%.2f" % ((float(q3p) / float(total)) * 100))
    q4avg = str("%.2f" % ((float(q4p) / float(total)) * 100))
    q5avg = str("%.2f" % ((float(q5p) / float(total)) * 100))
    q6avg = str("%.2f" % ((float(q6p) / float(total)) * 100))
    q7avg = str("%.2f" % ((float(q7p) / float(total)) * 100))
    q8avg = str("%.2f" % ((float(q8p) / float(total)) * 100))
    q9avg = str("%.2f" % ((float(q9p) / float(total)) * 100))
    q10avg = str("%.2f" % ((float(q10p) / float(total)) * 100))
    q11avg = str("%.2f" % ((float(q11p) / float(total)) * 100))
    q12avg = str("%.2f" % ((float(q12p) / float(total)) * 100))
    q13avg = str("%.2f" % ((float(q13p) / float(total)) * 100))
    q14avg = str("%.2f" % ((float(q14p) / float(total)) * 100))
    q15avg = str("%.2f" % ((float(q15p) / float(total)) * 100))
    q16avg = str("%.2f" % ((float(q16p) / float(total)) * 100))
    q17avg = str("%.2f" % ((float(q17p) / float(total)) * 100))
    q18avg = str("%.2f" % ((float(q18p) / float(total)) * 100))
    q19avg = str("%.2f" % ((float(q19p) / float(total)) * 100))
    q20avg = str("%.2f" % ((float(q20p) / float(total)) * 100))
    q21avg = str("%.2f" % ((float(q21p) / float(total)) * 100))
    q22avg = str("%.2f" % ((float(q22p) / float(total)) * 100))
    q23avg = str("%.2f" % ((float(q23p) / float(total)) * 100))
    q24avg = str("%.2f" % ((float(q24p) / float(total)) * 100))
    q25avg = str("%.2f" % ((float(q25p) / float(total)) * 100))
    

    chart1.add_data([q1sa, q1a, q1no, q1d, q1sd])
    chart1.set_colours
    chart2.add_data([q2sa, q2a, q2no, q2d, q2sd])
    chart3.add_data([q3sa, q3a, q3no, q3d, q3sd])
    chart4.add_data([q4sa, q4a, q4no, q4d, q4sd])
    chart5.add_data([q5sa, q5a, q5no, q5d, q5sd])
    chart6.add_data([q6sa, q6a, q6no, q6d, q6sd])
    chart7.add_data([q7sa, q7a, q7no, q7d, q7sd])
    chart8.add_data([q8sa, q8a, q8no, q8d, q8sd])
    chart9.add_data([q9sa, q9a, q9no, q9d, q9sd])
    chart10.add_data([q10sa, q10a, q10no, q10d, q10sd])
    chart11.add_data([q11sa, q11a, q11no, q11d, q11sd])
    chart12.add_data([q12sa, q12a, q12no, q12d, q12sd])
    chart13.add_data([q13sa, q13a, q13no, q13d, q13sd])
    chart14.add_data([q14sa, q14a, q14no, q14d, q14sd])
    chart15.add_data([q15sa, q15a, q15no, q15d, q15sd])
    chart16.add_data([q16sa, q16a, q16no, q16d, q16sd])
    chart17.add_data([q17sa, q17a, q17no, q17d, q17sd])
    chart18.add_data([q18sa, q18a, q18no, q18d, q18sd])
    chart19.add_data([q19sa, q19a, q19no, q19d, q19sd])
    chart20.add_data([q20sa, q20a, q20no, q20d, q20sd])
    chart21.add_data([q21sa, q21a, q21no, q21d, q21sd])
    chart22.add_data([q22sa, q22a, q22no, q22d, q22sd])
    chart23.add_data([q23sa, q23a, q23no, q23d, q23sd])
    chart24.add_data([q24sa, q24a, q24no, q24d, q24sd])
    chart25.add_data([q25sa, q25a, q25no, q25d, q25sd])

    chart1.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart2.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart3.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart4.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart5.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart6.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart7.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart8.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart9.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart10.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart11.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart12.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart13.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart14.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart15.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart16.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart17.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart18.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart19.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart20.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart21.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart22.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart23.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart24.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])
    chart25.set_pie_labels(['Strongly Agree', 'Agree', 'Not Observed', 'Disagree', 'Strongly Disagree'])

    chart1url = chart1.get_url()
    chart2url = chart2.get_url()
    chart3url = chart3.get_url()
    chart4url = chart4.get_url()
    chart5url = chart5.get_url()
    chart6url = chart6.get_url()
    chart7url = chart7.get_url()
    chart8url = chart8.get_url()
    chart9url = chart9.get_url()
    chart10url = chart10.get_url()
    chart11url = chart11.get_url()
    chart12url = chart12.get_url()
    chart13url = chart13.get_url()
    chart14url = chart14.get_url()
    chart15url = chart15.get_url()
    chart16url = chart16.get_url()
    chart17url = chart17.get_url()
    chart18url = chart18.get_url()
    chart19url = chart19.get_url()
    chart20url = chart20.get_url()
    chart21url = chart21.get_url()
    chart22url = chart22.get_url()
    chart23url = chart23.get_url()
    chart24url = chart24.get_url()
    chart25url = chart25.get_url()

    generalavg = str("%.2f" % (float((float(q1avg) + float(q2avg) + float(q3avg) + float(q4avg) + float(q5avg) + float(q6avg) + float(q7avg) + float(q8avg)) / 8)))
    featavg = str("%.2f" % (float((float(q9avg) + float(q10avg) + float(q11avg) + float(q12avg) + float(q13avg) + float(q14avg) + float(q15avg)) / 7)))
    ocuavg = str("%.2f" % (float((float(q16avg) + float(q17avg) + float(q18avg)) / 3)))
    manipavg = str("%.2f" % (float((float(q19avg) + float(q20avg)) / 2)))
    trainingavg = str("%.2f" % (float((float(q21avg) + float(q22avg) + float(q23avg) + float(q24avg) + float(q25avg)) / 5)))
    overall = str("%.2f" % (float(float(generalavg) + float(featavg) + float(ocuavg) + float(manipavg) + float(trainingavg)) / 5))

    

    return render_template('pages/survey/detail.html', thetime = thetime, today = today, chart1url = chart1url,  chart2url = chart2url, \
        chart3url = chart3url,  chart4url = chart4url,  chart5url = chart5url,  chart6url = chart6url,  chart7url = chart7url,\
        chart8url = chart8url,  chart9url = chart9url,  chart10url = chart10url,  chart11url = chart11url,  chart12url = chart12url,\
        chart13url = chart13url,  chart14url = chart14url,  chart15url = chart15url,  chart16url = chart16url,  chart17url = chart17url,\
        chart18url = chart18url,  chart19url = chart19url,  chart20url = chart20url,  chart21url = chart21url,  chart22url = chart22url,\
        chart23url = chart23url,  chart24url = chart24url,  chart25url = chart25url, q1avg = q1avg, q2avg = q2avg, q3avg = q3avg,\
        q4avg = q4avg, q5avg = q5avg, q6avg = q6avg, q7avg = q7avg, q8avg = q8avg, q9avg = q9avg, q10avg = q10avg, q11avg = q11avg,\
        q12avg = q12avg, q13avg = q13avg, q14avg = q14avg, q15avg = q15avg, q16avg = q16avg, q17avg = q17avg, q18avg = q18avg,\
        q19avg = q19avg, q20avg = q20avg, q21avg = q21avg, q22avg = q22avg, q23avg = q23avg, q24avg = q24avg, q25avg = q25avg,\
        generalavg = generalavg, featavg = featavg, ocuavg = ocuavg, manipavg = manipavg, trainingavg = trainingavg, overall = overall)


@app.route('/completesurvey/start/<key>', methods = ['GET', 'POST'])
def startsurvey(key):
    thetime = time.strftime("%H:%M")
    today = date.today()
    if request.method == 'POST':

        survey = Survey(key = key, name = request.form['name'], role = request.form['role'], unit = request.form['unit'],\
            location = request.form['location'], date = today, eodsof = request.form['eodsof'], thours = request.form['thours'],\
            fsr = request.form['fsr'], mdescript = request.form['mdescript'], terrain = request.form['terrain'], los = request.form['los'],\
            mesh = request.form['mesh'], manip = request.form['manip'], timeofday = request.form['timeofday'], q1 = request.form['q1'],\
            q2 = request.form['q2'], q3 = request.form['q3'], q4 = request.form['q4'], q5 = request.form['q5'], q6 = request.form['q6'],\
            q7 = request.form['q7'], q8 = request.form['q8'], q9 = request.form['q9'], q10 = request.form['q10'], q11 = request.form['q11'],\
            q12 = request.form['q12'], q13 = request.form['q13'], q14 = request.form['q14'], q15 = request.form['q15'], q16 = request.form['q16'],\
            q17 = request.form['q17'], q18 = request.form['q18'], q19 = request.form['q19'], q20 = request.form['q20'], q21 = request.form['q21'],\
            q22 = request.form['q22'], q23 = request.form['q23'], q24 = request.form['q24'], q25 = request.form['q25'],\
            comments = request.form['comments'])
        db.session.add(survey)
        db.session.commit()
        return redirect('/completesurvey/done')
    return render_template('pages/survey/start.html', key = key, thetime = thetime, today = today)

@app.route('/completesurvey/done')
def donesurvey():
    thetime = time.strftime("%H:%M")
    today = date.today()
    return render_template('pages/survey/done.html', thetime = thetime, today = today)

#----------------------------------------------------------------------------#
# Calendar
#----------------------------------------------------------------------------#

@app.route('/calendar')
@basic_auth.required
def calendar():
    thetime = time.strftime("%H:%M")
    today = date.today()
    return render_template('pages/calendar/calendar.html', thetime = thetime, today = today)

#----------------------------------------------------------------------------#
# Office Sign in / Out
#----------------------------------------------------------------------------#

@app.route('/qr/make', methods = ['GET', 'POST'])
@basic_auth.required
def qrmake():
    thetime = time.strftime("%H:%M")
    today = date.today()

    if request.method == 'POST':
        if request.form['type'] == "System":
            # Create a 125x125 QR code chart
            chart = QRChart(125, 125)
            # Add the text
            chart.add_data("http://107.21.186.10/qr/check/" + request.form['type'] + "/" + request.form['serial'])
            # chart.add_data(request.form['type'])

            # "Level H" error correction with a 0 pixel margin
            chart.set_ec('H', 0)
            # Download
            charturl = chart.get_url()
        else:
            # Create a 125x125 QR code chart
            chart = QRChart(125, 125)
            # Add the text
            chart.add_data("http://107.21.186.10/systemdetail.html?sys=" + request.form['serial'])
            # chart.add_data(request.form['type'])

            # "Level H" error correction with a 0 pixel margin
            chart.set_ec('H', 0)
            # Download
            charturl = chart.get_url()
        return render_template('pages/qr/view.html', thetime = thetime, today = today, charturl = charturl)

    return render_template('pages/qr/make.html', thetime = thetime, today = today)

@app.route('/qr/reports')
@basic_auth.required
def qrreports():
    thetime = time.strftime("%H:%M")
    today = date.today()

    return render_template('pages/qr/reports.html', thetime = thetime, today = today)


@app.route('/qr/check/<types>/<serial>', methods = ['GET', 'POST'])
@basic_auth.required
def officecheck(types, serial):
    thetime = time.strftime("%H:%M")
    today = date.today()

    if types == "MTGR":
        sys = Subsystem.query.filter_by(sub_type = "MTGR", serialsub = serial).first_or_404()
        return redirect('pages/systemdetail.html', sys = sys, thetime = thetime, today = today)
    elif types == "ROCU":
        sys = Subsystem.query.filter_by(sub_type = "ROCU", serialsub = serial).first_or_404()
        return redirect('pages/systemdetail.html', sys = sys, thetime = thetime, today = today)
    elif types == "Manipulator":
        sys = Subsystem.query.filter_by(sub_type = "Manipulator", serialsub = serial).first_or_404()
        return redirect('pages/systemdetail.html', sys = sys, thetime = thetime, today = today)
    elif types == "MPU":
        sys = Subsystem.query.filter_by(sub_type = "MPU", serialsub = serial).first_or_404()
        return redirect('pages/systemdetail.html', sys = sys, thetime = thetime, today = today)
    elif types == "System":
        return redirect('/systemdetail/' + serial)
    else: 
        pass
    # return render_template('pages/systemdetail.html', sys = sys, thetime = thetime, today = today)
    return render_template('pages/qr/check.html', thetime = thetime, today = today)


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