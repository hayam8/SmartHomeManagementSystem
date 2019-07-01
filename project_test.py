from fakesensor import DHT22
"""
This file is used as a test file for connecting to the gateway broker and publishing messages. Certificates were switched 
out for incorrectly signed certificates or removed entirely for testing.
Author: Haya Majeed
"""

__ca_cert = "***REMOVED***"
__DHT22_cert = "***REMOVED***"
__DHT22_key = "***REMOVED***"
__gateway_name = ""
__TLS_PORT = 8883
dummy = DHT22(__gateway_name, __ca_cert,  __TLS_PORT)
