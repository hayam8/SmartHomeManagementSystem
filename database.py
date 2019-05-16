import pymongo


#MongoClient object, specifying connection URL with IP address of connection
client = pymongo.MongoClient("***REMOVED***")

gateway_db = client["gateway"]

management_db = client["api"]
gateway = management_db["gateway"]
device = management_db["device"]
config = management_db["config"]

dblist = client.list_database_names()
if "local_gateway_storage" in dblist:
  print("The database exists.")

deviceTest = {"identifier":"floor_lamp",
              "name":"floor lamp",
              "device_type":"switch",
              "controller_gateway":"***REMOVED***"
              }


x = device.insert_one(deviceTest)
