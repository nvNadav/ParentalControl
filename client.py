import socket
import prot
import threading
import site_controller
import google_history

SERVER_IP = "127.0.0.1"  
PORT = 60123


class Client:
    def __init__(self, name):
        self.name = name
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user_choices=[]

        self.site_controller = site_controller.SiteController()
        self.google_history = google_history.GoogleHistory()
        
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
        functions = {"BLOCK":self.block_site,"UNBLOCK":self.unblock_site,"UNBLOCK_ALL":self.unblock_all
                    ,"USER_CHOICES":self.save_user_choices}

        while True:
            try:
                msg = prot.receive_msg(self.client_socket)

                if not msg:
                    print("Server disconnected")
                    break
                
                print("Message from server:", msg)
                lst = msg.split()
                print (lst)
                functions[lst[0]](lst)
                

            except Exception as e:
                print("Receive error:", e)
                break

        self.client_socket.close()
        print ("connection closed..")
    
    # Abilities
    def block_site(self,lst):
        self.site_controller.block(lst[1]) # lst[1]-> url
    def unblock_site(self,lst):
        self.site_controller.unblock(lst[1]) # lst[1]-> url
    def unblock_all(self,lst):
        self.site_controller.unblock_all()
    
    def save_user_choices(self,lst):
        self.user_choices=lst[1:]
        print(self.user_choices)
        
    def gemini_suggestion(self,lst):
        pass

if __name__ == "__main__":
    client = Client("Nadav")
    client.connect()
