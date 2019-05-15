import http.client
import json

conn = http.client.HTTPSConnection("***REMOVED***")

payload = "{\"client_id\":\"RDDiwomSJ3UonkAgRDJ2sZR6h0brNo9F\",\"client_secret\":\"KXnkIGkLLxd02QSSrOQ__2ZGOcnHtBGpjjHrJd2syf-o8uusVdyRgbXL4-L4eSjI\",\"audience\":\"***REMOVED***\",\"grant_type\":\"client_credentials\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()
token = json.loads(data)['access_token']
print(token)

conn = http.client.HTTPConnection("localhost:80")

headers = { 'authorization': "Bearer "+token }

conn.request("GET", "/secured/ping", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))