import tkinter as tk
import prot
from tkinter import messagebox

class AbilitiesWindow:
    """Class to handle the control panel once a client is connected."""
    def __init__(self, parent,user_choices, client_socket, client_name):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Control: {client_name}")
        self.window.geometry("450x350")
        self.window.configure(bg="#252526")
        
        self.client_socket = client_socket
        self.client_name = client_name

        self.user_choices=user_choices

        tk.Label(
            self.window,
            text=f"Connected to {client_name}",
            font=("Segoe UI", 16, "bold"),
            fg="white", bg="#252526"
        ).pack(pady=15)

        button_frame = tk.Frame(self.window, bg="#252526")
        button_frame.pack(expand=True)

        tk.Button(
            button_frame, text="Site actions", width=20, height=2,
            bg="#007ACC", fg="white", font=("Segoe UI", 11),
            command=self.open_block_sites_window
        ).pack(pady=6)

        tk.Button(
            self.window, text="Disconnect", bg="#f44336", fg="white",
            font=("Segoe UI", 11), width=20,
            command=self.disconnect
        ).pack(pady=15)

        # send the client the user choices
        self.send_message(f"USER_CHOICES {" ".join(self.user_choices)}")
    
    def open_block_sites_window(self):
        block_win = tk.Toplevel(self.window)
        block_win.title("Manage Blocked Sites")
        block_win.geometry("500x250") 
        block_win.configure(bg="#1e1e1e")

        # Create a main container frame to hold the left and right sections
        form_frame = tk.Frame(block_win, bg="#1e1e1e")
        form_frame.pack(pady=20)

        # --- LEFT SIDE: BLOCK SECTION ---
        left_frame = tk.Frame(form_frame, bg="#1e1e1e")
        left_frame.pack(side=tk.LEFT, padx=15) # Pack to the left

        tk.Label(left_frame, text="Enter URL to block:", fg="white", bg="#1e1e1e", font=("Arial", 10, "bold")).pack(pady=(0, 5))
        block_entry = tk.Entry(left_frame, width=25)
        block_entry.pack(pady=5)

        tk.Button(
            left_frame, text="Block Site", bg="#4CAF50", fg="white", width=15,
            command=lambda: self.process_block_action("BLOCK",block_entry,block_win)
        ).pack(pady=5)

        # --- RIGHT SIDE: UNBLOCK SECTION ---
        right_frame = tk.Frame(form_frame, bg="#1e1e1e")
        right_frame.pack(side=tk.LEFT, padx=15) # Pack next to the left frame

        tk.Label(right_frame, text="Enter URL to unblock:", fg="white", bg="#1e1e1e", font=("Arial", 10, "bold")).pack(pady=(0, 5))
        unblock_entry = tk.Entry(right_frame, width=25)
        unblock_entry.pack(pady=5)

        tk.Button(
            right_frame, text="Unblock Site", bg="#FF9800", fg="white", width=15,
            command=lambda: self.process_block_action("UNBLOCK",unblock_entry,block_win)
        ).pack(pady=5)

        # --- BOTTOM: UNBLOCK ALL SECTION ---
        tk.Button(
            block_win, text="Unblock All", bg="#F44336", fg="white", width=20,
            command=lambda: self.send_message("UNBLOCK_ALL") 
        ).pack(pady=(15, 10))

    def process_block_action(self,action,entry,block_win):
        url = entry.get().strip()
        if not url:
            # Prevent sending empty messages
            messagebox.showwarning("Input Error", f"Please enter a URL to {action.lower()}.", parent=block_win)
            return
                
        self.send_message(f"{action} {url}")
        entry.delete(0, tk.END) # Clears the entry box
        messagebox.showinfo("Success", f"Successfully {action.lower()}ed:\n{url}", parent=block_win)

    def send_message(self, msg):
        try:
            self.client_socket.send(prot.create_msg_with_header(msg).encode())
        except Exception as e:
            print(f"Send failed: {e}")

    def disconnect(self):
        if self.client_socket:
            self.client_socket.close()
        self.window.destroy()

if __name__=="__main__":
    root=tk.Tk()
    root.withdraw()
    ability=AbilitiesWindow(root,[""],1,2)
    root.mainloop()
