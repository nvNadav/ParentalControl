import socket
import prot
import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import requests
import json
import gemini_suggestion_api
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
        
        self.executor = ThreadPoolExecutor(max_workers=5)

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
        functions = {"BLOCK":self.block_site,"UNBLOCK":self.unblock_site,"UNBLOCK_ALL":self.unblock_all
                    ,"USER_CHOICES":self.save_user_choices,"GEMINI_SUGGEST_HISTORY":self.gemini_suggestion_history
                    ,"GEMINI_SUGGEST": self.gemini_suggestion,"ATTRIBUTES":self.send_attributes}

        while True:

            try:
                msg = prot.receive_msg(self.client_socket)

                if not msg:
                    print("Server disconnected")
                    break
                
                #print("Message from server:", msg)
                lst = msg.split()
                #print (lst)
                functions[lst[0]](lst)
                

            except Exception as e:
                print("Receive error:", e)
                break

        self.client_socket.close()
        print ("connection closed..")
    
    # Abilities
    def send_message(self,msg):
        try:
            self.client_socket.send(prot.create_msg_with_header(msg).encode())
        except Exception as e:
            print(f"Send failed: {e}")

    def block_site(self,lst):
        self.site_controller.block(lst[1]) # lst[1]-> url
    def unblock_site(self,lst):
        self.site_controller.unblock(lst[1]) # lst[1]-> url
    def unblock_all(self,lst):
        self.site_controller.unblock_all()
    
    def save_user_choices(self,lst):
        self.user_choices=lst[1:]
               
    def gemini_suggestion_history(self,lst):
        threading.Thread(target=self.gemini_worker,args=(lst,), daemon=True).start()

    def gemini_worker(self,lst):
        last_visited_sites= self.google_history.get_last_visited_sites(5)
        most_visited_sites= self.google_history.get_most_visited_sites(5)

        all_sites = last_visited_sites + most_visited_sites

        futures = [
            self.executor.submit(self.check_site_with_gemini, site)
            for site in all_sites
        ]
        results = []
        for f in as_completed(futures):
            try:
                result = f.result()
                results.append(result+"\n")
            except Exception as e:
                print("Error:", e)
        # send server the results
        self.send_message("GEMINI_RESULTS " + json.dumps(results))

    def check_site_with_gemini(self,site):
        try:
            html = requests.get(site["url"], timeout=5).text[:5000]
            answer = gemini_suggestion_api.generate(self.user_choices,site["title"],html)
            if "NO" in answer.upper(): # no means the site IS safe
                return f"{site['title']} is SAFE"
                # return {"url":site["url"],
                #         "title":site["title"],
                #         "safe":"Yes"}
            elif "YES" in answer.upper(): # yes means the site is NOT safe
                return f"{site['title']} is NOT safe"
                # return {"url":site["url"],
                #         "title":site["title"],
                #         "safe":"No"}
            else:
                return f"the model was not sure while checking {site['title']}"
                # return {"url":site["url"],
                #         "title":site["title"],
                #         "safe":"Unclear"}
        except Exception as e:
            print("Error:", e)
            return f"the model experienced high demend while checking {site['title']}"

    def gemini_suggestion(self, lst):
        threading.Thread(target=self.single_site_worker, args=(lst,), daemon=True).start()

    def single_site_worker(self, lst):
        site = {
            "url": lst[1],
            "title": lst[2]
        }

        result = self.check_site_with_gemini(site)

        # send result back
        self.send_message("GEMINI_RESULT " + json.dumps(result))

    def send_attributes(self,lst):
        attributes=self.google_history.get_attributes()
        msg=json.dumps(attributes)
        self.send_message("ATTRIBUTES "+msg)




if __name__ == "__main__":
    client = Client("Nadav")
    client.connect()
