import tkinter as tk
import threading
import socket
import prot
port = 60123


class mainWindow:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Main Menu")
        self.window.geometry("400x300")
        self.window.configure(bg="#2b2b2b")

        tk.Label(
            self.window,
            text="Remote Control",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#2b2b2b"
        ).pack(pady=20)

        tk.Button(
            self.window,
            text="Wait for connection",
            width=22,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Segoe UI", 11),
            command=self.wait_for_connection
        ).pack(pady=10)

        tk.Button(
            self.window,
            text="Exit",
            width=22,
            height=2,
            bg="#f44336",
            fg="white",
            font=("Segoe UI", 11),
            command=self.close
        ).pack(pady=10)

        self.wait_window = None
        self.server_socket = None
        self.client_socket = None

    # ------------------------
    # Wait for client
    # ------------------------
    def wait_for_connection(self):
        self.wait_window = tk.Toplevel(self.window)
        self.wait_window.title("Waiting for Client")
        self.wait_window.geometry("300x150")
        self.wait_window.configure(bg="#1e1e1e")
        self.wait_window.transient(self.window)
        self.wait_window.grab_set()

        tk.Label(
            self.wait_window,
            text="Waiting for client to connect...",
            font=("Segoe UI", 11),
            fg="white",
            bg="#1e1e1e"
        ).pack(expand=True)

        threading.Thread(
            target=self._accept_client_thread,
            daemon=True
        ).start()

    def _accept_client_thread(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(("0.0.0.0", port))
            self.server_socket.listen(1)

            client_socket, addr = self.server_socket.accept()
            self.client_socket = client_socket

            # 🔹 receive client name
            client_name = prot.receive_msg(client_socket)

            self.window.after(
                0,
                lambda: self.on_client_connected(addr, client_name)
            )

        except Exception as e:
            self.window.after(0, lambda: self.show_error(str(e)))

    def on_client_connected(self, addr, client_name):
        if self.wait_window:
            self.wait_window.destroy()

        print(f"Client connected from {addr}, name={client_name}")

        self.open_abilities_window(client_name)

    def show_error(self, msg):
        if self.wait_window:
            self.wait_window.destroy()
        print("Error:", msg)

    # ------------------------
    # Abilities window
    # ------------------------
    def open_abilities_window(self, client_name):
        abilities_win = tk.Toplevel(self.window)
        abilities_win.title(client_name)
        abilities_win.geometry("450x350")
        abilities_win.configure(bg="#252526")

        header = tk.Label(
            abilities_win,
            text=f"Connected to {client_name}",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#252526"
        )
        header.pack(pady=15)

        button_frame = tk.Frame(abilities_win, bg="#252526")
        button_frame.pack(expand=True)

        tk.Button(
            button_frame,
            text="Block Sites",
            width=20,
            height=2,
            bg="#007ACC",
            fg="white",
            font=("Segoe UI", 11),
            command=self.open_block_sites_window
        ).pack(pady=6)

        tk.Button(
            abilities_win,
            text="Disconnect",
            bg="#f44336",
            fg="white",
            font=("Segoe UI", 11),
            width=20,
            command=abilities_win.destroy
        ).pack(pady=15)

    def open_block_sites_window(self):
        block_win = tk.Toplevel(self.window)
        block_win.title("Block Sites")
        block_win.geometry("350x200")
        block_win.configure(bg="#1e1e1e")

        tk.Label(
            block_win,
            text="Enter URL to block:",
            font=("Segoe UI", 11),
            fg="white",
            bg="#1e1e1e"
        ).pack(pady=10)

        url_entry = tk.Entry(block_win, width=40)
        url_entry.pack(pady=5)

        tk.Button(
            block_win,
            text="Send",
            bg="#4CAF50",
            fg="white",
            width=15,
            command=lambda: self.send_message("BLOCK " + url_entry.get())
        ).pack(pady=15)

    def send_message(self, msg):
        if not self.client_socket:
            print("No client connected.")
            return
        try:
            self.client_socket.send(prot.create_msg_with_header(msg).encode())
        except Exception as e:
            print("Send failed:", e)

    # ------------------------
    # Exit
    # ------------------------
    def close(self):
        self.window.destroy()
        self.root.deiconify()
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()
