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

@app.route('/getuser')
def getUser():
    users_ref = db.collection(u'users')
    docs = users_ref.get()
    jsonstr = "{"
    for doc in docs:
        jsonstr += str(doc.id)+":"+json.dumps(doc.to_dict())+","
    jsonstr += "}"
    return jsonstr

if __name__ == "__main__":
    app.run()