from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from flask import jsonify
from flask import send_file
import bcrypt
import os
import pyqrcode
from aadhaar import get_details, generate_unique_token, get_licence_detail
import pandas as pd
import random

app = Flask(__name__)
app.secret_key = "@13@6$$#ddfccv"

client = "mongodb+srv://project:hrithik1234@cluster0.yoorx.mongodb.net/?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
cluster = MongoClient(client)

dbPatient = cluster["Patient"]
patientdetail = dbPatient["PatientSignUp"]
patientmedicaldetail = dbPatient["patientmedicaldetail"]
patientreportdetail = dbPatient["patientreportdetail"]

dbDoctor = cluster["Doctor"]
doctordetail = dbDoctor["DoctorSignUp"]
doctoraddress = dbDoctor["doctoraddress"]
consentlist = dbDoctor["ConsentList"]

dbPharmacy = cluster["Pharmacy"]
pharmacydetail = dbPharmacy["PharmacySignUp"]
medicinedetail = dbPharmacy["MedicineDetail"]
orderedmedicinedetail = dbPharmacy["OrderedMedicine"]
billdetail=dbPharmacy["Bill"]

# Ending point for homepage
@app.route("/")
def homepage():
    return render_template("home.html")

# Doctor Section


# Ending point for doctor login
@app.route('/doctorsignin', methods=['GET', 'POST'])
def doctorsignin():
    if request.method == 'POST':
        aadhar = request.form['doctoraadhar']
        userLogin = doctordetail.find_one({'aadhar': aadhar})
        if userLogin:
            if bcrypt.hashpw(request.form['doctorpassword'].encode('utf-8'), userLogin['password']) == userLogin['password']:
                token=generate_unique_token()
                session['doctor'] = {
                    'aadhar': aadhar,
                    'var': 1
                }
                return redirect(url_for('twoFacAuthDoc', token=token))
        message = "Invalid Credentials"
        return render_template('login.html', message=message)
    return render_template("login.html")


# Ending point for doctor signup
# todo--> make a centralized db
@app.route('/doctorsignup', methods=['POST', 'GET'])
def doctorsignup():
    if request.method == 'POST':
        aadhar = request.form['doctoraadhar']
        email = request.form['doctoremail']
        councilnum = request.form['doctorcouncilnumber']
        data = get_details(aadhar)
        exist = doctordetail.find_one({'aadhar': aadhar})
        if data is not None and exist is None:
            hashpass = bcrypt.hashpw(
                request.form['doctorpassword'].encode('utf-8'), bcrypt.gensalt())
            session['doctor'] = {
                    'aadhar': aadhar,
                    'password': hashpass,
                    'email': email,
                    'councilnum': councilnum,
                    'name': data['name'],
                    'mobile': data['mobile'],
                    'var':0
                }
            token = generate_unique_token()
            return redirect(url_for('twoFacAuthDoc', token=token))
        message = "Invalid Details"
        return render_template("login.html", message=message)
    return render_template("login.html")

# 2 modals are there, make it one

@app.route('/twofacauthdoc/<string:token>', methods=['POST', 'GET'])
def twoFacAuthDoc(token):
    if 'doctor' in session:
        user_data = session.get('doctor')
        contains="No"
        if user_data:
            aadhar = user_data['aadhar']
            if user_data['var'] == 0:
                contains = "Yes"
                hashpass = user_data['password']
                email = user_data['email']
                councilnum = user_data['councilnum']
            data=get_details(aadhar)
            exist = doctordetail.find_one({'aadhar': aadhar})
            if request.method == 'POST':
                mobile_num = request.form.get('mob_number')
                session.pop('doctor')
                if "doctor" not in session:
                    mobile = data['mobile']
                    if mobile == mobile_num:
                        if exist is None:
                            doctordetail.insert_one({'name': data['name'], 'aadhar': data['aadhaar'], 'gender': data['gender'], 'DOB': data['dob'], 'age': data['age'],'address': data['address'], 'mobile': data['mobile'], 'councilnum' : councilnum,  'email': email, 'password': hashpass})
                            s = "http://34.31.27.140/emergencydashboard"
                            url = pyqrcode.create(s)
                            # path = "/var/www/html/RogItihaas/static/img/qrcode/" + aadhar + ".png"
                            path = "static/img/qrcode/"+aadhar+".png"
                            # path = "var/www/Rogitihaas/static/img/qrcode/"+aadhar+".png"
                            url.png(path, scale=6)
                        session['doctor'] = aadhar
                        return redirect(url_for('doctordashboard'))
                    else:
                        message = "Incorrect Mobile No. Try again"
                        return render_template('doctor/modal.html', message=message, name=data['name'], mobile=mobile, aadhar=aadhar,token=token)
                return redirect(url_for('doctordashboard'))
            if contains=="Yes":
                return render_template('doctor/modal.html', aadhar=aadhar, hashpass=hashpass, email=email, councilnum=councilnum, name=data['name'], mobile=data['mobile'],token=token)
    return render_template('doctor/modal.html', aadhar=aadhar, name=data['name'], mobile=data['mobile'],token=token)


@app.route('/doctordashboard', methods=['POST', 'GET'])
def doctordashboard():
    if 'doctor' in session:
        data = patientmedicaldetail.find({"draadhar": session["doctor"]})
        files = []
        for row in data:
            files.append({
                "name": row['name'],
                "aadhar": row['aadhar'],
                "todaydate": row["todaydate"],
                "_id": row['_id']
            })
        size = len(files)
        return render_template('doctor/dashboard.html', files=files, size=size)
    return render_template("login.html")
# Ending point for doctor signup

# End point for logging out
@app.route("/logout")
def customerLogout():
    if 'doctor' in session:
        patientdetail.update_one({'aadhar': session['doctor']}, {
                                "$set": {'verified': "No"}})
    session.clear()
    return redirect(url_for('homepage'))

# Patient-Doctor Section

# @app.route("/patdrhealthcard/<string:aadhar>", methods=['POST', 'GET'])
# def patdrhealthcard(aadhar):
#     if 'doctor' in session:
#         drexist = doctordetail.find_one({"aadhar": session['doctor']})
#         exist = patientdetail.find_one({'aadhar': aadhar})
#         return render_template("patient-doctor/healthcard.html", aadhar=aadhar, drname=drexist["name"], name=exist["name"])
#     return render_template("login.html")


# End point for grabbing patient
# details based on aadhar
@app.route("/doctorpatientdashboard", methods=['POST', 'GET'])
def doctorpatientdashboard():
    if 'doctor' in session:
        if request.method == 'POST':
            aadhar = request.form['aadhar']
            exist = patientdetail.find_one({'aadhar': aadhar})
            drexist = doctordetail.find_one({"aadhar": session['doctor']})

            if exist:
                return render_template("patient-doctor/dashboard.html", aadhar=aadhar, name=exist['name'], drname=drexist["name"], draadhar=session["doctor"],gender=exist['gender'],age=exist['age'],address=exist['address'],mobile=exist['mobile'])
        data = patientmedicaldetail.find({"draadhar": session['doctor']})
        files = []
        for row in data:
            files.append({
                "name": row['name'],
                "aadhar": row['aadhar'],
                "todaydate": row["todaydate"],
            })
        return render_template('doctor/dashboard.html', files=files, size=len(files))

    return render_template("login.html")

# End point for seeing medical p
@app.route('/viewprescription/<string:id>', methods=['POST', 'GET'])
def viewprescription(id):
    if 'doctor' in session:
        data1=patientmedicaldetail.find_one({'_id': ObjectId(id)})
        if data1 is not None:
            drexist=doctordetail.find_one({'aadhar':data1['draadhar']})
            files=[]
            medications = data1['medications']
            for medication in medications:
                medicine = medication.get('medicine')
                mg = medication.get('mg')
                dose = medication.get('dose')
                days = medication.get('days')
                food = medication.get('food')
                
                files.append({
                    'medicine': medicine,
                    'mg': mg,
                    'dose': dose,
                    'days': days,
                    'food': food
                })
            return render_template("patient-doctor/prescription_readonly.html", name=data1['name'], drname=data1["drname"], address=drexist["address"], phone=drexist["mobile"], medications=data1['medications'], age=data1['age'], weight=data1['weight'], disease=data1['disease'], gender=data1['gender'], files=files, aadhar=data1['aadhar'])
    return render_template("login.html")


# Open write prescription page from doctors side
@app.route('/writeprescription/<string:name>/<string:aadhar>')
def writeprescription(name, aadhar):
    if 'doctor' in session:
        exist = doctordetail.find_one({"aadhar": session["doctor"]})
        addr = exist["address"].split(",")
        addl = addr[2]
        addlen = len(addl)
        city = addl[1:addlen]
        medicines = medicinedetail.find()
        files = []
        for data in medicines:
            add = data["City"]
            addlenn = len(add)
            medcity = add[0:addlenn-1]

            if city == medcity:
                files.append({
                    "medicinename": data["Medicinename"],
                })
        print(len(files))
        return render_template("patient-doctor/prescription.html", files=files, name=name, drname=exist["name"], address=exist["address"], phone=exist["mobile"], aadhar=aadhar)
    return render_template("login.html")

@app.route("/documents/<string:name>/<string:aadhar>")
def documents(aadhar,name):
    if 'doctor' in session:
        files = []
        data = patientmedicaldetail.find({"aadhar": aadhar})
        if data is not None:
            for row in data:
                if row["presname"] == "Prescription":
                    files.append({
                        "name": row["name"],
                        "doctor": row['drname'],
                        "todaydate": row['todaydate'],
                        "presname": row["presname"],
                        "_id" :row['_id'],
                        'uploadedBydr':row['uploadedBydr']
                    })

        datapatientreport = patientreportdetail.find({"aadhar": aadhar})
        if datapatientreport is not None:
            for row in datapatientreport:
                if row["presname"] == "Prescription":
                    files.append({
                        "name": row["name"],
                        "doctor": row['drname'],
                        "todaydate": row['todaydate'],
                        "presname": row["presname"],
                        "_id" :row['_id'],
                        "url": row["url"],
                        'uploadedBydr':row['uploadedBydr']
                    })
        contain = "Yes"
        if len(files) == 0:
            contain = "No"
            files.append({
                "doctor": "No record found",
            })
        drexist = doctordetail.find_one({"aadhar": session['doctor']})
        data = patientdetail.find_one({"aadhar": aadhar})
        return render_template("patient-doctor/documents.html", files=files, aadhar=aadhar, name=data["name"], drname=drexist["name"], contain=contain)
    return render_template("login.html")


@app.route('/document-delete/<string:id>', methods=['GET','POST'])
def documentDelete(id):
    if 'doctor' in session:
        data2=patientmedicaldetail.find_one({'_id': ObjectId(id)})
        data3=patientreportdetail.find_one({'_id': ObjectId(id)})
        if data2 is not None:
            patientmedicaldetail.delete_one({'_id': ObjectId(id)})
            return redirect(url_for('documents', name=data2['name'], aadhar=data2['aadhar']))
        elif data3 is not None:
            i = str(data3['url'])
            s = (i.split('/')[3]).split('.')[0]
            file_to_delete = s+".pdf"

            # report_file_dir = "/var/www/html/RogItihaas/static/prescription/"+data3['aadhar']+"/"
            report_file_dir = "static/prescription/" + data3['aadhar'] + "/"

            file_path = os.path.join(report_file_dir, file_to_delete)
            
            if os.path.exists(file_path):
                os.remove(file_path)
            patientreportdetail.delete_one({'_id': ObjectId(id)})
            return redirect(url_for('documents',name=data3['name'], aadhar=data3['aadhar']))
    else:
        return redirect(url_for('doctorsignin'))

@app.route('/patient-document-delete/<string:id>',methods=['GET','POST'])
def patientdocumentDelete(id):
    if 'patient' in session:
        data2=patientmedicaldetail.find_one({'_id': ObjectId(id)})
        data3=patientreportdetail.find_one({'_id': ObjectId(id)})
        if data2 is not None:
            patientmedicaldetail.delete_one({'_id': ObjectId(id)})
            return redirect(url_for('patientdocuments'))
        elif data3 is not None:
            i=str(data3['url'])
            s=(i.split('/')[3]).split('.')[0]
            file_to_delete = s+".pdf"

            # report_file_dir = "/var/www/html/RogItihaas/static/prescription/"+data3['aadhar']+"/"
            report_file_dir = "static/prescription/" + data3['aadhar'] + "/"

            file_path = os.path.join(report_file_dir, file_to_delete)
            
            if os.path.exists(file_path):
                os.remove(file_path)
            patientreportdetail.delete_one({'_id': ObjectId(id)})
            return redirect(url_for('patientdocuments'))
    else:
        return redirect(url_for('patientsignin'))

@app.route("/uploadnewprescription/<string:name>/<string:aadhar>", methods=["POST", "GET"])
def uploadnewprescription(name, aadhar):
    if "doctor" in session:
        if request.method == "POST":
            file = request.files['file']

            path = "static/prescription/"
            # path = "/var/www/html/RogItihaas/static/prescription/"

            parent = str(aadhar)
            final_path = os.path.join(path, parent)
            if os.path.isdir(final_path) == False:
                os.mkdir(final_path)

            path = os.path.join(final_path, file.filename)
            file.save(path)

            now = datetime.now()  # current date and time

            year = now.strftime("%Y")
            month = now.strftime("%m")
            day = now.strftime("%d")

            todaydate = day + "/" + month + "/" + year

            drexist = doctordetail.find_one({"aadhar": session["doctor"]})
            checkIfavailable=patientreportdetail.find_one({'name': name, "aadhar": aadhar, 'drname': "Dr. " + drexist["name"],
                 "todaydate": todaydate, "draadhar": session["doctor"], "presname": "Prescription", "url": path, 'uploadedBydr': "Yes"})
            if checkIfavailable is None:
                patientreportdetail.insert_one({'name': name, "aadhar": aadhar, 'drname': "Dr. " + drexist["name"],
                 "todaydate": todaydate, "draadhar": session["doctor"], "presname": "Prescription", "url": path, 'uploadedBydr': "Yes"})
        files = []

        data = patientreportdetail.find({"aadhar": aadhar})
        if data is not None:
            for row in data:
                name: row["name"]
                if row["presname"] == "Prescription":
                    newpath = ""
                    for i in row["url"]:
                        if i == "\\":
                            newpath = newpath + "/"
                        else:
                            newpath = newpath + i
                    files.append({
                        "name": row["name"],
                        "doctor": row['drname'],
                        "todaydate": row['todaydate'],
                        "presname": row["presname"],
                        "url": newpath,
                        "_id": row['_id'],
                        'uploadedBydr': row['uploadedBydr']
                    })
        data2 = patientmedicaldetail.find({"aadhar": aadhar})
        if data2 is not None:
            for row in data2:
                    files.append({
                        "name": row["name"],
                        "doctor": row['drname'],
                        "todaydate": row['todaydate'],
                        "presname": row["presname"],
                        "_id": row['_id'],
                        'uploadedBydr': row['uploadedBydr']
                    })
        contain = "Yes"
        if len(files) == 0:
            contain = "No"
            files.append({
                "todaydate": "No record found",
            })
        drexist = doctordetail.find_one({"aadhar": session['doctor']})
        data = patientdetail.find_one({"aadhar": aadhar})
        return render_template("patient-doctor/documents.html", files=files, aadhar=aadhar, name=data["name"],
                               drname=drexist["name"], contain=contain)
    return render_template("login.html")

@app.route('/uploadpresciption/<string:aadhar>/<string:drname>',  methods=['POST', 'GET'])
def uploadpresciption(aadhar, drname):
    if 'doctor' in session:
        if request.method == 'POST':
            now = datetime.now()  # current date and time

            year = now.strftime("%Y")
            month = now.strftime("%m")
            day = now.strftime("%d")

            todaydate = day+"/"+month+"/"+year

            count=request.form['count']
            name = request.form['name']
            age = request.form['age']
            gender = request.form['gender']
            weight = request.form['weight']
            disease = request.form['disease']
            medications=[]

            for i in range(1, int(count)+1):
                medicine = request.form.get(f'medicine{i}')
                mg = request.form.get(f'mg{i}')
                dose = request.form.get(f'dose{i}')
                days = request.form.get(f'days{i}')
                food = request.form.get(f'food{i}')
                
                medication = {
                    'medicine': medicine,
                    'mg': mg,
                    'dose': dose,
                    'days': days,
                    'food': food
                }
                medications.append(medication)

            prescription = {
                'aadhar': aadhar,
                'drname': "Dr. " +drname,
                "draadhar": session["doctor"],
                "todaydate": todaydate,
                'name': name,
                'age': age,
                'gender': gender,
                'weight': weight,
                'disease': disease,
                'medications': medications,
                "presname": "Prescription",
                "uploadedBydr": "No"
            }
            if patientmedicaldetail.find_one(prescription) is None:
                patientmedicaldetail.insert_one(prescription)
            

            files = []

            data = patientmedicaldetail.find({"aadhar": aadhar})
            for row in data:
                files.append({
                    "name": row["name"],
                    "doctor": row['drname'],
                    "todaydate": row['todaydate'],
                    "presname": row["presname"],
                    "_id" :row['_id'],
                    'uploadedBydr':row['uploadedBydr']
                })
            data2 = patientreportdetail.find({"aadhar": aadhar})
            for row in data:
                if row["presname"] == "Prescription":
                    files.append({
                        "name": row["name"],
                        "doctor": row['drname'],
                        "todaydate": row['todaydate'],
                        "presname": row["presname"],
                        "url": row["url"],
                        "_id" :row['_id'],
                        'uploadedBydr':row['uploadedBydr']
                    })

            data2 = doctordetail.find_one({'aadhar': session['doctor']})
            return render_template("patient-doctor/documents.html", files=files, aadhar=aadhar, name=data2["name"], drname=data2["name"],contain="Yes")
    return render_template("login.html")


@app.route("/documents")
def drdocuments():
    if 'doctor' in session:
        data = patientmedicaldetail.find({"draadhar": session['doctor']})
        files = []
        found = "Yes"

        if data is not None:
            for row in data:
                files.append({
                    "name": row["name"],
                    "aadhar": row["aadhar"],
                    "drname": row["drname"],
                    "todaydate": row["todaydate"],
                    "presname": row["presname"],
                    "_id" :row['_id'],
                    'uploadedBydr':row['uploadedBydr']
                })

        data = patientreportdetail.find({"draadhar": session['doctor']})

        if data is not None:
            for row in data:
                if row["presname"] == "Prescription":
                    files.append({
                        "name": row["name"],
                        "aadhar": row["aadhar"],
                        "drname": row["drname"],
                        "todaydate": row["todaydate"],
                        "presname": row["presname"],
                        "url": row["url"],
                        "_id" :row['_id'],
                        'uploadedBydr':row['uploadedBydr']
                    })
        if len(files) == 0:
            found = "No"
            files.append({
                "name": "No records found",
            })
        return render_template("doctor/documents.html", files=files, found = found)
    return render_template("login.html")


@app.route('/consentview/<string:aadhar>/<string:econtact>')
def consentview(aadhar, econtact):
    if "doctor" in session:
        data1 = patientdetail.find_one({"mobile": econtact})
        data = consentlist.find_one({"aadhar": aadhar, "econtact": econtact})
        return render_template("patient-doctor/consentview.html", name=data["name"], drname=data["drname"], draadhar=data["draadhar"], relname=data1["name"],
                           econtact=econtact, status=data["status"], cost=data["cost"], severity=data["severity"], date=data["date"], aadhar=aadhar)
    return render_template("login.html")


@app.route("/consent1/<string:draadhar>/<string:econtact>", methods=["POST", "GET"])
def consent1(draadhar, econtact):
    if 'doctor' in session:
        data = consentlist.find_one({"draadhar": draadhar, "econtact": econtact})
        data1 = patientdetail.find_one({"mobile": econtact})
        return render_template("doctor/consent.html", name=data["name"], drname=data["drname"], draadhar=draadhar, relname=data1["name"],
                           econtact=econtact, status=data["status"], cost=data["cost"], severity=data["severity"], date=data["date"])
    return render_template("login.html")

@app.route('/consentlist1',  methods=['POST', 'GET'])
def consentList1():
    if 'doctor' in session:
        data = consentlist.find({"draadhar": session["doctor"]})
        files = []
        if data is not None:
            for row in data:
                files.append({
                    "name": row["name"],
                    "aadhar": row["aadhar"],
                    "drname": row["drname"],
                    "status": row["status"],
                    "draadhar": session["doctor"],
                    "severity": row["severity"],
                    "cost": row["cost"],
                    "date": row["date"],
                    "signature": row["signature"],
                    "econtact": row["econtact"],
                })
        contain = "Yes"
        if len(files) == 0:
            contain = "No"
            files.append({
                "name": "No Record Found",
            })

        return render_template("doctor/consentlist.html", contain=contain, files=files)
    return render_template("login.html")


@app.route('/consentlist/<string:drname>/<string:aadhar>',  methods=['POST', 'GET'])
def consentList(aadhar,drname):
    if 'doctor' in session:
        data = consentlist.find({"aadhar": aadhar})
        files = []
        if data is not None:
            for row in data:
                files.append({
                    "name": row["name"],
                    "aadhar": row["aadhar"],
                    "drname": row["drname"],
                    "status": row["status"],
                    "draadhar": session["doctor"],
                    "severity": row["severity"],
                    "cost": row["cost"],
                    "date": row["date"],
                    "signature": row["signature"],
                    "econtact": row["econtact"],
                })
        contain = "Yes"
        if len(files) == 0:
            contain = "No"
            files.append({
                "name": "No Record Found",
            })

        data = patientdetail.find_one({"aadhar": aadhar})

        return render_template("patient-doctor/consentlist.html", contain=contain, files=files, aadhar=aadhar, name=data["name"], drname=drname)
    return render_template("login.html")

@app.route('/consent/<string:drname>/<string:aadhar>',  methods=['POST', 'GET'])
def consent(drname,aadhar):
    if 'doctor' in session:
        data = patientdetail.find_one({"aadhar": aadhar})
        if request.method == "POST":
            severity = request.form['severity']
            cost = request.form["cost"]
            signature = request.form["signature"]

            now = datetime.now()  # current date and time

            year = now.strftime("%Y")
            month = now.strftime("%m")
            day = now.strftime("%d")

            todaydate = day + "/" + month + "/" + year

            consentlist.insert_one({
                "name": data["name"],
                "aadhar": aadhar,
                "drname": drname,
                "status": "Waiting for approval",
                "draadhar": session["doctor"],
                "severity": severity,
                "cost": cost,
                "date": todaydate,
                "signature": signature,
                "econtact": data["econtact"],
            })

        drexist = doctordetail.find_one({"aadhar": session['doctor']})
        return render_template("patient-doctor/consent.html", aadhar=aadhar, name=data["name"], drname=drexist["name"])
    return render_template("login.html")

@app.route("/prescriptiondecision")
def prescriptiondecision():
    if 'doctor' in session:
        return render_template("doctor/prescriptiondecision.html")
    return render_template("login.html")


@app.route("/prescription_repository",methods=["GET","POST"])
def prescription_repository():
    if "patient" in session:
        return render_template("patient/prescription_repository.html")
    return render_template("login.html")

@app.route("/drsettings", methods=["POST", "GET"])
def drsettings():
    if "doctor" in session:
        exist=doctordetail.find_one({'aadhar':session['doctor']})
        if request.method == "POST":
            old_pass=request.form['old_pass']
            new_pass=request.form['new_pass']
            if bcrypt.hashpw(old_pass.encode('utf-8'), exist['password']) == exist['password']:
                password = bcrypt.hashpw(
                            new_pass.encode('utf-8'), bcrypt.gensalt())
                doctordetail.update_one({'aadhar':session['doctor']},{"$set":{'password':password}})
                message="Updation successfull"
                return render_template("doctor/settings.html",message=message)
            else:
                message="Wrong Password! Please try again"
                return render_template("doctor/settings.html",message=message)
        return render_template("doctor/settings.html")
    return render_template("login.html")

@app.route("/drviewprescription/<string:id>", methods=["POST", "GET"])
def drviewprescription(id):
    if "doctor" in session:
            data1=patientmedicaldetail.find_one({'_id': ObjectId(id)})
            if data1 is not None:
                drexist=doctordetail.find_one({'aadhar':data1['draadhar']})
                files=[]
                medications = data1['medications']
                for medication in medications:
                    medicine = medication.get('medicine')
                    mg = medication.get('mg')
                    dose = medication.get('dose')
                    days = medication.get('days')
                    food = medication.get('food')
                    
                    files.append({
                        'medicine': medicine,
                        'mg': mg,
                        'dose': dose,
                        'days': days,
                        'food': food
                    })
                return render_template("doctor/prescription_readonly.html", name=data1['name'], drname=data1["drname"], address=drexist["address"], phone=drexist["mobile"], medications=data1['medications'], age=data1['age'], weight=data1['weight'], disease=data1['disease'], gender=data1['gender'], files=files, aadhar=data1['aadhar'])
    return render_template("login.html")


@app.route("/reports/<string:name>/<string:aadhar>", methods=["POST", "GET"])
def uploadreport(name, aadhar):
    if "doctor" in session:
        if request.method == "POST":
            now = datetime.now()  # current date and time
            year = now.strftime("%Y")
            month = now.strftime("%m")
            day = now.strftime("%d")

            docname = request.form["docname"]
            file = request.files['file']
            # path = "/var/www/html/RogItihaas/static/reports/"
            path = "static/reports/"
            # path = "var/www/Rogitihaas/static/reports/"
            parent = str(aadhar)

            final_path = os.path.join(path, parent)
            if os.path.isdir(final_path) == False:
                os.mkdir(final_path)
            # file.filename=str(aadhar)+str(day)+str(month)

            path = os.path.join(final_path, file.filename)
            file.save(path)



            todaydate = day + "/" + month + "/" + year
            newpath = ""
            for i in path:
                if i == "\\":
                    newpath = newpath + "/"
                else:
                    newpath = newpath + i
            drexist = doctordetail.find_one({"aadhar": session["doctor"]})
            if patientreportdetail.find_one({'name': name, "aadhar": aadhar, 'drname': "Dr. "+drexist["name"],
                 "todaydate": todaydate, "draadhar": session["doctor"], "presname": docname, "url": newpath, 'uploadedBydr': "Yes"}) is None:
                patientreportdetail.insert_one({'name': name, "aadhar": aadhar, 'drname': "Dr. "+drexist["name"],
                                                "todaydate": todaydate, "draadhar": session["doctor"], "presname": docname, "url": newpath, 'uploadedBydr':"Yes"})
        files = []

        data = patientreportdetail.find({"aadhar": aadhar})

        if data is not None:
            for row in data:
                name: row["name"]
                if row["presname"] != "Prescription":
                    files.append({
                        "name": row["name"],
                        "doctor": row['drname'],
                        "todaydate": row['todaydate'],
                        "presname": row["presname"],
                        "url": row["url"],
                        "_id" :row['_id']
                    })
        contain = "Yes"
        if len(files) == 0:
            contain = "No"
            files.append({
                "todaydate": "No record found",
            })
        drexist = doctordetail.find_one({"aadhar": session['doctor']})
        data = patientdetail.find_one({"aadhar": aadhar})
        return render_template("patient-doctor/reports.html", files=files, aadhar=aadhar, name=data["name"], drname=drexist["name"], contain=contain)
    return render_template("login.html")

@app.route('/report-delete/<string:id>',methods=['GET','POST'])
def reportDelete(id):
    if 'doctor' in session:
        data=patientreportdetail.find_one({'_id': ObjectId(id)})
        patientreportdetail.delete_one({'_id': ObjectId(id)})
        i=str(data['url'])
        s=(i.split('/')[3]).split('.')[0]
        file_to_delete = s+".pdf"

        # report_file_dir = "/var/www/html/RogItihaas/static/reports/"+data['aadhar']+"/"
        report_file_dir = "static/reports/" + data['aadhar'] + "/"

        file_path = os.path.join(report_file_dir, file_to_delete)
        
        if os.path.exists(file_path):
            os.remove(file_path)
        return redirect(url_for('uploadreport',name=data['drname'],aadhar=data['aadhar']))
    else:
        return redirect(url_for('doctorsignin'))
# Patient Section

# Ending point for patient signup
@app.route('/patientsignup', methods=['POST', 'GET'])
def patientsignup():
    if request.method == 'POST':
        radio = request.form['patienttype']
        aadhar = request.form['patientaadhar1']
        email = request.form['patientemail']
        econtact = request.form['emergency']
        hashpass=request.form['patientpassword']
        if radio == 'aadhaar_card':
            data = get_details(aadhar)
            exist = patientdetail.find_one({'aadhar': aadhar})
            if data is not None and exist is None:
                password = bcrypt.hashpw(
                            hashpass.encode('utf-8'), bcrypt.gensalt())
                session['patient'] = {
                    'aadhar': aadhar,
                    'password': password,
                    'email': email,
                    'econtact': econtact,
                    'name': data['name'],
                    'mobile': data['mobile'],
                    'var':0
                }
                token = generate_unique_token()
                return redirect(url_for('twoFacAuth', token=token))

            message = "Aadhar Record not found"
            return render_template("patientLogin.html", message=message)
        else:
            sliceaadhar = aadhar[0:12]
            data = get_details(sliceaadhar)
            exist = patientdetail.find_one({'aadhar': sliceaadhar})
            if data is not None and exist is None:
                password = bcrypt.hashpw(
                            hashpass.encode('utf-8'), bcrypt.gensalt())
                session['patient'] = {
                    'aadhar': aadhar,
                    'password': password,
                    'email': email,
                    'econtact': econtact,
                    'name': data['name'],
                    'mobile': data['mobile'],
                    'var': 0
                }
                token = generate_unique_token()
                return redirect(url_for('twoFacAuth', token=token))


            message = "Aadhar Record not found"
            return render_template("patientLogin.html", message=message)
    return render_template("patientLogin.html")


@app.route('/twofactorauth/<string:token>', methods=['POST', 'GET'])
def twoFacAuth(token):
    if 'patient' in session:
        user_data = session.get('patient')
        contains = "No"
        if user_data:
            aadhar = user_data['aadhar']
            if user_data['var'] == 0:
                contains = "Yes"
                hashpass = user_data['password']
                email = user_data['email']
                econtact = user_data['econtact']
            if len(aadhar) != 12:
                data = get_details(str(aadhar[0:12]))
            else:
                data = get_details(aadhar)
            exist = patientdetail.find_one({'aadhar': aadhar})
            if request.method == 'POST':
                mobile_num = request.form.get('mob_number')
                session.pop('patient')
                if "patient" not in session:
                    mobile = data['mobile']
                    if mobile == mobile_num:
                        if exist is None:
                            patientdetail.insert_one({'name': data['name'], 'aadhar': aadhar, 'gender': data['gender'], 'DOB': data['dob'], 'age': data['age'],'address': data['address'], 'mobile': data['mobile'], 'econtact' : econtact,  'email': email, 'password': hashpass})
                            s = "http://34.31.27.140/emergencydashboard/"+str(aadhar)
                            url = pyqrcode.create(s)
                            # path = "/var/www/html/RogItihaas/static/img/qrcode/"+aadhar+".png"
                            path = "static/img/qrcode/"+aadhar+".png"
                            # path = "var/www/Rogitihaas/static/img/qrcode/"+aadhar+".png"
                            url.png(path, scale=6)
                        session['patient'] = aadhar
                        return redirect(url_for('patientdashboard'))
                    else:
                        message = "Incorrect Mobile No. Try again"
                        return render_template('patient/modal.html', message=message, name=data['name'], mobile=mobile, aadhar=aadhar, token=token)
                return redirect(url_for('patientdashboard'))
            if contains == "Yes":
                return render_template('patient/modal.html', aadhar=aadhar, hashpass=hashpass, email=email, econtact=econtact, name=data['name'], mobile=data['mobile'],token=token)
    return render_template('patient/modal.html', aadhar=aadhar, name=data['name'], mobile=data['mobile'],token=token)



@app.route('/patientdashboard', methods=['POST', 'GET'])
def patientdashboard():
    if "patient" in session:
        files = []
        data = patientmedicaldetail.find({"aadhar": session["patient"]})
        for row in data:
            files.append({
                "name": row["name"],
                "doctor": row['drname'],
                "todaydate": row['todaydate'],
                "presname": row["presname"],
                "draadhar": row["draadhar"],
                "_id" :row['_id']
            })
    
        contain = "True"
        if len(files)==0:
            contain = "False"
            files.append({
                "name": "No Medical History",
                "doctor": "No Medical History",
                "todaydate": "No Medical History",
                "presname": "No Medical History",
                "draadhar": "No Medical History",
            })
        data2 = patientdetail.find_one({"aadhar": session["patient"]})
        return render_template('patient/dashboard.html', files=files, aadhar=session['patient'],name=data2['name'], address=data2['address'], mobile=data2['mobile'], econtact=data2['econtact'], contain=contain)
    return render_template("patientLogin.html")

@app.route("/patientviewprescription/<string:id>", methods=["POST", "GET"])
def patientviewprescription(id):
    if "patient" in session:
        data1=patientmedicaldetail.find_one({'_id': ObjectId(id)})
        if data1 is not None:
            drexist = doctordetail.find_one({'aadhar': data1['draadhar']})
            files = []
            medications = data1['medications']
            for medication in medications:
                medicine = medication.get('medicine')
                mg = medication.get('mg')
                dose = medication.get('dose')
                days = medication.get('days')
                food = medication.get('food')
                
                files.append({
                    'medicine': medicine,
                    'mg': mg,
                    'dose': dose,
                    'days': days,
                    'food': food
                })
            return render_template("patient/prescription_readonly.html", name=data1['name'], drname=data1["drname"], address=drexist["address"], phone=drexist["mobile"], medications=data1['medications'], age=data1['age'], weight=data1['weight'], disease=data1['disease'], gender=data1['gender'], files=files, aadhar=data1['aadhar'])
    return render_template("patientLogin.html")

@app.route("/patientrequestmed", methods=["POST", "GET"])
def patientrequestmed():
    if "patient" in session:
        return render_template("patient/requestmed.html")
    return render_template("patientLogin.html")

@app.route('/patienthome/<string:aadhar>', methods=['POST', 'GET'])
def patienthome(aadhar):
    if "doctor" in session:
        exist = patientdetail.find_one({'aadhar': aadhar})
        drexist = doctordetail.find_one({"aadhar": session['doctor']})

        if exist:
            files = []
            data = patientmedicaldetail.find(
                {"draadhar": session['doctor']})
            for row in data:
                files.append({
                    "doctor": row['drname'],
                    "todaydate": row['todaydate'],
                })
            return render_template("patient-doctor/dashboard.html", aadhar=aadhar, name=exist['name'],
                                   drname=drexist["name"], draadhar=session["doctor"], address=exist["address"], gender=exist["gender"],
                                   age=exist["age"], mobile=exist["mobile"])
    return render_template("patientLogin.html")


@app.route('/patientdiagnosis', methods=['POST', 'GET'])
def patientdiagnosis():
    if "patient" in session:
        return render_template('patient/diagnosis.html')
    return render_template("patientLogin.html")

@app.route('/prescriptionstatus', methods=['POST', 'GET'])
def prescriptionstatus():
    if "patient" in session:
        return render_template('patient/prescriptiondecision.html')
    return render_template("patientLogin.html")


@app.route('/patientoredermed', methods=['POST', 'GET'])
def patientoredermed():
    global regnum
    if "patient" in session:
        data1 = patientdetail.find_one({"aadhar": session["patient"]})

        if request.method == "POST":
            file = request.files['file']
            multiselect = request.form.getlist('medicines')
            mediname=[]
            for row in multiselect:
                medname, regnum = row.split('_')
                mediname.append(medname)
            # path = "/var/www/html/RogItihaas/static/pharmacyprescription/"
            path = "static/pharmacyprescription/"
            # path = "var/www/Rogitihaas/static/pharmacyprescription/"
            parent = str(regnum)+str(random.randint(1, 9999999))
            final_path = os.path.join(path, parent)
            if os.path.isdir(final_path) == False:
                os.mkdir(final_path)

            path = os.path.join(final_path, file.filename)
            file.save(path)

            now = datetime.now()  # current date and time

            year = now.strftime("%Y")
            month = now.strftime("%m")
            day = now.strftime("%d")

            todaydate = day + "/" + month + "/" + year
            randomnum = str(random.randint(10000, 99999))

            orderedmedicinedetail.insert_one({"patientname": data1["name"], "uploadedby": "Self", "medicinename": mediname, "regnum": regnum, "patientaadhar": session["patient"], "url": path, "status": "Ordered", "todaydate": todaydate, "randomnum": randomnum})
            return redirect(url_for("patientdeliverytracking"))

        address = data1["address"]
        addresslist = address.split(" ")
        city = addresslist[2]
        clen = len(city)
        city = city[0:clen-1]
        print(city)

        data = medicinedetail.find()
        files = []
        if data is not None:
            for rec in data:
                if rec["City"] == city:
                    files.append({
                        "Regnumber": rec["Regnumber"],
                        "Medicinename": rec["Medicinename"],
                        "Companyname": rec["Companyname"],
                        "Expiry": rec["Expiry"],
                        "Quantity": int(rec["Quantity"]),
                    })

        return render_template('patient/oredermed.html', files=files)

    return render_template("patientLogin.html")


@app.route('/patientdeliverytracking', methods=['GET', 'POST'])
def patientdeliverytracking():
    if "patient" in session:
        data = orderedmedicinedetail.find({"patientaadhar": session["patient"]})
        files = []
        for row in data:
            files.append({
                "Medicinename": row["medicinename"],
                "Regnum": row["regnum"],
                "Patientaadhar": row["patientaadhar"],
                "Url": row["url"],
                "Status": row["status"],
                "Uploadedby": row["uploadedby"],
                "patientname": row["patientname"],
                "todaydate": row["todaydate"],
                "randomnum": row["randomnum"],
                "_id": row["_id"],
            })
        return render_template("patient/deliverytrack.html", files=files)
    return render_template('patientLogin.html')

@app.route('/patientconsent', methods=['GET', 'POST'])
def patientconsent():
    if "patient" in session:
        data = patientdetail.find_one({"aadhar": session["patient"]})
        mobile = data["mobile"]
        data = consentlist.find({"econtact": mobile})

        files = []
        for row in data:
            files.append({
                "name": row["name"],
                "econtact": row["econtact"],
                "status": row["status"],
                "draadhar": row["draadhar"],
            })
        return render_template("patient/consent.html", files=files)
    return render_template('patientLogin.html')


@app.route('/patientconsentletter/<string:econtact>/<string:draadhar>', methods=['GET', 'POST'])
def patientconsentletter(econtact, draadhar):
    if "patient" in session:
        if request.method == "POST":
            accept = request.form.get("accept")
            if accept == "accept":
                consentlist.update_one({'econtact': econtact, 'draadhar': draadhar}, {
                                        "$set": {'status': "Approved"}})
            else:
                consentlist.update_one({'econtact': econtact, 'draadhar': draadhar}, {
                    "$set": {'status': "Rejected"}})
            data = patientdetail.find_one({"aadhar": session["patient"]})
            mobile = data["mobile"]
            data = consentlist.find({"econtact": mobile})

            files = []
            for row in data:
                files.append({
                    "name": row["name"],
                    "econtact": row["econtact"],
                    "status": row["status"],
                    "draadhar": row["draadhar"],
                })
            return render_template("patient/consent.html", files=files)
        data = consentlist.find_one({"econtact": econtact, "draadhar": draadhar})
        data1 = patientdetail.find_one({"aadhar": session["patient"]})
        return render_template("patient/accept_consent.html", name=data["name"], drname=data["drname"], draadhar=draadhar, econtact=econtact,
                               status=data["status"], cost=data["cost"], severity=data["severity"], date=data["date"],relname=data1["name"])
    return render_template('patientLogin.html')


@app.route('/acceptaction/<string:econtact>/<string:draadhar>', methods=['GET', 'POST'])
def acceptaction(econtact, draadhar):
    if "patient" in session:
        return render_template("patient/consent.html")
    return render_template('patientLogin.html')

# @app.route('/settings', methods=['POST', 'GET'])
# def settings(message):
#     if 'patient' in session:
#         exist=patientdetail.find_one({'aadhar':session['patient']})
#         return render_template('patient/settings.html', aadhar=exist['aadhar'])

@app.route('/patientsettings', methods=['POST', 'GET'])
def patientsettings():
    if "patient" in session:
        exist=patientdetail.find_one({'aadhar':session['patient']})
        if request.method == "POST":
            old_pass=request.form['old_pass']
            new_pass=request.form['new_pass']
            if bcrypt.hashpw(old_pass.encode('utf-8'), exist['password']) == exist['password']:
                password = bcrypt.hashpw(
                            new_pass.encode('utf-8'), bcrypt.gensalt())
                patientdetail.update_one({'aadhar':session['patient']},{"$set":{'password':password}})
                message="Updation successfull"
                return render_template("patient/settings.html",message=message, aadhar=session['patient'])
            else:
                message="Wrong Password! Please try again"
                return render_template("patient/settings.html",message=message, aadhar=session['patient'])
        return render_template("patient/settings.html", aadhar=session['patient'])
    return render_template("patientLogin.html")

@app.route('/aadharsettings', methods=['POST', 'GET'])
def aadharsettings():
    if "patient" in session:
        if request.method == "POST":
            old_aadhar=session['patient']
            econtact=request.form['econtact']
            email=request.form['email']
            new_aadhar=request.form['new_aadhar']
            password=request.form['password']
            exist=patientdetail.find_one({'aadhar':session['patient']})
            data=get_details(new_aadhar)
            prevExist = patientdetail.find_one({'aadhar':data['aadhaar']})
            if bcrypt.hashpw(password.encode('utf-8'), exist['password']) == exist['password'] and data is not None and prevExist is None:

                patientdetail.update_one({'aadhar': session['patient']}, {"$set": {'name': data['name'], 'aadhar': new_aadhar, 'gender': data['gender'], 'DOB': data['dob'], 'age': data['age'],'address': data['address'], 'mobile': data['mobile'], 'econtact' : econtact,  'email': email, 'password': exist['password']}})

                file_to_delete = old_aadhar+".png"
                # qr_code_dir = "/var/www/html/RogItihaas/static/img/qrcode/"
                qr_code_dir = "static/img/qrcode/"

                file_path = os.path.join(qr_code_dir, file_to_delete)

                if os.path.exists(file_path):
                    os.remove(file_path)

                s = "http://34.134.66.105/emergencydashboard"
                url = pyqrcode.create(s)

                # path = "/var/www/html/RogItihaas/static/img/qrcode/"+new_aadhar+".png"
                path = "static/img/qrcode/" + new_aadhar + ".png"

                url.png(path, scale=6)
                session['patient'] = new_aadhar
                message="Updation successfull"
                return render_template("patient/settings.html",message=message, aadhar=new_aadhar)
            else:
                message = "Wrong Credentials! Please try again"
                return render_template("patient/settings.html",message=message, aadhar=session['patient'])
        return render_template("patient/settings.html", aadhar=session['patient'])
    return render_template("patientLogin.html")

# Ending point for patient login
@app.route('/patientsignin', methods=['GET', 'POST'])
def patientsignin():
    if request.method == 'POST':
        aadhar = request.form['patientaadhar']
        userLogin = patientdetail.find_one({'aadhar': aadhar})
        if userLogin:
            if bcrypt.hashpw(request.form['patientpassword'].encode('utf-8'), userLogin['password']) == userLogin['password']:
                token = generate_unique_token()
                session['patient'] = {
                    'aadhar': aadhar,
                    'var': 1
                }
                return redirect(url_for('twoFacAuth', token=token))
        message = "Entered Invalid Credentials"
        return render_template('patientLogin.html', message=message)
    return render_template("patientLogin.html")


# End point for seeing medical records
@app.route("/patientdocuments")
def patientdocuments():
    if 'patient' in session:
        files = []
        data = patientmedicaldetail.find({"aadhar": session["patient"]})
        for row in data:
            files.append({
                "name": row["name"],
                "doctor": row['drname'],
                "todaydate": row['todaydate'],
                "presname": row["presname"],
                "draadhar": row["draadhar"],
                "aadhar": row["aadhar"],
                "_id": row['_id'],
                "uploadedBydr" : row['uploadedBydr']
            })

        data = patientreportdetail.find({"aadhar": session["patient"]})
        for row in data:
            if row['presname']=='Prescription':
                files.append({
                "name": row["name"],
                "doctor": row['drname'],
                "todaydate": row['todaydate'],
                "presname": row["presname"],
                "draadhar": row["draadhar"],
                "aadhar": row["aadhar"],
                "url": row["url"],
                "_id": row['_id'],
                 "uploadedBydr" : row['uploadedBydr']
            })

        contain = "Yes"
        if len(files) == 0:
            contain = "No"
            # name = row["name"]
            files.append({
                "name": "No Record Found",
                "doctor": "No Record Found",
                "todaydate": "No Record Found",
                "presname": "No Record Found",
                "draadhar": "No Record Found",
                "aadhar": "No Record Found",
                "type": "None",  # Add a new key-value pair for no record found
            })

            data = patientreportdetail.find({"aadhar": session["patient"]})
            for row in data:
                
                files.append({
                    "name": "No Record Found",
                    "doctor": "No Record Found",
                    "todaydate": "No Record Found",
                    "presname": "No Record Found",
                    "draadhar": "No Record Found",
                    "aadhar": "No Record Found",
                    "url": "No Record Found",
                    "type": "None",  # Add a new key-value pair for no record found
                })
    
        return render_template("patient/documents.html", files=files, contain=contain)
    return render_template("patientLogin.html")

# @app.route('/patientuploadprescription/<string:aadhar>/<string:drname>',  methods=['POST', 'GET'])
# def patientuploadpresciption(aadhar, drname):
#     if 'patient' in session:
#         if request.method == 'POST':
#             data = patientreportdetail.find({"aadhar": session["patient"]})
#             for row in data:
#                 prescription = {
#                 "name": row["name"],
#                     "doctor": row['drname'],
#                     "todaydate": row['todaydate'],
#                     "presname": row["presname"],
#                     "draadhar": row["draadhar"],
#                     "aadhar": row["aadhar"],
#                     "url": row["url"],
#                     "_id": row['_id'],
#                     "uploadedBydr" : row['uploadedBydr']
#                 }
#             if patientmedicaldetail.find_one(prescription) is None:
#                 patientmedicaldetail.insert_one(prescription)
            

#             files = []

#             data = patientmedicaldetail.find({"aadhar": aadhar})
#             for row in data:
#                 files.append({
#                     "name": row["name"],
#                     "doctor": row['drname'],
#                     "todaydate": row['todaydate'],
#                     "presname": row["presname"],
#                     "_id" :row['_id'],
#                     'uploadedBydr':row['uploadedBydr']
#                 })
#             data2 = patientreportdetail.find({"aadhar": aadhar})
#             for row in data:
#                 if row["presname"] == "Prescription":
#                     files.append({
#                         "name": row["name"],
#                         "doctor": row['drname'],
#                         "todaydate": row['todaydate'],
#                         "presname": row["presname"],
#                         "url": row["url"],
#                         "_id" :row['_id'],
#                         'uploadedBydr':row['uploadedBydr']
#                     })

#             data2 = doctordetail.find_one({'aadhar': session['doctor']})
#             return render_template("patient/documents.html", files=files, aadhar=aadhar, name=data2["name"], drname=data2["name"],contain="Yes")
#     return render_template("patientLogin.html")



@app.route("/patienthealthcard")
def patienthealthcard():
    if 'patient' in session:
        return render_template("patient/healthcard.html", aadhar=session["patient"])
    return render_template("patientLogin.html")

# Pharmacy Section

@app.route('/pharmacysignup', methods=['POST', 'GET'])
def pharmacysignup():
    licensenumber = request.form['licensenum']
    email = request.form['email']
    licensenumber=licensenumber.upper()
    if request.method == 'POST':
        exist = pharmacydetail.find_one({'licence': licensenumber})
        data = get_licence_detail(licensenumber)
        if data is not None and exist is None:
            hashpass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())
            session['pharmacy'] = {
                    'password': hashpass,
                    'email': email,
                    'licence' : data['licence'],
                    'var':0
                }
            token = generate_unique_token()
            return redirect(url_for('twoFacAuthPharmacy', token=token))

        message = "User Already Exist"
        return render_template("pharmacyLogin.html", message=message)
    return render_template("pharmacyLogin.html")



@app.route('/twofactorauthpharmacy/<string:token>', methods=['POST', 'GET'])
def twoFacAuthPharmacy(token):
    if 'pharmacy' in session:
        user_data = session.get('pharmacy')
        contains="No"
        if user_data:
            licence = user_data['licence']
            if user_data['var']==0:
                contains="Yes"
                hashpass = user_data['password']
                email = user_data['email']
            data=get_licence_detail(licence)
            exist = pharmacydetail.find_one({'licence': licence})
            if request.method == 'POST':
                mobile_num = request.form.get('mob_number')
                session.pop('pharmacy')
                if "pharmacy" not in session:
                    mobile = data['mobile']
                    if mobile == mobile_num:
                        if exist is None:
                            pharmacydetail.insert_one({'licence':data['licence'],'name': data['name'], 'gst':data['gst'], 'address': data['address'], 'mobile': data['mobile'], 'email': email, 'password': hashpass})
                        session['pharmacy'] = licence
                        return redirect(url_for('pharmacydashboard'))
                    else:
                        message = "Incorrect Mobile No. Try again"
                        return render_template('pharmacy/modal.html', message=message, name=data['name'], mobile=mobile,token=token)
                return redirect(url_for('pharmacydashboard'))
            if contains=="Yes":
                return render_template('pharmacy/modal.html', licence=licence, hashpass=hashpass, email=email, name=data['name'], mobile=data['mobile'],token=token)
    return render_template('pharmacy/modal.html', licence=licence, name=data['name'], mobile=data['mobile'],token=token)


@app.route('/pharmacysignin', methods=['GET', 'POST'])
def pharmacysignin():
    if request.method == 'POST':
        licensenumber = request.form['licensenumber']
        licensenumber = licensenumber.upper()
        userLogin = pharmacydetail.find_one({'licence': licensenumber})
        if userLogin:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), userLogin['password']) == userLogin['password']:
                token=generate_unique_token()
                session['pharmacy'] = {
                    'licence': licensenumber,
                    'var':1
                }
                return redirect(url_for('twoFacAuthPharmacy', token=token))

        message = "Invalid Credentials"
        return render_template('pharmacyLogin.html', message=message)
    return render_template('pharmacyLogin.html')

@app.route('/pharmacydashboard', methods=['POST', 'GET'])
def pharmacydashboard():
    if "pharmacy" in session:
        data = medicinedetail.find({"Regnumber": session["pharmacy"]})
        noofmedicine = len(list(data))
        return render_template('pharmacy/dashboard.html', noofmedicine=noofmedicine)
    return render_template("pharmacyLogin.html")

@app.route('/pharmacysettings', methods=['POST', 'GET'])
def pharmacysettings():
    if "pharmacy" in session:
        exist=pharmacydetail.find_one({'licence':session['pharmacy']})
        if request.method == "POST":
            old_pass=request.form['old_pass']
            new_pass=request.form['new_pass']
            if bcrypt.hashpw(old_pass.encode('utf-8'), exist['password']) == exist['password']:
                password = bcrypt.hashpw(
                            new_pass.encode('utf-8'), bcrypt.gensalt())
                pharmacydetail.update_one({'licence':session['pharmacy']},{"$set":{'password':password}})
                message="Updation successfull"
                return render_template("pharmacy/settings.html",message=message, licence=session['pharmacy'])
            else:
                message="Wrong Password! Please try again"
                return render_template("pharmacy/settings.html",message=message, licence=session['pharmacy'])
        return render_template("pharmacy/settings.html", licence=session['pharmacy'])
    return render_template("pharmacyLogin.html")

@app.route('/medicines', methods=['GET', 'POST'])
def medicines():
    if "pharmacy" in session:
        data = medicinedetail.find({"Regnumber": session["pharmacy"]})
        files = []
        if data is not None:
            for rec in data:
               files.append({
                    "Regnumber": rec["Regnumber"],
                    "Medicinename": rec["Medicinename"],
                    "Companyname": rec["Companyname"],
                    "Expiry": rec["Expiry"],
                    "Quantity": int(rec["Quantity"]),
                    "_id": rec["_id"],
                   })
        return render_template("pharmacy/medicines.html", regnumber=session["pharmacy"], files=files)
    return render_template('pharmacyLogin.html')

@app.route('/delete_medicine/<string:id>', methods=['GET', 'POST'])
def delete_medicine(id):
    if "pharmacy" in session:
        medicinedetail.delete_one({"_id":ObjectId(id)})
        return redirect(request.referrer or url_for("medicines", _external=True))
    return render_template('pharmacyLogin.html')


@app.route('/deliverytrack', methods=['GET', 'POST'])
def deliverytrack():
    if "pharmacy" in session:
        data = orderedmedicinedetail.find({"regnum": session["pharmacy"]})
        files = []
        if data is not None:
            for row in data:
                if row["status"] != "Ordered" and row["status"] != "Medicine Not Available":
                    files.append({
                        "Medicinename": row["medicinename"],
                        "Regnum": row["regnum"],
                        "Patientaadhar": row["patientaadhar"],
                        "Url": row["url"],
                        "Status": row["status"],
                        "Uploadedby": row["uploadedby"],
                        "patientname": row["patientname"],
                        "todaydate": row["todaydate"],
                        "randomnum": row["randomnum"],
                    })
        return render_template("pharmacy/deliverytrack.html", files=files)
    return render_template('pharmacyLogin.html')


@app.route('/pharmacydeliverytrack/<string:randomnum>/<string:patientaadhar>', methods=['GET', 'POST'])
def pharmacydeliverytrack(randomnum, patientaadhar):
    if "pharmacy" in session:
        if request.method == "POST":
            value = request.form.get("statusvalue")
            orderedmedicinedetail.update_one({'regnum': session['pharmacy'], 'randomnum': randomnum, 'patientaadhar': patientaadhar},
                                             {"$set": {'status': value}})
        data = orderedmedicinedetail.find({"regnum": session["pharmacy"]})
        files = []
        if data is not None:
            for row in data:
                if row["status"] != "Ordered":
                    files.append({
                        "Medicinename": row["medicinename"],
                        "Regnum": row["regnum"],
                        "Patientaadhar": row["patientaadhar"],
                        "Url": row["url"],
                        "Status": row["status"],
                        "Uploadedby": row["uploadedby"],
                        "patientname": row["patientname"],
                        "todaydate": row["todaydate"],
                        "randomnum": row["randomnum"],
                    })
        return render_template("pharmacy/deliverytrack.html", files=files)
    return render_template('pharmacyLogin.html')



@app.route('/onlineorderpatient/<string:patientname>/<string:randomnum>', methods=['GET', 'POST'])
def onlineorderpatient(patientname, randomnum):
    if "pharmacy" in session:
        if request.method == "POST":
            accept = request.form.get("accept")
            if accept == "accept":
                exist = pharmacydetail.find_one({"licence": session["pharmacy"]})
                orderedmedicinedetail.update_one({'regnum': session['pharmacy'], 'patientname': patientname, 'randomnum': randomnum}, {"$set": {'status': "Accepted"}})
                return render_template("pharmacy/onlinebill.html", name=exist['name'], address=exist['address'], mobile=exist['mobile'], email=exist['email'], gst=exist['gst'], randomnum=randomnum)
            else:
                orderedmedicinedetail.update_one({'regnum': session['pharmacy'], 'patientname': patientname, 'randomnum': randomnum}, {"$set": {'status': "Medicine Not Available"}})
            data = orderedmedicinedetail.find({"regnum": session["pharmacy"]})
            files = []
            if data is not None:
                for row in data:
                    if row["status"] == "Accepted":
                        files.append({
                            "Medicinename": row["medicinename"],
                            "Regnum": row["regnum"],
                            "Patientaadhar": row["patientaadhar"],
                            "Url": row["url"],
                            "Status": row["status"],
                            "Uploadedby": row["uploadedby"],
                            "patientname": row["patientname"],
                            "todaydate": row["todaydate"],
                            "randomnum": row["randomnum"],
                        })
            return render_template("pharmacy/deliverytrack.html", files=files)
    return render_template('pharmacyLogin.html')


@app.route('/onlineorder', methods=['GET', 'POST'])
def onlineorder():
    if "pharmacy" in session:
        data = orderedmedicinedetail.find({"status": "Ordered", "regnum": session["pharmacy"]})
        files = []
        if data is not None:
            for row in data:
                files.append({
                    "Medicinename": row["medicinename"],
                    "Regnum": row["regnum"],
                    "Patientaadhar": row["patientaadhar"],
                    "Url": row["url"],
                    "Status": row["status"],
                    "Uploadedby": row["uploadedby"],
                    "patientname": row["patientname"],
                    "todaydate": row["todaydate"],
                    "randomnum": row["randomnum"],
                })
            contain = "Yes"
            if len(files) == 0:
                contain = "No"
                files.append({
                    "patientname": "No record found",
                })
        return render_template("pharmacy/onlineorder.html", files=files, contain=contain)
    return render_template('pharmacyLogin.html')


@app.route('/offlineBilling', methods=['GET', 'POST'])
def offlineBilling():
    if "pharmacy" in session:
        exist = pharmacydetail.find_one({"licence": session["pharmacy"]})
        return render_template("pharmacy/offlineBilling.html",name=exist['name'],address=exist['address'],mobile=exist['mobile'],email=exist['email'],gst=exist['gst'])
    return render_template('pharmacyLogin.html')

@app.route('/generate_pdf/<string:invoice_number>', methods=['POST'])
def generate_pdf(invoice_number):
    pdf_data = request.get_data()

    # directory = '/var/www/html/RogItihaas/static/bills'

    directory = 'static/bills'
    os.makedirs(directory, exist_ok=True)
    file_name = f'bills_{invoice_number}.pdf'
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'wb') as file:
        file.write(pdf_data)
    return send_file(file_path, as_attachment=True)


@app.route('/uploadmedicine/<string:regnumber>', methods=['GET', 'POST'])
def uploadmedicine(regnumber):
    if "pharmacy" in session:
        if request.method == 'POST':
            f = request.files['file']
            print(f, " file")
            df = pd.read_csv(f)
            print("after df head")
            data = medicinedetail.find({"Regnumber": session["pharmacy"]})
            data1 = pharmacydetail.find_one({"licence": session["pharmacy"]})
            print(data1)
            address = data1["address"]
            print(address)
            citylist = address.split(" ")
            for ind in df.index:
                if medicinedetail.find_one({"Regnumber": regnumber, "Medicinename": df["Medicine Name"][ind], "Companyname": df["Company Name"][ind],
                                          "Expiry": df["Expiry Date"][ind], "Quantity": int(df["Quantity"][ind]), "City": citylist[1]}) is None:
                    medicinedetail.insert_one({"Regnumber": regnumber, "Medicinename": df["Medicine Name"][ind], "Companyname": df["Company Name"][ind],
                                          "Expiry": df["Expiry Date"][ind], "Quantity": int(df["Quantity"][ind]), "City": citylist[1]})

        files = []
        if data is not None:
            for rec in data:
                files.append({
                    "Medicinename": rec["Medicinename"],
                    "Companyname": rec["Companyname"],
                    "Expiry": rec["Expiry"],
                    "Quantity": int(rec["Quantity"]),
                })
        print(files)
        return render_template("pharmacy/medicines.html", regnumber=session["pharmacy"], files=files)
    return render_template('pharmacyLogin.html')

# Scan QR Section
@app.route('/emergencydashboard/<string:aadhar>', methods=['GET', 'POST'])
def emergencydashboard(aadhar):
    if "doctor" in session:
        exist = patientdetail.find_one({'aadhar': aadhar})
        drexist = doctordetail.find_one({"aadhar": session['doctor']})
        if exist:
            return render_template("patient-doctor/dashboard.html", aadhar=aadhar, name=exist['name'],
                                   drname=drexist["name"], draadhar=session["doctor"], gender=exist['gender'],
                                   age=exist['age'], address=exist['address'], mobile=exist['mobile'])
    data = patientdetail.find_one({"aadhar": aadhar})
    return render_template("scanqr/dashboard.html", name=data["name"], address=data["address"], mobile=data["econtact"], aadhar=data["aadhar"])


@app.route("/doctorpatientdashboardeme/<string:patientaadhar>", methods=['POST', 'GET'])
def doctorpatientdashboardeme(patientaadhar):
    if 'doctor' in session:
        exist = patientdetail.find_one({'aadhar': patientaadhar})
        drexist = doctordetail.find_one({"aadhar": session['doctor']})
        if exist:
            return render_template("patient-doctor/dashboard.html", aadhar=patientaadhar, name=exist['name'], drname=drexist["name"], draadhar=session["doctor"],gender=exist['gender'],age=exist['age'],address=exist['address'],mobile=exist['mobile'])
        data = patientmedicaldetail.find({"draadhar": session['doctor']})
        files = []
        for row in data:
            files.append({
                "name": row['name'],
                "aadhar": row['aadhar'],
                "todaydate": row["todaydate"],
            })
        return render_template('doctor/dashboard.html', files=files, size=len(files))

    return render_template("login.html")


@app.route('/twofacauthdocEme/<string:token>/<string:patientaadhar>', methods=['POST', 'GET'])
def twoFacAuthDocEme(token, patientaadhar):
    if 'doctor' in session:
        user_data = session.get('doctor')
        contains = "No"
        if user_data:
            aadhar = user_data['aadhar']
            if user_data['var'] == 0:
                contains = "Yes"
                hashpass = user_data['password']
                email = user_data['email']
                councilnum = user_data['councilnum']
            data = get_details(aadhar)
            exist = doctordetail.find_one({'aadhar': aadhar})
            if request.method == 'POST':
                mobile_num = request.form.get('mob_number')
                session.pop('doctor')
                if "doctor" not in session:
                    mobile = data['mobile']
                    if mobile == mobile_num:
                        if exist is None:
                            doctordetail.insert_one({'name': data['name'], 'aadhar': data['aadhaar'], 'gender': data['gender'], 'DOB': data['dob'], 'age': data['age'],'address': data['address'], 'mobile': data['mobile'], 'councilnum' : councilnum,  'email': email, 'password': hashpass})
                        session['doctor'] = aadhar
                        return redirect(url_for('doctorpatientdashboardeme', patientaadhar=patientaadhar))
                    else:
                        message = "Incorrect Mobile No. Try again"
                        return render_template('doctor/modal.html', message=message, name=data['name'], mobile=mobile, aadhar=aadhar,token=token)
                return redirect(url_for('doctorpatientdashboardeme', patientaadhar=patientaadhar))
            if contains == "Yes":
                return render_template('scanqr/modal.html', patientaadhar=patientaadhar, aadhar=aadhar, hashpass=hashpass, email=email, councilnum=councilnum, name=data['name'], mobile=data['mobile'],token=token)
    return render_template('scanqr/modal.html', patientaadhar=patientaadhar, aadhar=aadhar, name=data['name'], mobile=data['mobile'],token=token)


@app.route('/doctoremergencysignin/<string:patientaadhar>', methods=['GET', 'POST'])
def doctoremergencysignin(patientaadhar):
    if "doctor" in session:
        exist = patientdetail.find_one({'aadhar': patientaadhar})
        drexist = doctordetail.find_one({"aadhar": session['doctor']})
        if exist:
            return render_template("patient-doctor/dashboard.html", aadhar=patientaadhar, name=exist['name'],
                                   drname=drexist["name"], draadhar=session["doctor"], gender=exist['gender'],
                                   age=exist['age'], address=exist['address'], mobile=exist['mobile'])
    if request.method == 'POST':
        aadhar = request.form['doctoraadhar']
        userLogin = doctordetail.find_one({'aadhar': aadhar})
        if userLogin:
            if bcrypt.hashpw(request.form['doctorpassword'].encode('utf-8'), userLogin['password']) == userLogin['password']:
                token = generate_unique_token()
                session['doctor'] = {
                    'aadhar': aadhar,
                    'var': 1
                }
                return redirect(url_for('twoFacAuthDocEme', token=token, patientaadhar=patientaadhar))
        message = "Invalid Credentials"
        return render_template('login.html', message=message)
    return render_template("scanqr/doctorsignin.html", aadhar=patientaadhar)

if __name__ == '__main__':
    app.run(port=5000, debug=True)