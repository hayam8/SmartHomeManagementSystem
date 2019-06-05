from fakesensor import DHT22


__ca_cert = "ca.crt"
__DHT22_cert = "client.crt"
__DHT22_key = "client.key"
__TLS_PORT = 8883
dummy = DHT22("***REMOVED***", __ca_cert, __DHT22_cert, __DHT22_key, __TLS_PORT)
