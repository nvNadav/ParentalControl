import tkinter as tk
import prot

class AbilitiesWindow:
    """Class to handle the control panel once a client is connected."""
    def __init__(self, parent, client_socket, client_name):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Control: {client_name}")
        self.window.geometry("450x350")
        self.window.configure(bg="#252526")
        
        self.client_socket = client_socket
        self.client_name = client_name

        tk.Label(
            self.window,
            text=f"Connected to {client_name}",
            font=("Segoe UI", 16, "bold"),
            fg="white", bg="#252526"
        ).pack(pady=15)

        button_frame = tk.Frame(self.window, bg="#252526")
        button_frame.pack(expand=True)

        tk.Button(
            button_frame, text="Block Sites", width=20, height=2,
            bg="#007ACC", fg="white", font=("Segoe UI", 11),
            command=self.open_block_sites_window
        ).pack(pady=6)

        tk.Button(
            self.window, text="Disconnect", bg="#f44336", fg="white",
            font=("Segoe UI", 11), width=20,
            command=self.disconnect
        ).pack(pady=15)

    def open_block_sites_window(self):
        block_win = tk.Toplevel(self.window)
        block_win.title("Block Sites")
        block_win.geometry("350x200")
        block_win.configure(bg="#1e1e1e")

        tk.Label(block_win, text="Enter URL to block:", fg="white", bg="#1e1e1e").pack(pady=10)
        url_entry = tk.Entry(block_win, width=40)
        url_entry.pack(pady=5)

        tk.Button(
            block_win, text="Send", bg="#4CAF50", fg="white", width=15,
            command=lambda: self.send_message(f"BLOCK {url_entry.get()}")
        ).pack(pady=15)

    def send_message(self, msg):
        try:
            self.client_socket.send(prot.create_msg_with_header(msg).encode())
        except Exception as e:
            print(f"Send failed: {e}")

    def disconnect(self):
        if self.client_socket:
            self.client_socket.close()
        self.window.destroy()