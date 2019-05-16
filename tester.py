from flask import Flask
import json
from six.moves.urllib.request import urlopen
from functools import wraps
from flask_cors import cross_origin
from flask import Flask, request, jsonify, _request_ctx_stack
import jwt 
AUTH0_DOMAIN = '***REMOVED***'
API_AUDIENCE = '***REMOVED***'
ALGORITHMS = "RS256"

# jwt.decode('', algorithms=['RS256'])
payload = {
    'some': 'payload',
    'iss': 'urn:foo'
}
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlFUQTFNVGRHUXpJeU5USkRPREEzTkVOQ1FVRTBPRUV6TVVaRFFqbEdOalZGUWpJelFUZ3pOZyJ9.eyJpc3MiOiJodHRwczovL2dhdGV3YXktbWFuYWdlbWVudC5hdXRoMC5jb20vIiwic3ViIjoiUkREaXdvbVNKM1VvbmtBZ1JESjJzWlI2aDBick5vOUZAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vZ2F0ZXdheS1tYW5hZ2VtZW50LmF1dGgwLmNvbS9hcGkvdjIvIiwiaWF0IjoxNTU3OTgxNzk3LCJleHAiOjE1NTgwNjgxOTcsImF6cCI6IlJERGl3b21TSjNVb25rQWdSREoyc1pSNmgwYnJObzlGIiwic2NvcGUiOiJyZWFkOmNsaWVudF9rZXlzIHVwZGF0ZTpjbGllbnRfa2V5cyBjcmVhdGU6Y2xpZW50X2tleXMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.k5s0unBBTGv9dXEA0D6YLskkH0pCviCFuz_Tdt6qS1ARJWXZZD56JndAWD66oliwH6uJ1_3dHEKcbEXUEaNIFvjUWTPSkeb0NYKuCPnpG43bsECebF4UA0vOnChqsyewa5MPP7lnBv07isJkFI8eouHODZwPEeoALPYi99PZ_IWidhR5XK-r7Kcj_QYZ_LQcNRSfzJ3S82aUdeujkY6KihOMFe21m2OHpaqt2uqIdY95JNRKXYJOPxDbZUBhzc-FTmzzPY7RZkZG7hq8EoDWMjbRdT-eDJGtjDWWTWS93EidNRb0SegmjWlHbpe9rHWW-bmCIdt2_D6OOdnd7xiJWA'
# tokens = jwt.encode(payload)
# decoded = jwt.decode(token, issuer='urn:foo', algorithms=['HS256'])
# print(decoded)


jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
jwks = json.loads(jsonurl.read())
unverified_header = jwt.get_unverified_header(token)
# print(unverified_header)
rsa_key = {}

for key in jwks["keys"]:
    if key["kid"] == unverified_header["kid"]:
        print("here")
        rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
print(rsa_key)
payload = jwt.encode(
                    rsa_key,'KXnkIGkLLxd02QSSrOQ__2ZGOcnHtBGpjjHrJd2syf-o8uusVdyRgbXL4-L4eSjI',algorithm='RS256'
                )
print(payload)