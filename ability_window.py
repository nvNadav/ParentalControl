import tkinter as tk
import prot
from tkinter import messagebox
from tkinter import scrolledtext
import threading
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class AbilitiesWindow:
    """Class to handle the control panel once a client is connected."""
    def __init__(self, parent,user_choices, client_socket, client_name):
        self.window = tk.Toplevel(parent)
        self.window.title("Abilities Window")
        self.window.geometry("450x350")
        self.window.configure(bg="#252526")
        
        self.client_socket = client_socket
        self.client_name = client_name

        self.user_choices=user_choices
        self.df=None

        tk.Label(
            self.window,
            text=f"Connected to {client_name}",
            font=("Segoe UI", 16, "bold"),
            fg="white", bg="#252526"
        ).pack(pady=15)

        button_frame = tk.Frame(self.window, bg="#252526")
        button_frame.pack(expand=True)

        # Site actions button
        tk.Button(
            button_frame, text="Site actions", width=20, height=2,
            bg="#007ACC", fg="white", font=("Segoe UI", 11),
            command=self.open_block_sites_window
        ).pack(pady=6)

        # Gemini button
        tk.Button(
            button_frame, text="Gemini suggestion", width=20, height=2,
            bg="#007ACC", fg="white", font=("Segoe UI", 11),
            command=self.open_gemini_suggestion_window
        ).pack(pady=6)

        # Graphs button
        tk.Button(
            button_frame, text="Graphs", width=20, height=2,
            bg="#007ACC", fg="white", font=("Segoe UI", 11),
            command=self.open_graphs_window
        ).pack(pady=6)


        # Disconnect button
        tk.Button(
            self.window, text="Disconnect", bg="#f44336", fg="white",
            font=("Segoe UI", 11), width=20,
            command=self.disconnect
        ).pack(pady=15)

        # send the client the user choices
        self.send_message(f"USER_CHOICES {' '.join(self.user_choices)}")

        #start a receiving thread 
        threading.Thread(target=self.receive_messages, daemon=True).start()

        self.send_message("ATTRIBUTES")

    def open_graphs_window(self):
        graph_win = tk.Toplevel(self.window)
        graph_win.title("Graphs")
        graph_win.geometry("400x250")
        graph_win.configure(bg="#1e1e1e")
        
        tk.Label(
            graph_win,
            text="Graphs based on google history",
            fg="white",
            bg="#1e1e1e",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=15)

        button_frame = tk.Frame(graph_win, bg="#1e1e1e")
        button_frame.pack(expand=True)

        tk.Button(
            button_frame, text="visits per day", width=20, height=2,
            bg="#007ACC", fg="white", font=("Segoe UI", 11),
            activebackground="#005A9E", activeforeground="white",
            command=self.show_visits_per_day
        ).grid(row=0, column=0, padx=5, pady=5)
        
        tk.Button(
            button_frame, text="visits per hour", width=20, height=2,
            bg="#007ACC", fg="white", font=("Segoe UI", 11),
            activebackground="#005A9E", activeforeground="white",
            command=self.show_visits_per_hour
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            button_frame, text="Heatmap View", width=20, height=2,
            bg="#007ACC", fg="white", font=("Segoe UI", 11),
            activebackground="#005A9E", activeforeground="white",
            command=self.show_heatmap_hour_vs_day
        ).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(
            button_frame, text="Most Visited sites", width=20, height=2,
            bg="#007ACC", fg="white", font=("Segoe UI", 11),
            activebackground="#005A9E", activeforeground="white",
            command=self.show_visit_count_of_url
        ).grid(row=1, column=1, padx=5, pady=5)

    def open_gemini_suggestion_window(self):
        gemini_win = tk.Toplevel(self.window)
        gemini_win.title("Gemini Suggestions")
        gemini_win.geometry("400x250")
        gemini_win.configure(bg="#1e1e1e")

        tk.Label(
            gemini_win,
            text="Gemini Site Suggestions",
            fg="white",
            bg="#1e1e1e",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=15)

        # Button: suggest based on history 
        tk.Button(
            gemini_win,
            text="Suggest from browsing history",
            width=25,
            height=2,
            bg="#4CAF50",
            fg="white",
            command=lambda: self.send_message("GEMINI_SUGGEST_HISTORY")
        ).pack(pady=10)

        # --- Single site suggestion ---
        tk.Label(
            gemini_win,
            text="Enter a site:",
            fg="white",
            bg="#1e1e1e"
        ).pack(pady=(10, 3))

        url_entry = tk.Entry(gemini_win, width=30)
        url_entry.pack(pady=5)

        title_entry = tk.Entry(gemini_win, width=30)
        title_entry.pack(pady=5)

        tk.Button(
            gemini_win,
            text="Suggest for this site",
            width=25,
            height=2,
            bg="#007ACC",
            fg="white",
            command=lambda: self.single_site_helper(url_entry,title_entry,gemini_win)  
        ).pack(pady=10)

    def single_site_helper(self,url_entry,title_entry,parent_win):
        url=url_entry.get().strip()
        title=title_entry.get().strip()
        
        if not url:
            messagebox.showwarning("Input Error", "Please enter a url.", parent=parent_win)
            return
        elif not title:
            messagebox.showwarning("Input Error", "Please enter a title.", parent=parent_win)
            return
        self.send_message(f"GEMINI_SUGGEST {url} {title}")
        url_entry.delete(0, tk.END)
        title_entry.delete(0, tk.END)

        messagebox.showinfo(
            "Request Sent",
            f"Suggestion requested for:\n{title} , {url}",
            parent=parent_win
        )

    def open_block_sites_window(self):
        block_win = tk.Toplevel(self.window)
        block_win.title("Site Acctions")
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
            self.send_message("CLOSE")
            self.client_socket.close()
        self.window.destroy()

    def receive_messages(self):
        while True:
            try:
                msg = prot.receive_msg(self.client_socket)

                if not msg:
                    break
                #check if its the attribute message
                if msg.split()[0]=="ATTRIBUTES":
                    msg=" ".join(msg.split()[1:])
                    attribute=json.loads(msg)
                    self.create_data_frame(attribute)
                    continue
                
                self.window.after(0, self.show_message_window, msg)

            except Exception as e:
                print("Receive error:", e)
    def show_message_window(self, msg):
        win = tk.Toplevel(self.window)
        win.title("Message")
        win.geometry("400x250")

        text_box = scrolledtext.ScrolledText(
            win,
            wrap=tk.WORD,
            width=50,
            height=10,
            font=("Segoe UI", 10)
        )

        text_box.pack(padx=10, pady=10, fill="both", expand=True)

        text_box.insert(tk.END, msg)
        text_box.configure(state="disabled")  # read-only

    def create_data_frame(self,attributes):
        try:
            self.df = pd.DataFrame(attributes)
            self.df["datetime"] = self.df["last_visit_time"].apply(self.chrome_time_to_datetime)
            self.df["datetime"] = pd.to_datetime(self.df["datetime"], errors="coerce")
            self.df["date"] = self.df["datetime"].dt.date
            self.df["hour"] = self.df["datetime"].dt.hour
            self.df["day_name"] = self.df["datetime"].dt.day_name()

        except Exception as e:
            print("Receive error:", e)

    def show_visit_count_of_url(self):
        df_grouped = self.df.groupby("url")["visit_count"].sum().reset_index()
        df_grouped = df_grouped[df_grouped["visit_count"] > 5]
        df_grouped = df_grouped.sort_values(by="visit_count",ascending=False).head(10)

        plt.figure(figsize=(10, 6))

        sns.barplot(data=df_grouped, x="url" , y="visit_count")
        
        plt.title("Top 10 Most Visited Websites")
        plt.ylabel("Visit Count")
        plt.xlabel("Website")
        plt.xticks(rotation=45) 
        plt.tight_layout()
        plt.show()

    def show_visits_per_day(self):
        visits_per_day = self.df.groupby("date").size().reset_index(name="visits")
        plt.figure(figsize=(12, 5))

        sns.lineplot(data=visits_per_day, x="date", y="visits" , marker="o")

        plt.title("Visits Per Day")
        plt.xlabel("Date")
        plt.ylabel("Number of Visits")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def show_visits_per_hour(self):
        visits_per_hour = self.df.groupby("hour").size().reset_index(name="visits")
        plt.figure(figsize=(10, 5))
        
        sns.lineplot(data=visits_per_hour, x="hour", y="visits")
        
        plt.title("Most Active Hours of the Day")
        plt.xlabel("Hour (0–23)")
        plt.ylabel("Number of Visits")
        plt.tight_layout()
        plt.show()

    def show_heatmap_hour_vs_day(self):
        heatmap_data = self.df.pivot_table(index="day_name", columns="hour", values="visit_count", aggfunc="sum")
        days_order = ["Sunday","Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        heatmap_data = heatmap_data.reindex(days_order)
        plt.figure(figsize=(12, 6))

        sns.heatmap(heatmap_data, cmap="coolwarm", linewidths=0.2, linecolor="black")

        plt.title("Browsing Activity Heatmap")
        plt.xlabel("Hour")
        plt.ylabel("Day")
        plt.tight_layout()
        plt.show()

    def chrome_time_to_datetime(self,chrome_time):
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)


if __name__=="__main__":
    root=tk.Tk()
    root.withdraw()
    ability=AbilitiesWindow(root,[""],1,2)
    root.mainloop()
