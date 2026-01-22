import tkinter as tk
import threading
import socket

port = 60123


class mainWindow:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Main Menu")
        self.window.geometry("400x300")

        tk.Button(
            self.window,
            text="Wait for connection",
            width=20,
            command=self.wait_for_connection
        ).pack(pady=20)

        tk.Button(
            self.window,
            text="Exit",
            command=self.close
        ).pack(pady=20)

        self.wait_window = None
        self.server_socket = None
        self.client_socket = None

    # ------------------------
    # Wait for client
    # ------------------------
    def wait_for_connection(self):
        # Open waiting window
        self.wait_window = tk.Toplevel(self.window)
        self.wait_window.title("Waiting")
        self.wait_window.geometry("300x150")
        self.wait_window.transient(self.window)
        self.wait_window.grab_set()

        tk.Label(
            self.wait_window,
            text="Waiting for client to connect...",
            font=("Arial", 12)
        ).pack(pady=30)

        # Start thread for blocking accept()
        threading.Thread(target=self._accept_client_thread, daemon=True).start()

    def _accept_client_thread(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(("0.0.0.0", port))
            self.server_socket.listen(1)

            client_socket, addr = self.server_socket.accept()
            self.client_socket = client_socket

            # GUI update on main thread
            self.window.after(0, lambda: self.on_client_connected(addr))

        except Exception as e:
            self.window.after(0, lambda: self.show_error(str(e)))

    def on_client_connected(self, addr):
        if self.wait_window:
            self.wait_window.destroy()

        tk.Label(self.window, text=f"Connected: {addr[0]}:{addr[1]}").pack(pady=10)
        print(f"Client connected from {addr}")

        # Open your abilities window
        self.open_abilities_window()

    def show_error(self, msg):
        if self.wait_window:
            self.wait_window.destroy()
        print("Error:", msg)

    # ------------------------
    # Abilities window (buttons)
    # ------------------------
    def open_abilities_window(self):
        abilities_win = tk.Toplevel(self.window)
        abilities_win.title("Abilities")
        abilities_win.geometry("400x300")

        # Example buttons
        tk.Button(abilities_win, text="Ability 1", command=lambda: self.use_ability(1)).pack(pady=10)
        tk.Button(abilities_win, text="Ability 2", command=lambda: self.use_ability(2)).pack(pady=10)
        tk.Button(abilities_win, text="Exit", command=abilities_win.destroy).pack(pady=20)

    def use_ability(self, n):
        print(f"Using ability {n}")
        # Here you can send a message to the client using self.client_socket
        if self.client_socket:
            self.client_socket.send(f"Ability {n} activated".encode())

    # ------------------------
    # Exit
    # ------------------------
    def close(self):
        self.window.destroy()
        self.root.deiconify()  # show login again
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()
