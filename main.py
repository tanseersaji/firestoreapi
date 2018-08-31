import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask
from flask import request
import json
import time
import cloudinary
import cloudinary.uploader
import cloudinary.api
from math import sin, cos, sqrt, atan2, radians

cred = credentials.Certificate('voyage.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

cloudinary.config( 
  cloud_name = "dkb1nvu7q", 
  api_key = "978112495987194", 
  api_secret = "q31AssaNz2kEbGgp1owhOo5yrdw" 
)

maxDistance = 500

app = Flask(__name__)

#TODO: check if the user is corrected uploaded


@app.route('/adduser',methods=['POST','GET'])
def addUser():
    if request.method == 'POST':
        jsonData = request.json
        currentTime = str(time.time())
        doc_ref = db.collection(u'users').document(u'user'+currentTime)
        doc_ref.set(jsonData)
        return "200"
    return "403"

@app.route('/getuser')
def getUser():
    users_ref = db.collection(u'users')
    docs = users_ref.get()
    jsonstr = "{"
    for doc in docs:
        jsonstr += str(doc.id)+":"+json.dumps(doc.to_dict())+","
    jsonstr += "}"
    return jsonstr

@app.route('/storeimage',methods=['POST','GET'])
def store_image():
    if request.method == 'POST':
        imgstr = request.json['image_string']
        lat = request.json['location_lat']
        lng = request.json['location_long']
        email = request.json['user_email']
        current_time = time.time()
        doc_ref = db.collection(u'images').document(u'doc'+str(current_time))
        image_link = cloudinary.uploader.upload("data:image/png;base64,"+imgstr)
        doc_ref.set({
            u'user_email':email,
            u'image_id':current_time,
            u'image_link':image_link,
            u'lat':lat,
            u'long':lng
        })
        return str(image_link)
    else:
        return "403"

def get_all_images():
    images_string_ref = db.collection(u'images')
    docs = images_string_ref.get()
    all_images = []
    for doc in docs:
        current_doc = doc.to_dict()
        all_images.append(current_doc)
    return all_images

@app.route('/getlocationimage',methods=['POST','GET'])
def get_image_based_on_lat_long():
    if request.method == 'POST':
        currentLat = request.json["currentLat"]
        currentLong = request.json['currentLong']

        all_images = get_all_images()
        final_images = []

        for image in all_images:
            R = 6373.0
            lat1 = radians(int(image['lat']))
            lon1 = radians(int(image['long']))
            lat2 = radians(int(currentLat))
            lon2 = radians(int(currentLong))
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c

            if(distance<maxDistance):
                final_images.append({
                    'string' :image['image_link'],
                    'lat' :lat1,
                    'long' :lon1
                })
        return json.dumps(final_images)

if __name__ == "__main__":
    app.run()