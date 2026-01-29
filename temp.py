import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket created")
client.connect(("127.0.0.1", 60123))
client.send(b"saar")
print ("Connected to server")