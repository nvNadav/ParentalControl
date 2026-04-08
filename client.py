import socket
import prot
import threading
import site_controller

SERVER_IP = "127.0.0.1"  
PORT = 60123


class Client:
    def __init__(self, name):
        self.name = name
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.site_controller = site_controller.SiteController()

    def connect(self):
        try:
            self.client_socket.connect((SERVER_IP, PORT))
            print("Connected to server")

            # send client name
            self.client_socket.send(prot.create_msg_with_header(self.name).encode())

            
        except Exception as e:
            print("Connection failed:", e)
        self.receive_messages()

    def receive_messages(self):
        functions = {"BLOCK":self.block_site}

        while True:
            try:
                msg = prot.receive_msg(self.client_socket)

                if not msg:
                    print("Server disconnected")
                    break

                lst = msg.split()
                print (lst)
                functions[lst[0]](lst)
                print("Message from server:", msg)

            except Exception as e:
                print("Receive error:", e)
                break

        self.client_socket.close()
        print ("connection closed..")
    
    #abilities
    def block_site(self,lst):
        self.site_controller.block(lst[1]) # lst[1]-> url

if __name__ == "__main__":
    client = Client("Nadav")
    client.connect()
