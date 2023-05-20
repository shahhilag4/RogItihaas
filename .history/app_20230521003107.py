from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import bcrypt
import os
import pyqrcode
from aadhaar import get_details, generate_unique_token, get_licence_detail
import pandas as pd

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
                    'var':1
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

        message = "User Already Exist"
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
            if user_data['var']==0:
                contains="Yes"
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
                            s = "http://34.28.38.229/doctorsignup"
                            url = pyqrcode.create(s)
                            path = "static/img/qrcode/"+aadhar+".png"
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
                files = []
                data = patientmedicaldetail.find(
                    {"draadhar": session['doctor']})
                for row in data:
                    files.append({
                        "doctor": row['drname'],
                        "todaydate": row['todaydate'],
                    })
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

# End point for seeing medical records


@app.route("/documents/<string:name>/<string:aadhar>")
def documents(name, aadhar):
    if 'doctor' in session:
        files = []

        data = patientmedicaldetail.find({"aadhar": aadhar})
        if data is not None:
            for row in data:
                name: row["name"]
                if row["presname"] == "Prescription":
                    files.append({
                        "name": row["name"],
                        "doctor": row['drname'],
                        "todaydate": row['todaydate'],
                        "presname": row["presname"],
                    })
        data = patientreportdetail.find({"aadhar": aadhar})
        if data is not None:
            for row in data:
                name: row["name"]
                if row["presname"] == "Prescription":
                    files.append({
                        "name": row["name"],
                        "doctor": row['drname'],
                        "todaydate": row['todaydate'],
                        "presname": row["presname"],
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


@app.route('/consentview/<string:aadhar>/<string:econtact>')
def consentview(aadhar, econtact):
    if "doctor" in session:
        data1 = patientdetail.find_one({"mobile": econtact})
        data = consentlist.find_one({"aadhar": aadhar, "econtact": econtact})
        return render_template("patient-doctor/consentview.html", name=data["name"], drname=data["drname"], draadhar=data["draadhar"], relname=data1["name"],
                           econtact=econtact, status=data["status"], cost=data["cost"], severity=data["severity"], date=data["date"], aadhar=aadhar)
    return render_template("login.html")
# Open write prescription page from doctors side

@app.route('/writeprescription/<string:name>/<string:aadhar>')
def writeprescription(name, aadhar):
    if 'doctor' in session:
        exist = doctordetail.find_one({"aadhar": session["doctor"]})
        return render_template("patient-doctor/prescription.html", name=name, drname=exist["name"], address=exist["address"], phone=exist["mobile"], aadhar=aadhar)
    return render_template("login.html")

@app.route('/viewprescription/<string:name>/<string:aadhar>')
def viewprescription(name, aadhar):
    if 'doctor' in session:
        exist = doctordetail.find_one({"aadhar": session["doctor"]})
        return render_template("patient-doctor/prescription_readonly.html", name=name, drname=exist["name"], address=exist["address"], phone=exist["mobile"], aadhar=aadhar)
    return render_template("login.html")



@app.route('/uploadpresciption/<string:aadhar>/<string:drname>',  methods=['POST', 'GET'])
def uploadpresciption(aadhar, drname):
    if 'doctor' in session:
        if request.method == 'POST':

            a = 0
            b = 0
            c = 0

            now = datetime.now()  # current date and time

            year = now.strftime("%Y")
            month = now.strftime("%m")
            day = now.strftime("%d")

            todaydate = day+"/"+month+"/"+year

            name = request.form['name']
            age = request.form['age']
            gender = request.form['gender']
            disease = request.form['disease']

            medicine1 = request.form['medicine1']
            if len(medicine1) > 1:
                a = 1
                mg1 = request.form['mg1']
                dose1 = request.form['dose1']
                days1 = request.form['days1']
                food1 = request.form['food1']

            medicine2 = request.form['medicine2']
            if len(medicine2) > 1:
                b = 1
                mg2 = request.form['mg2']
                dose2 = request.form['dose2']
                days2 = request.form['days2']
                food2 = request.form['food2']

            medicine3 = request.form['medicine3']
            if len(medicine3) > 1:
                c = 1
                mg3 = request.form['mg3']
                dose3 = request.form['dose3']
                days3 = request.form['days3']
                food3 = request.form['food3']

            if a == 1 and b == 1 and c == 1:
                available = patientmedicaldetail.find_one({'name': name, "aadhar": aadhar, 'age': age, 'gender': gender, 'disease': disease, 'drname': drname, "todaydate": todaydate,
                                                           'medicine1': medicine1, "mg1": mg1, "dose1": dose1, "days1": days1, "food1": food1,
                                                           "medicine2": medicine2, "mg2": mg2, "dose2": dose2, "days2": days2, "food2": food2,
                                                           "medicine3": medicine3, "mg3": mg3, "dose3": dose3, "days3": days3, "food3": food3})

                if available == None:
                    patientmedicaldetail.insert_one({'name': name, "aadhar": aadhar, 'age': age, 'gender': gender, 'disease': disease, 'drname': drname, "todaydate": todaydate,
                                                     'medicine1': medicine1, "mg1": mg1, "dose1": dose1, "days1": days1, "food1": food1,
                                                     "medicine2": medicine2, "mg2": mg2, "dose2": dose2, "days2": days2, "food2": food2,
                                                     "medicine3": medicine3, "mg3": mg3, "dose3": dose3, "days3": days3, "food3": food3,
                                                     "draadhar": session["doctor"], "presname": "Prescription"})

            if a == 1 and b == 1 and c == 0:
                available = patientmedicaldetail.find_one({'name': name, "aadhar": aadhar, 'age': age, 'gender': gender, 'disease': disease, 'drname': drname, "todaydate": todaydate,
                                                           'medicine1': medicine1, "mg1": mg1, "dose1": dose1, "days1": days1, "food1": food1,
                                                           "medicine2": medicine2, "mg2": mg2, "dose2": dose2, "days2": days2, "food2": food2, "presname": "Prescription"})

                if available == None:
                    patientmedicaldetail.insert_one({'name': name, "aadhar": aadhar, 'age': age, 'gender': gender, 'disease': disease, 'drname': drname, "todaydate": todaydate,
                                                     'medicine1': medicine1, "mg1": mg1, "dose1": dose1, "days1": days1, "food1": food1,
                                                     "medicine2": medicine2, "mg2": mg2, "dose2": dose2, "days2": days2, "food2": food2,
                                                     "draadhar": session["doctor"], "presname": "Prescription"})

            if a == 1 and b == 0 and c == 0:
                available = patientmedicaldetail.find_one({'name': name, "aadhar": aadhar, 'age': age, 'gender': gender, 'disease': disease, 'drname': drname, "todaydate": todaydate,
                                                           'medicine1': medicine1, "mg1": mg1, "dose1": dose1, "days1": days1, "food1": food1})

                if available == None:
                    patientmedicaldetail.insert_one({'name': name, "aadhar": aadhar, 'age': age, 'gender': gender, 'disease': disease, 'drname': drname, "todaydate": todaydate,
                                                     'medicine1': medicine1, "mg1": mg1, "dose1": dose1, "days1": days1, "food1": food1,
                                                     "draadhar": session["doctor"], "presname": "Prescription"})

            files = []

            data = patientmedicaldetail.find({"aadhar": aadhar})
            for row in data:
                files.append({
                    "doctor": row['drname'],
                    "todaydate": row['todaydate'],
                    "presname": row["presname"],
                })

            return render_template("patient-doctor/documents.html", files=files)

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
                    "presname": row["presname"]
                })

        if len(files) == 0:
            found = "No"
            files.append({
                "name": "No records found",
            })
        return render_template("doctor/documents.html", files=files, found = found)
    return render_template("login.html")

@app.route("/consent1/<string:draadhar>/<string:econtact>", methods=["POST", "GET"])
def consent1(draadhar, econtact):
    if 'doctor' in session:
        data = consentlist.find_one({"draadhar": draadhar, "econtact": econtact})
        data1 = patientdetail.find_one({"mobile": econtact})
        return render_template("doctor/consent.html", name=data["name"], drname=data["drname"], draadhar=draadhar, relname=data1["name"],
                           econtact=econtact, status=data["status"], cost=data["cost"], severity=data["severity"], date=data["date"])
    return render_template("login.html")

@app.route("/prescriptiondecision")
def prescriptiondecision():
    if 'doctor' in session:
        return render_template("doctor/prescriptiondecision.html")
    return render_template("login.html")


@app.route("/prescription_repository")
def prescription_repository():
    if "patient" in session:
        print("Hello")
        return render_template("patient/prescription_repository.html")
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


@app.route("/drsettings", methods=["POST", "GET"])
def drsettings():
    if "doctor" in session:
        return render_template("doctor/settings.html")
    return render_template("login.html")

@app.route("/drviewprescription", methods=["POST", "GET"])
def drviewprescription():
    if "doctor" in session:
        return render_template("doctor/prescription_readonly.html")
    return render_template("login.html")

@app.route("/uploadprescription/<string:name>/<string:aadhar>", methods=["POST", "GET"])
def uploadprescription(name, aadhar):
    if "doctor" in session:
        if request.method == "POST":
            file = request.files['file']
            path = "static/prescription/"
            parent = str(aadhar)
            final_path = os.path.join(path, parent)
            if os.path.isdir(final_path) == "False":
                os.mkdir(final_path)

            path = os.path.join(final_path, file.filename)
            file.save(path)

            now = datetime.now()  # current date and time

            year = now.strftime("%Y")
            month = now.strftime("%m")
            day = now.strftime("%d")

            todaydate = day + "/" + month + "/" + year

            drexist = doctordetail.find_one({"aadhar": session["doctor"]})
            patientreportdetail.insert_one(
                {'name': name, "aadhar": aadhar, 'drname': "Dr. " + drexist["name"],
                 "todaydate": todaydate, "draadhar": session["doctor"], "presname": "Prescription", "url": path})
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


@app.route("/reports/<string:name>/<string:aadhar>", methods=["POST", "GET"])
def uploadreport(name, aadhar):
    if "doctor" in session:
        if request.method == "POST":
            docname = request.form["docname"]
            file = request.files['file']
            path = "static/reports/"
            parent = str(aadhar)
            final_path = os.path.join(path, parent)
            if os.path.isdir(final_path) == "False":
                os.mkdir(final_path)

            path = os.path.join(final_path, file.filename)
            file.save(path)

            now = datetime.now()  # current date and time

            year = now.strftime("%Y")
            month = now.strftime("%m")
            day = now.strftime("%d")

            todaydate = day + "/" + month + "/" + year

            drexist = doctordetail.find_one({"aadhar": session["doctor"]})
            patientreportdetail.insert_one(
                {'name': name, "aadhar": aadhar, 'drname': "Dr. "+drexist["name"],
                 "todaydate": todaydate, "draadhar": session["doctor"], "presname": docname, "url": path})
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
        contains="No"
        if user_data:
            aadhar = user_data['aadhar']
            if user_data['var']==0:
                contains="Yes"
                hashpass = user_data['password']
                email = user_data['email']
                econtact = user_data['econtact']
            if len(aadhar)!=12:
                data=get_details(str(aadhar[0:12]))
            else:
                data=get_details(aadhar)
            exist = patientdetail.find_one({'aadhar': aadhar})
            if request.method == 'POST':
                mobile_num = request.form.get('mob_number')
                session.pop('patient')
                if "patient" not in session:
                    mobile = data['mobile']
                    if mobile == mobile_num:
                        if exist is None:
                            patientdetail.insert_one({'name': data['name'], 'aadhar': data['aadhaar'], 'gender': data['gender'], 'DOB': data['dob'], 'age': data['age'],'address': data['address'], 'mobile': data['mobile'], 'econtact' : econtact,  'email': email, 'password': hashpass})
                            s = "http://34.28.38.229/patientsignup"
                            url = pyqrcode.create(s)
                            path = "static/img/qrcode/"+aadhar+".png"
                            url.png(path, scale=6)
                        session['patient'] = aadhar
                        return redirect(url_for('patientdashboard'))
                    else:
                        message = "Incorrect Mobile No. Try again"
                        return render_template('patient/modal.html', message=message, name=data['name'], mobile=mobile, aadhar=aadhar,token=token)
                return redirect(url_for('patientdashboard'))
            if contains=="Yes":
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
        return render_template('patient/dashboard.html', files=files, name=data2['name'], address=data2['address'], mobile=data2['mobile'], econtact=data2['econtact'], contain=contain)
    return render_template("patientLogin.html")

@app.route("/patientviewprescription", methods=["POST", "GET"])
def patientviewprescription():
    if "patient" in session:
        return render_template("patient/prescription_readonly.html")
    return render_template("patientLogin.html")
@app.route("/patientviewprescription", methods=["POST", "GET"])
def patientviewprescription():
    if "patient" in session:
        return render_template("patient/prescription_readonly.html")
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
    if "patient" in session:
        return render_template('patient/oredermed.html')
    return render_template("patientLogin.html")

@app.route('/patientdeliverytracking', methods=['GET', 'POST'])
def patientdeliverytracking():
    if "patient" in session:
        return render_template("patient/deliverytrack.html")
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


@app.route('/patientsettings', methods=['POST', 'GET'])
def patientsettings():
    if "patient" in session:
        return render_template('patient/settings.html')
    return render_template("patientLogin.html")


# Ending point for patient login
@app.route('/patientsignin', methods=['GET', 'POST'])
def patientsignin():
    if request.method == 'POST':
        aadhar = request.form['patientaadhar']
        userLogin = patientdetail.find_one({'aadhar': aadhar})
        if userLogin:
            if bcrypt.hashpw(request.form['patientpassword'].encode('utf-8'), userLogin['password']) == userLogin['password']:
                token=generate_unique_token()
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
            name = row["name"]
            files.append({
                "name": row["name"],
                "doctor": row['drname'],
                "todaydate": row['todaydate'],
                "presname": row["presname"],
                "draadhar": row["draadhar"],
                "aadhar": row["aadhar"],
                "type": "Prescription",  # Assign type as "Prescription" for documents in the "prescription" folder
            })

        data = patientreportdetail.find({"aadhar": session["patient"]})
        for row in data:
            name = row["name"]
            files.append({
                "name": row["name"],
                "doctor": row['drname'],
                "todaydate": row['todaydate'],
                "presname": row["presname"],
                "draadhar": row["draadhar"],
                "aadhar": row["aadhar"],
                "url": row["url"],
                "type": "Report",  # Assign type as "Report" for documents in the "reports/{{aadhar}}" folder
            })

        contain = "Yes"
        if len(files) == 0:
            contain = "No"
            name = row["name"]
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
                name = row["name"]
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
                return redirect(url_for('twoFacAuthPharmacy',token=token))

        message = "Invalid Credentials"
        return render_template('pharmacyLogin.html', message=message)
    return render_template('pharmacyLogin.html')

@app.route('/pharmacydashboard', methods=['POST', 'GET'])
def pharmacydashboard():
    if "pharmacy" in session:
        return render_template('pharmacy/dashboard.html')
    return render_template("pharmacyLogin.html")

@app.route('/medicines', methods=['GET', 'POST'])
def medicines():
    if "pharmacy" in session:
        data = medicinedetail.find({"Regnumber": session["pharmacy"]})
        files = []
        if data is not None:
            for rec in data:
               files.append({
                    "Medicinename": rec["Medicinename"],
                    "Companyname": rec["Companyname"],
                    "Expiry": rec["Expiry"],
                    "Quantity": int(rec["Quantity"]),
                   })
            return render_template("pharmacy/medicines.html", regnumber=session["pharmacy"], files=files)
    return render_template('pharmacyLogin.html')


@app.route('/deliverytrack', methods=['GET', 'POST'])
def deliverytrack():
    if "pharmacy" in session:
        return render_template("pharmacy/deliverytrack.html")
    return render_template('pharmacyLogin.html')


@app.route('/onlineorder', methods=['GET', 'POST'])
def onlineorder():
    if "pharmacy" in session:
        return render_template("pharmacy/onlineorder.html")
    return render_template('pharmacyLogin.html')


@app.route('/offlineBilling', methods=['GET', 'POST'])
def offlineBilling():
    if "pharmacy" in session:
        return render_template("pharmacy/offlineBilling.html")
    return render_template('pharmacyLogin.html')


@app.route('/onlinebill', methods=['GET', 'POST'])
def onlinebill():
    if "pharmacy" in session:
        return render_template("pharmacy/onlinebill.html")
    return render_template('pharmacyLogin.html')

@app.route('/pharmacyviewprescription', methods=['GET', 'POST'])
def pharmacyviewprescription():
    if "pharmacy" in session:
        return render_template("pharmacy/prescription_readonly.html")
    return render_template('pharmacyLogin.html')

@app.route('/pharmacyviewbill', methods=['GET', 'POST'])
def pharmacyviewbill():
    if "pharmacy" in session:
        return render_template("pharmacy/bill_readonly.html")
    return render_template('pharmacyLogin.html')

@app.route('/uploadmedicine/<string:regnumber>', methods=['GET', 'POST'])
def uploadmedicine(regnumber):
    if "pharmacy" in session:
        if request.method == 'POST':
            f = request.files['file']
            df = pd.read_csv(f)
            for ind in df.index:
                medicinedetail.insert_one({"Regnumber": regnumber, "Medicinename": df["Medicine Name"][ind], "Companyname": df["Company Name"][ind],
                                          "Expiry": df["Expiry Date"][ind], "Quantity": int(df["Quantity"][ind])})
        return render_template("pharmacy/medicines.html")
    return render_template('pharmacyLogin.html')

# Scan QR Section
@app.route('/emergencydashboard', methods=['GET', 'POST'])
def emergencydashboard():
    return render_template("scanqr/dashboard.html")

@app.route('/emergencydoctorsignin', methods=['GET', 'POST'])
def emergencydoctorsignin():
        return render_template("scanqrLogin.html")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
