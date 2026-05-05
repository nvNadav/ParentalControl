import tkinter as tk
import UserDatabase
from tkinter import messagebox
import connection_window



class GUI:
    def __init__(self):
        self.db = UserDatabase.UserDatabase()

        self.root = tk.Tk()
        self.root.title("Login / Signup Window")
        self.root.geometry("300x280") 
        self.root.configure(bg="#1e1e1e")

        main_frame = tk.Frame(self.root, bg="#1e1e1e")
        main_frame.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)

        # Username label + entry
        tk.Label(main_frame, text="Username:", bg="#1e1e1e", fg="white", font=("Arial", 10, "bold")).pack(pady=(0, 5))
        self.username_entry = tk.Entry(main_frame, width=25, font=("Arial", 10))
        self.username_entry.pack(pady=5, ipady=3)
        self.add_placeholder(self.username_entry, "Enter your username...")

        # Password label + entry
        tk.Label(main_frame, text="Password:", bg="#1e1e1e", fg="white", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        self.password_entry = tk.Entry(main_frame, width=25, font=("Arial", 10))
        self.password_entry.pack(pady=5, ipady=3)
        self.add_placeholder(self.password_entry, "Enter your password...", is_password=True)

        # Buttons 
        tk.Button(
            main_frame, text="Login", bg="#4CAF50", fg="white", 
            relief="raised", borderwidth=3, cursor="hand2", font=("Arial", 10, "bold"),
            command=self.login
        ).pack(pady=(15, 5), fill=tk.X, ipady=3)

        tk.Button(
            main_frame, text="Create Account", bg="#2196F3", fg="white", 
            relief="raised", borderwidth=3, cursor="hand2", font=("Arial", 10, "bold"),
            command=self.open_signup_window
        ).pack(pady=5, fill=tk.X, ipady=3)

        self.signup_username = None
        self.signup_password = None
        self.signup_confirm = None
        self.signup_window = None

        def on_closing():
            if messagebox.askyesno("Exit", "Are you sure you want to close this window?", parent=self.root):
                self.root.destroy() 
        
        self.root.protocol("WM_DELETE_WINDOW", on_closing)


    def open_signup_window(self):
        self.signup_window = tk.Toplevel(self.root)
        self.signup_window.title("Create Account")
        self.signup_window.geometry("300x350") 
        self.signup_window.grab_set() 
        self.signup_window.configure(bg="#1e1e1e")

        signup_frame = tk.Frame(self.signup_window, bg="#1e1e1e")
        signup_frame.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)

        # Entries with placeholders
        tk.Label(signup_frame, text="Username:", bg="#1e1e1e", fg="white", font=("Arial", 10, "bold")).pack(pady=(0, 5))
        self.signup_username = tk.Entry(signup_frame, width=25, font=("Arial", 10))
        self.signup_username.pack(pady=5, ipady=3)
        self.add_placeholder(self.signup_username, "Choose a username...")

        tk.Label(signup_frame, text="Password:", bg="#1e1e1e", fg="white", font=("Arial", 10, "bold")).pack(pady=(5, 5))
        self.signup_password = tk.Entry(signup_frame, width=25, font=("Arial", 10))
        self.signup_password.pack(pady=5, ipady=3)
        self.add_placeholder(self.signup_password, "Create a password...", is_password=True)

        tk.Label(signup_frame, text="Confirm Password:", bg="#1e1e1e", fg="white", font=("Arial", 10, "bold")).pack(pady=(5, 5))
        self.signup_confirm = tk.Entry(signup_frame, width=25, font=("Arial", 10))
        self.signup_confirm.pack(pady=5, ipady=3)
        self.add_placeholder(self.signup_confirm, "Confirm your password...", is_password=True)

        tk.Button(
            signup_frame, text="Sign Up", bg="#4CAF50", fg="white", 
            relief="raised", borderwidth=3, cursor="hand2", font=("Arial", 10, "bold"),
            command=self.create_user
        ).pack(pady=(15, 5), fill=tk.X, ipady=3)

        def on_closing():
            if messagebox.askyesno("Exit", "Are you sure you want to close this window?", parent=self.signup_window):
                self.signup_window.destroy() 
        
        self.signup_window.protocol("WM_DELETE_WINDOW", on_closing)

    # --- HELPER FUNCTION FOR PLACEHOLDERS ---
    def add_placeholder(self, entry, placeholder_text, is_password=False):
        entry.insert(0, placeholder_text)
        entry.config(fg="gray")
        if is_password:
            entry.config(show="") # Show the placeholder text normally, not as asterisks

        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, tk.END)
                entry.config(fg="black") # Change to normal text color
                if is_password:
                    entry.config(show="*") # Turn on asterisks for typing

        def on_focus_out(event):
            if not entry.get(): # If they leave the box empty, put placeholder back
                if is_password:
                    entry.config(show="")
                entry.insert(0, placeholder_text)
                entry.config(fg="gray")

        # Bind the click-in and click-out events
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)


    def create_user(self):
        username = self.signup_username.get()
        password = self.signup_password.get()
        confirm = self.signup_confirm.get()

        # Prevent the database from trying to save the literal placeholder text
        if username == "Choose a username...": username = ""
        if password == "Create a password...": password = ""
        if confirm == "Confirm your password...": confirm = ""

        if not username or not password:
            messagebox.showerror("Error", "Please fill out all fields.", parent=self.signup_window)
            return

        if password != confirm:
            messagebox.showerror("Confirmation Error", "Passwords do not match!", parent=self.signup_window)
        else:
            if self.db.add_user(username, password):
                messagebox.showinfo("Account Created", "Account successfully created!", parent=self.signup_window)
                self.signup_window.destroy()
            else:
                messagebox.showerror("Signup Error", "Username already exists!", parent=self.signup_window)


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Ignore the placeholder text if they hit login without typing anything
        if username == "Enter your username...": username = ""
        if password == "Enter your password...": password = ""

        if not self.db.check_user(username, password):
            messagebox.showerror("Login Error", "Incorrect username or password!", parent=self.root)
        else:
            self.root.withdraw()  
            connection_window.ConnectionWindow(self.root)

if __name__=="__main__":
    gui=GUI()
    gui.root.mainloop()