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

            self.receive_messages()
        except Exception as e:
            print("Connection failed:", e)

    def receive_messages(self):
        functions = {"BLOCK":self.block_site}

        while True:
            try:
                msg = prot.receive_msg(self.client_socket)

                function = msg.split("")
                
                if not msg:
                    print("Server disconnected")
                    break

                print("Message from server:", msg)

            except Exception as e:
                print("Receive error:", e)
                break

        self.client_socket.close()
        print ("connection closed..")


if __name__ == "__main__":
    client = Client("Nadav")
    client.connect()
