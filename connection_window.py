import tkinter as tk
import threading
import socket
import prot
import gemini_question_window

PORT = 60123

class ConnectionWindow:
    """Class to handle server startup and waiting for clients."""
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Client Connection")
        self.window.geometry("400x300")
        self.window.configure(bg="#2b2b2b")

        self.server_socket = None
        self.wait_window = None

        tk.Label(
            self.window, text="Remote Control", font=("Segoe UI", 18, "bold"),
            fg="white", bg="#2b2b2b"
        ).pack(pady=20)

        tk.Button(
            self.window, text="Wait for connection", width=22, height=2,
            bg="#4CAF50", fg="white", command=self.start_listening
        ).pack(pady=10)

        tk.Button(
            self.window, text="Exit", width=22, height=2,
            bg="#f44336", fg="white", command=self.close_app
        ).pack(pady=10)

    def start_listening(self):
        # UI for the "Waiting..." state
        self.wait_window = tk.Toplevel(self.window)
        self.wait_window.title("Waiting...")
        self.wait_window.geometry("300x150")
        self.wait_window.configure(bg="#1e1e1e")
        self.wait_window.grab_set()

        tk.Label(self.wait_window, text="Waiting for client...", fg="white", bg="#1e1e1e").pack(expand=True)

        threading.Thread(target=self._server_thread, daemon=True).start()

    def _server_thread(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("0.0.0.0", PORT))
            self.server_socket.listen(1)

            client_socket, addr = self.server_socket.accept()
            client_name = prot.receive_msg(client_socket)
            print (client_name)

            # Switch back to Main Thread to open the next window
            self.window.after(0, lambda: self.on_connect(client_socket, client_name))
        except Exception as e:
            print(f"Server Error: {e}")

    def on_connect(self, client_socket, client_name):
        if self.wait_window:
            self.wait_window.destroy()
        
        # Instantiate the gemini_question class, pass the socket
        gemini_question_window.GQWindow(self.root,client_socket,client_name)

        #ability_window.AbilitiesWindow(self.window, client_socket, client_name)

    def close_app(self):
        if self.server_socket:
            self.server_socket.close()
        self.window.destroy()
        self.root.quit()