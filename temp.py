import socket
import prot

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket created")
client.connect(("127.0.0.1", 60123))
client.send(prot.create_msg_with_header("nadav").encode())
print ("Connected to server")