from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import bcrypt
import os
import pyqrcode
import pandas as pd
from aadhaar import get_details

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
    elif request.method == 'POST':
        aadhar = request.form['doctoraadhar']
        userLogin = doctordetail.find_one({'aadhar': aadhar})
        if userLogin:
            if bcrypt.hashpw(request.form['doctorpassword'].encode('utf-8'), userLogin['password']) == userLogin['password']:
                session['doctor'] = aadhar
                data = patientmedicaldetail.find({"draadhar": aadhar})
                files = []
                for row in data:
                    files.append({
                        "name": row['name'],
                        "aadhar": row['aadhar'],
                        "todaydate": row["todaydate"],
                    })
                size = len(files)
                return render_template('doctor/dashboard.html', files=files, size=size)
        message = "Invalid Credentials"
        return render_template('login.html', message=message)
    return render_template("login.html")


# Ending point for doctor signup
@app.route('/doctorsignup', methods=['POST', 'GET'])
def doctorsignup():
    if request.method == 'POST':
        aadhar = request.form['doctoraadhar']
        email = request.form['doctoremail']
        name = request.form['doctorname']
        councilnum = request.form['doctorcouncilnumber']
        exist = doctordetail.find_one({'aadhar': aadhar})
        if exist is None:
            hashpass = bcrypt.hashpw(
                request.form['doctorpassword'].encode('utf-8'), bcrypt.gensalt())
            doctordetail.insert_one(
                {'name': name, 'aadhar': aadhar, 'email': email, 'councilnum': councilnum, 'password': hashpass})

            session['doctor'] = aadhar

            return render_template('doctor/dashboard.html')
        message = "User Already Exist"
        return render_template("login.html", message=message)
    return render_template("login.html")

# End point for logging out
@app.route("/logout")
def customerLogout():
    if 'patient' in session:
        patientdetail.update_one({'aadhar': session['patient']}, {
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
                return render_template("patient-doctor/dashboard.html", aadhar=aadhar, name=exist['name'], drname=drexist["name"], draadhar=session["doctor"])
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


# Open write prescription page from doctors side

@app.route('/writeprescription/<string:name>/<string:aadhar>')
def writeprescription(name, aadhar):
    if 'doctor' in session:
        exist = doctoraddress.find_one({"aadhar": session["doctor"]})
        return render_template("patient-doctor/prescription.html", name=name, drname=exist["name"], addlineone=exist["addlineone"],
                               statecountry=exist["statecountry"], phone=exist["phone"], aadhar=aadhar)
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
        for row in data:
            files.append({
                "name": row["name"],
                "aadhar": row["aadhar"],
                "drname": row["drname"],
                "todaydate": row["todaydate"],
                "presname": row["presname"]
            })
        return render_template("doctor/documents.html", files=files)
    return render_template("login.html")


@app.route("/prescription_repository")
def prescription_repository():
    if "patient" in session:
        return render_template("patient/prescription_repository.html")
    return render_template("login.html")


@app.route("/prescription_template", methods=["POST", "GET"])
def prescription_template():
    if "doctor" in session:
        if request.method == 'POST':
            drname = request.form["drname"]
            addlineone = request.form["addlineone"]
            statecountry = request.form["statecountry"]
            phone = request.form["phone"]
            exit = doctoraddress.find_one({"aadhar": session["doctor"]})
            if exit == None:
                doctoraddress.insert_one({"aadhar": session["doctor"], "name": drname, "addlineone": addlineone,
                                          "statecountry": statecountry, "phone": phone})
            else:
                doctoraddress.delete_one({"aadhar": session["doctor"]})
                doctoraddress.insert_one({"aadhar": session["doctor"], "name": drname, "addlineone": addlineone,
                                          "statecountry": statecountry, "phone": phone})
        exist = doctoraddress.find_one({"aadhar": session["doctor"]})
        return render_template("doctor/sample.html", name=exist["name"], addlineone=exist["addlineone"],
                               statecountry=exist["statecountry"], phone=exist["phone"])
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
            contain="No"
            files.append({
                "name": "No Record Found",
            })

        data = patientdetail.find_one({"aadhar": aadhar})

        return render_template("patient-doctor/consentlist.html", contain=contain, files=files, aadhar=aadhar, name=data["name"], drname=drname)
    return render_template("login.html")

@app.route('/consent/<string:drname>/<string:aadhar>',  methods=['POST', 'GET'])
def consent(aadhar,drname):
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
            datapatient = get_details(aadhar)

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
                "econtact": datapatient["mobile"],
            })

        drexist = doctordetail.find_one({"aadhar": session['doctor']})
        return render_template("patient-doctor/consent.html", aadhar=aadhar, name=data["name"], drname=drexist["name"])
    return render_template("login.html")


@app.route("/drsettings", methods=["POST", "GET"])
def drsettings():
    if "doctor" in session:
        return render_template("doctor/settings.html")
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
            print(path)
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
            print(path)
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
        if radio == 'aadhaar_card':
            data = get_details(aadhar)
            exist = patientdetail.find_one({'aadhar': aadhar})
            if data is not None and exist is None:
                hashpass = bcrypt.hashpw(
                    request.form['patientpassword'].encode('utf-8'), bcrypt.gensalt())
                patientdetail.insert_one({'name': data['name'], 'aadhar': data['aadhaar'], 'gender': data['gender'], 'DOB': data['dob'], 'age': data['age'],'address': data['address'], 'mobile': data['mobile'], 'econtact' : econtact,  'email': email, 'password': hashpass, 'infant': 0, 'verified': "No"})
                s = "http://34.28.38.229/patientsignup"
                url = pyqrcode.create(s)
                path = "static/img/qrcode/"+aadhar+".png"
                url.png(path, scale=6)
                return render_template('patient/modal.html', name=data['name'], mobile=data['mobile'], aadhar=aadhar)

            message = "Aadhar Record not found"
            return render_template("patientLogin.html", message=message)
        else:
            sliceaadhar = aadhar[0:12]
            data = get_details(sliceaadhar)
            exist = patientdetail.find_one({'aadhar': sliceaadhar})
            if data is not None and exist is None:
                hashpass = bcrypt.hashpw(
                    request.form['patientpassword'].encode('utf-8'), bcrypt.gensalt())
                patientdetail.insert_one({'name': data['name'], 'aadhar': aadhar, 'gender': data['gender'], 'DOB': data['dob'], 'age': data['age'],
                                         'address': data['address'], 'mobile': data['mobile'], 'econtact' : econtact, 'email': email, 'password': hashpass, 'infant': 1, 'verified': "No"})
                s = "http://34.28.38.229/patientsignup"
                url = pyqrcode.create(s)
                path = "static/img/qrcode/"+aadhar+".png"
                url.png(path, scale=6)

                return render_template('patient/modal.html', name=data['name'], mobile=data['mobile'], aadhar=sliceaadhar)

            message = "Aadhar Record not found"
            return render_template("patientLogin.html", message=message)
    return render_template("patientLogin.html")


@app.route('/twofactorauth/<string:aadhar>', methods=['Post', 'Get'])
def twoFacAuth(aadhar):
    mobile_num = request.form['mob_number']
    exist = patientdetail.find_one({'aadhar': aadhar})
    print(exist['verified'])
    if request.method == 'POST':
        if exist['verified'] == "No":
            mobile = exist['mobile']
            if mobile == mobile_num:
                patientdetail.update_one({'aadhar': aadhar}, {
                                         "$set": {'verified': "Yes"}})
                session['patient'] = aadhar
                files = []
                pData = patientmedicaldetail.find({"aadhar": aadhar})

                for row in pData:
                    files.append({
                        "name": row["name"],
                        "doctor": row['drname'],
                        "todaydate": row['todaydate'],
                        "presname": row["presname"],
                        "draadhar": row["draadhar"],
                    })
                return redirect(url_for('patientdashboard'))
            message = "Incorrect Mobile No. Try again"
            return render_template('patient/modal.html', message=message, name=exist['name'], mobile=exist['mobile'], aadhar=exist['aadhar'])
        messageVerify = "Already verified"
        return redirect(url_for('patientdashboard', message=messageVerify))
    return render_template('patientLogin.html')


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
        return render_template('patient/dashboard.html', files=files, name=data2['name'], address=data2['address'], mobile=data2['mobile'], infant=data2['infant'], econtact=data2['econtact'], contain=contain)
    return render_template("patientLogin.html")


@app.route('/patientdiagnosis', methods=['POST', 'GET'])
def patientdiagnosis():
    if "patient" in session:
        return render_template('patient/diagnosis.html')
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
        return render_template("patient/consent.html")
    return render_template('patientLogin.html')

@app.route('/patientconsentletter', methods=['GET', 'POST'])
def patientconsentletter():
    if "patient" in session:
        return render_template("patient/accept_consent.html")
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
                return render_template('patient/modal.html', name=userLogin['name'], mobile=userLogin['mobile'], aadhar=aadhar)

        message = "Invalid Credentials"
        return render_template('patientLogin.html', message=message)
    return render_template("patientLogin.html")


# End point for seeing medical records
@app.route("/patientdocuments")
def patientdocuments():
    if 'patient' in session:
        files = []

        data = patientmedicaldetail.find({"aadhar": session["patient"]})
        for row in data:
            name: row["name"]
            files.append({
                "name": row["name"],
                "doctor": row['drname'],
                "todaydate": row['todaydate'],
                "presname": row["presname"],
                "draadhar": row["draadhar"],
                "aadhar": row["aadhar"],
            })

            data = patientreportdetail.find({"aadhar": session["patient"]})
            for row in data:
                name: row["name"]
                files.append({
                    "name": row["name"],
                    "doctor": row['drname'],
                    "todaydate": row['todaydate'],
                    "presname": row["presname"],
                    "draadhar": row["draadhar"],
                    "aadhar": row["aadhar"],
                    "url": row["url"],
                })
        contain = "Yes"
        if len(files)==0:
            contain = "No"
            name: row["name"]
            files.append({
                "name": "No Record Found",
                "doctor": "No Record Found",
                "todaydate": "No Record Found",
                "presname": "No Record Found",
                "draadhar": "No Record Found",
                "aadhar": "No Record Found",
            })

            data = patientreportdetail.find({"aadhar": session["patient"]})
            for row in data:
                name: row["name"]
                files.append({
                    "name": "No Record Found",
                    "doctor": "No Record Found",
                    "todaydate": "No Record Found",
                    "presname": "No Record Found",
                    "draadhar": "No Record Found",
                    "aadhar": "No Record Found",
                    "url": "No Record Found",
                })
        return render_template("patient/documents.html", files=files, contain=contain)
    return render_template("patientLogin.html")


@app.route("/patienthealthcard")
def patienthealthcard():
    if 'patient' in session:
        # print(session["patient"])
        return render_template("patient/healthcard.html", aadhar=session["patient"])
    return render_template("patientLogin.html")

# Pharmacy Section

@app.route('/pharmacysignup', methods=['POST', 'GET'])
def pharmacysignup():
    if request.method == 'POST':
        licensenumber = request.form['licensenum']
        gstnumber = request.form['gstnumber']
        email = request.form['email']
        exist = pharmacydetail.find_one({'licensenumber': licensenumber})
        if exist is None:
            hashpass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())
            pharmacydetail.insert_one(
                {'licensenumber': licensenumber, 'gstnumber': gstnumber, 'email': email, 'password': hashpass}
            )
            session['pharmacy'] = licensenumber

            return render_template('pharmacy/dashboard.html', regnumber=licensenumber)
        message = "User Already Exist"
        return render_template("pharmacyLogin.html", message=message)
    return render_template("pharmacyLogin.html")


@app.route('/pharmacysignin', methods=['GET', 'POST'])
def pharmacysignin():
    if request.method == 'POST':
        licensenumber = request.form['licensenumber']
        userLogin = pharmacydetail.find_one({'licensenumber': licensenumber})
        if userLogin:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), userLogin['password']) == userLogin['password']:
                session['pharmacy'] = licensenumber
                return render_template('pharmacy/dashboard.html', regnumber=licensenumber)

        message = "Invalid Credentials"
        return render_template('pharmacyLogin.html', message=message)
    return render_template('pharmacyLogin.html')


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
    app.run(debug=True)
