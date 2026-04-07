import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# cli.connect(('127.0.0.1', 60123))

# Colors
BG_COLOR = "#2D2D2D"      # Dark Charcoal
ACCENT_COLOR = "#4CAF50"  # Success Green
HOVER_COLOR = "#45a049"   # Slightly darker green
TEXT_COLOR = "#F0F0F0"    # Off-white
FRAME_BG = "#383838"      # Slightly lighter gray for the box

class GQWindow:

    def __init__(self):
        # Root config
        self.root=tk.Tk()
        self.root.title("Option Collector Pro")
        self.root.geometry("400x450")
        self.root.configure(bg=BG_COLOR)

        # Style config
        self.style = ttk.Style()
        self.style.configure("TCheckbutton", 
                    background=FRAME_BG, 
                    foreground=TEXT_COLOR, 
                    font=("Segoe UI", 10))

        # Header Section
        self.header_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.header_frame.pack(fill="x", pady=(30, 10))

        tk.Label(self.header_frame, 
                text="SITES TO BLOCK", 
                font=("Segoe UI", 14, "bold"), 
                bg=BG_COLOR, 
                fg=ACCENT_COLOR).pack()

        tk.Label(self.header_frame, 
                text="Please choose site categories to block:", 
                font=("Segoe UI", 9), 
                bg=BG_COLOR, 
                fg="#AAAAAA").pack()
        
        # Options Container (The "Card")
        self.container = tk.Frame(self.root, bg=FRAME_BG, bd=1, relief="flat", padx=20, pady=20)
        self.container.pack(pady=10, padx=40, fill="both")

        self.options = ["gambling", "sports", "violent", "adult content", "gaming"]
        self.selections = {}

        for item in self.options:
            var = tk.BooleanVar()
            self.selections[item] = var
            
            # Using ttk for a cleaner look
            self.cb = ttk.Checkbutton(self.container, text=item, variable=var, style="TCheckbutton")
            self.cb.pack(anchor="w", pady=5)

        # Button
        self.save_btn = tk.Button(self.root, 
                            text="SAVE SELECTIONS", 
                            command=self.save_selections, 
                            bg=ACCENT_COLOR, 
                            fg="white", 
                            font=("Segoe UI", 10, "bold"),
                            relief="raised",
                            borderwidth=3, 
                            padx=20, 
                            pady=10,
                            cursor="hand2", # Changes cursor to a hand
                            activebackground=HOVER_COLOR,
                            activeforeground="white")
        self.save_btn.pack(pady=30)

        # Bindings
        self.save_btn.bind("<Enter>", self.on_enter)
        self.save_btn.bind("<Leave>", self.on_leave)
        # 3D Click effect
        self.save_btn.bind("<Button-1>", self.on_press)
        self.save_btn.bind("<ButtonRelease-1>", self.on_release)

        # The user's choices
        self.user_choices = []

    def start(self):
        self.root.mainloop()

    def save_selections(self):
        self.user_choices = [option for option, var in self.selections.items() if var.get()]

        if not self.user_choices: # havent chosen anything
            msg = "You haven't selected anything. Are you sure you want to proceed?"
        else:
            msg = f"You selected: {', '.join(self.user_choices)}\n\nAre you sure you want to save these?"

        #Ask for confirmation
        #askyesno returns True for 'Yes' and False for 'No'
        is_sure = messagebox.askyesno("Confirm Selections", msg)
        
        if is_sure:
            self.root.destroy() 

    # Hover effects for the button
    def on_enter(self, e):
        self.save_btn['background'] = HOVER_COLOR

    def on_leave(self, e):
        self.save_btn['background'] = ACCENT_COLOR

    def on_press(self, e):
        self.save_btn.config(relief="sunken")

    def on_release(self, e):
        self.save_btn.config(relief="raised")


if __name__=="__main__":
    gemini_window=GQWindow()
    gemini_window.start()
