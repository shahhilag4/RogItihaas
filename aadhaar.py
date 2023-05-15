from datetime import datetime
import requests

def get_details(aadhaar):
    url = f"https://testapi-11co.onrender.com/aadhaar/{aadhaar}"
    response = requests.get(url)
    length=len(response.json())
    
    if length>1:
        data = response.json()
        dob = data['DOB']
        age = calculate_age(dob)
    else:
        return "Aadhaar record not found"
    return {
        'aadhaar': data['adhar_no'],
        'name': data['name'],
        'dob': dob,
        'age': age,
        'gender': data['gender'],
        'address': data['address'],
        'mobile': data['mobile_no']
    }

def calculate_age(dob):
    dob_datetime = datetime.strptime(dob, "%Y-%m-%d").date()
    today = datetime.now().date()
    age = today.year - dob_datetime.year
    if today < dob_datetime.replace(year=today.year):
        age -= 1
    return age
