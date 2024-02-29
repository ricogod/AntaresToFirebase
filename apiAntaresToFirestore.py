import requests
import json
import time 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"D:\python\api\lorawan2-firebase-adminsdk-xyepi-6e10f7c0bd.json" # ganti ini dengan alamat json verifikasi firebase
cred = credentials.Certificate(r"D:\python\api\lorawan2-firebase-adminsdk-xyepi-6e10f7c0bd.json")  # ganti ini dengan alamat json verifikasi firebase 
firebase_admin.initialize_app(cred)



db = firestore.Client()

# Prepare the data to be sent
# Antares API endpoint
url = "https://platform.antares.id:8443/~/antares-cse/antares-id/TempHumid/R720c/la" # ganti ini dengan alamat endpoint antares

# Headers for Antares API
headers = {
    'X-M2M-Origin': 'secret-key-antares', # ganti ini dengan secret key antares
    'Content-Type': 'application/json;ty=4',
    'Accept': 'application/json'
}
lastKnownTemp=0

while True:
    # Fetch data from Antares
    

    response = requests.request("GET", url, headers=headers)
    raw_data = response.json()
    
    con_dict = json.loads(raw_data['m2m:cin']['con'])
    data=con_dict["data"] 
    print(data)
    
    air_pressure = int(data[8:16], 16)/100
    temperature = int(data[16:20], 16)/100
    
    print("Air pressure: ", air_pressure, "hPa")
    print("Temperature: ", temperature, "°C")

    # Add the data to Firestore
    doc_ref = db.collection('database').document()
    if temperature != lastKnownTemp: #tidak sama dengan
        doc_ref.set({
            'temperature': temperature,
            'air_pressure': air_pressure,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        print("Data added to Firestore")
        lastKnownTemp = temperature
        print ("Last known temperature: ", lastKnownTemp)
        print("data is not same")

    elif temperature == lastKnownTemp:
        print("data is the same")

    time.sleep(2.5)
