import tkinter as tk
import UserDatabase
from tkinter import messagebox

 
class GUI:
    def __init__(self):
        self.db = UserDatabase.UserDatabase()

        self.root = tk.Tk()
        self.root.title("Login / Signup Window")
        self.root.geometry("300x200")
        self.root.configure(bg="lightblue")

        # Username label + entry
        tk.Label(self.root, text="Username:", bg="lightblue").pack(pady=5)
        self.username_entry = tk.Entry(self.root, width=25)
        self.username_entry.pack()

        # Password label + entry
        tk.Label(self.root, text="Password:", bg="lightblue").pack(pady=5)
        self.password_entry = tk.Entry(self.root, width=25, show="*")
        self.password_entry.pack()

        # Buttons
        tk.Button(self.root, text="Login", width=10, command=self.login).pack(pady=10)
        tk.Button(self.root, text="Create Account", width=15, command=self.open_signup_window).pack()

        self.signup_username = None
        self.signup_password = None
        self.signup_confirm = None
        self.signup_window = None

    def open_signup_window(self):
        self.signup_window = tk.Toplevel(self.root)
        self.signup_window.title("Create Account")
        self.signup_window.geometry("300x250")
        self.signup_window.grab_set()  # make modal (block main window)
        self.signup_window.configure(bg="lightblue")

        # Entries
        tk.Label(self.signup_window, text="Username:",bg="lightblue").pack(pady=5)
        self.signup_username = tk.Entry(self.signup_window, width=25)
        self.signup_username.pack()

        tk.Label(self.signup_window, text="Password:",bg="lightblue").pack(pady=5)
        self.signup_password = tk.Entry(self.signup_window, width=25, show="*")
        self.signup_password.pack()

        tk.Label(self.signup_window, text="Confirm Password:",bg="lightblue").pack(pady=5)
        self.signup_confirm = tk.Entry(self.signup_window, width=25, show="*")
        self.signup_confirm.pack()

        tk.Button(self.signup_window, text="Sign Up", command=self.create_user).pack(pady=10)


        def on_closing():
            if messagebox.askyesno("Exit", "Are you sure you want to close this window?"):
                self.signup_window.destroy() # Destroy the window if user confirms
        
        self.signup_window.protocol("WM_DELETE_WINDOW", on_closing)

        

    def create_user(self):
        username = self.signup_username.get()
        password = self.signup_password.get()
        confirm = self.signup_confirm.get()
        if password != confirm:
            messagebox.showerror("Confirmation Error", "Password do not match!")
        else:
            if self.db.add_user(username,password):
                messagebox.showinfo("Account Created", "Account successfully created!")
                self.signup_window.destroy()
            else:
                messagebox.showerror("Signup Error", "Username already exists!")


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not self.db.check_user(username,password):
            messagebox.showerror("Login Error", "Incorrect username or password!")
        else:
            messagebox.showinfo("Login Success", "Successfully logged in")

if __name__=="__main__":
    gui=GUI()
    gui.root.mainloop()
