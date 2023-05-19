from datetime import datetime
import requests
import uuid

def generate_unique_token():
    token = str(uuid.uuid4())
    return token

def get_details(aadhaar):
    url = f"https://testapi-11co.onrender.com/aadhaar/{aadhaar}"
    response = requests.get(url)
    length=len(response.json())
    if length>1:
        data = response.json()
        dob = data['DOB']
        age = calculate_age(dob)
    else:
        return None
    return {
        'aadhaar': data['adhar_no'],
        'name': data['name'],
        'dob': dob,
        'age': age,
        'gender': data['gender'],
        'address': data['address'],
        'mobile': data['mobile_no']
    }

def get_licence_detail(licence):
    url = f"https://pharmacyapi.onrender.com/licence/{licence}"
    response = requests.get(url)
    length=len(response.json())
    print(response.json())
    if length>1:
        data = response.json()
    else:
        return None
    return {
        'licence': data['licence'],
        'gst' : data['gst_no'],
        'name': data['name'],
        'address': data['address'],
        'mobile': data['mobile_number']
    }

def calculate_age(dob):
    dob_datetime = datetime.strptime(dob, "%Y-%m-%d").date()
    today = datetime.now().date()
    age = today.year - dob_datetime.year
    if today < dob_datetime.replace(year=today.year):
        age -= 1
    return age