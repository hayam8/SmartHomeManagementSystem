import http.client
import json
from six.moves.urllib.request import urlopen
conn = http.client.HTTPSConnection("***REMOVED***")

payload = "{\"client_id\":\"RDDiwomSJ3UonkAgRDJ2sZR6h0brNo9F\",\"client_secret\":\"KXnkIGkLLxd02QSSrOQ__2ZGOcnHtBGpjjHrJd2syf-o8uusVdyRgbXL4-L4eSjI\",\"audience\":\"***REMOVED***\",\"grant_type\":\"client_credentials\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()
token = json.loads(data)['access_token']

jsonurl = urlopen("https://***REMOVED***/.well-known/jwks.json")
        
jwks = json.loads(jsonurl.read())
***REMOVED***

***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***

***REMOVED***
***REMOVED***

***REMOVED***
conn = http.client.HTTPConnection("***REMOVED***")

headers = { 'authorization': "Bearer "+ token }


conn.request("GET", "/device", headers=headers)

res = conn.getresponse()
data = res.read()
# print(token)
# print(data.decode("utf-8"))


# client = MongoClient("23.99.178.246/?ssl=true") #host uri
# db = client.test    #Select the database
# db.authenticate(name="localhost",password='C2y6yDjf5' + r'/R' + '+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw' + r'/Jw==')
from flask import Flask, request
from flask import render_template
from flask_pymongo import PyMongo,MongoClient
app = Flask(__name__)
uri = "***REMOVED***"
db = MongoClient(uri)
database = db['db']
collection = database['device']
post_data = {
    'name': 'Python and MongoDB',
    'device_type':'this that test'
}
# result = collection.insert_one(post_data)

# device = db.db.device
# output = []
# for d in device.find():
#     output.append({'name':d['name'], 'device_type': d['device_type']})
# print(output)    device = mongo.db.device
headers = { 'authorization': "Bearer "+ token, 'device_id':'try', 'name':'Ethan',
 'identifier':'Ethan', 'device_type':'Ethan', 'controller_gateway':'Ethan'}

conn.request("PUT", "/device", headers=headers)

res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))


# device_id = request.json['device_id']
# identifier = request.json['identifier']
# name = request.json['name']
# device_type = request.json['device_type']
# controller_gateway = request.json['controller_gateway']
# new_device_id = device.insert({'device_id' : device_id, 'identifier' : identifier, 'name': name, 'device_type' : device_type, 'controller_gateway' : controller_gateway})
# new_device = device.find_one({'_id': new_device_id})
# output = {'device_id' : new_device['device_id'], 'identifier' : new_device['identifier'], 'name': new_device['name'], 'device_type' : new_device['device_type'], 'controller_gateway' : new_device['controller_gateway']}
# print(jsonify({'result': output}))
