import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask
from flask import request
import json
import time


cred = credentials.Certificate('voyage.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

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
        lat = request.json['lat']
        lng = request.json['long']
        current_time = time.time()
        doc_ref = db.collection(u'images').document(u'doc'+str(current_time))
        doc_ref.set({
            u'image_id':current_time,
            u'image_string':imgstr,
            u'lat':lat,
            u'long':lng
        })


def get_all_images():
    images_string_ref = db.collection(u'images')
    docs = images_string_ref.get()
    all_images = []
    for doc in docs:
        current_doc = doc.to_dict()
        all_images.append(current_doc)
    return all_images

if __name__ == "__main__":
    app.run()