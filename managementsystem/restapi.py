
""""
app = Flask(__name__) #creates instance of flask application

@app.route("/") #defines route code is executed if we access localhost:5000/

def hello_world():
    return "Hello, World!"

if __name__== '__main__':
    app.run(debug=True)
"""
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'api'
app.config['MONGO_URI'] = ''
mongo =PyMongo(app)

#/api/gateway/<string:gateway_id>[—downloads information about a gateway with identiﬁcation number expressed by a gateway_id parameter
#/api/device/<string:device_id>[—downloads information about a device with identiﬁcation number expressed by a gateway_id parameter
#/api/conﬁg/<string:gateway_id>[—downloads most up-to-date conﬁguration for a gateway with identiﬁcation number expressed by a gateway_id parameter

"""
downloads information about a gateway with identiﬁcation number expressed by a gateway_id parameter
"""
@app.route('/gateway/<string:gateway_id>')
def get_gateway(gateway_id):
    return


# downloads information about all devices
@app.route("/device", methods=['GET'])
def get_all_devices():
    device = mongo.db.device
    output = []
    for d in device.find():
        output.append({'name':d['name'], 'device_type': d['device_type']})
    return jsonify({'result' : output})

"""
downloads information about a device with identiﬁcation number expressed by a DEVICE_id parameter
Information returned is a json format containing: device id, identifier, name, device_type, controller_gateway
"""
@app.route("/device/<string:device_id>", methods = ['GET'])
def get_device(device_id):
    device = mongo.db.device
    d = device.find_one({'device_id' : device_id})
    if(d):
        output = {'device_id': d['device_id'], 'identifier' : d['identifier'], 'name' : d['name'], 'device_type' : d['device_type'], 'controller_gateway' : d['controller_gateway']}
    else:
        output = "No such device ID"
    return jsonify({'result' : output})

"""
api/device—adds to the system information about a device described in a message 
Information added is a json format containing: device id, identifier, name, device_type, controller_gateway
"""
@app.route("/device", methods = ['PUT'])
def add_device():
    device = mongo.db.device
    device_id = request.json['device_id']
    identifier = request.json['identifier']
    name = request.json['name']
    device_type = request.json['device_type']
    controller_gateway = request.json['controller_gateway']
    new_device_id = device.insert({'device_id' : device_id, 'identifier' : identifier, 'name': name, 'device_type' : device_type, 'controller_gateway' : controller_gateway})
    new_device = device.find_one({'_id': new_device_id})
    output = {'device_id' : new_device['device_id'], 'identifier' : new_device['identifier'], 'name': new_device['name'], 'device_type' : new_device['device_type'], 'controller_gateway' : new_device['controller_gateway']}
    return jsonify({'result': output})




if __name__ == '__main__':
    app.run(debug=True)

