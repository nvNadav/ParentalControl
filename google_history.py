import sqlite3
import shutil
from datetime import datetime, timedelta
import os
from urllib.parse import urlparse

class GoogleHistory():
    def __init__(self):
        self.last_visited_sites=[] # list containing a dictionary of url, title, last_time_visited
        
        self.most_visited_sites=[] # list containing a dictionary of url, title, visit_count 

        self.history_path = r'C:\Users\USER\AppData\Local\Google\Chrome\User Data\Default\History'
        self.history_path_copy = r'C:\temp\History-copy'        
    
    def get_last_visited_sites(self, limit=50):
        if os.path.exists(self.history_path_copy):
            os.remove(self.history_path_copy)

        shutil.copy2(self.history_path, self.history_path_copy)

        with sqlite3.connect(self.history_path_copy) as conn:
            cursor = conn.cursor()

            cursor.execute("""
            SELECT url, title, last_visit_time
            FROM urls
            ORDER BY last_visit_time DESC
            LIMIT ?
            """, (limit,))

            results = []

            for url, title, last_visit_time in cursor.fetchall():
                readable_time = self.chrome_time_to_datetime(last_visit_time)
                results.append({
                    "url": self.get_domain(url),
                    "title": title,
                    "last_visit_time": readable_time
                })

        self.last_visited_sites = results
        return results
    
    def get_most_visited_sites(self, limit=50):

        if os.path.exists(self.history_path_copy):
            os.remove(self.history_path_copy)
        
        shutil.copy2(self.history_path,self.history_path_copy)

        with sqlite3.connect(self.history_path_copy) as conn:
            cursor = conn.cursor()

            cursor.execute("""
            SELECT url, title, visit_count
            FROM urls
            ORDER BY visit_count DESC
            LIMIT ?
            """, (limit,))

            results = []

            for url, title, visit_count in cursor.fetchall():
                results.append({
                    "url": self.get_domain(url),
                    "title": title,
                    "visit_count": visit_count
                })
        self.most_visited_sites=results
        return results
    
    def get_attributes(self, limit=500):

        if os.path.exists(self.history_path_copy):
            os.remove(self.history_path_copy)
        
        shutil.copy2(self.history_path,self.history_path_copy)

        with sqlite3.connect(self.history_path_copy) as conn:
            cursor = conn.cursor()

            cursor.execute("""
            SELECT url, title, visit_count,last_visit_time
            FROM urls
            LIMIT ?
            """, (limit,))

            results = []

            for url, title, visit_count, last_visit_time in cursor.fetchall():
                #readable_time = self.chrome_time_to_datetime(last_visit_time)
                results.append({
                    "url": self.get_domain(url),
                    "title": title,
                    "visit_count": visit_count,
                    "last_visit_time": last_visit_time#readable_time.strftime("%Y-%m-%d %H:%M:%S")

                })
        return results
    
    def chrome_time_to_datetime(self,chrome_time):
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)
    
    def get_domain(self,url):
        return urlparse(url).netloc