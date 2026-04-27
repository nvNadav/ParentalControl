import sqlite3
import shutil
from datetime import datetime, timedelta

def chrome_time_to_datetime(chrome_time):
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)

def get_last_visited_sites(limit=50):
        # Copy file to avoid lock issues
        shutil.copy2(history_path,"te")

        conn = sqlite3.connect("te")
        cursor = conn.cursor()

        # Get visited URLs
        cursor.execute("""
        SELECT url, title, last_visit_time
        FROM urls
        ORDER BY last_visit_time DESC
        LIMIT ?
        """, (limit,))
        results = []

        for url, name, last_visit_time in cursor.fetchall():
            readable_time = chrome_time_to_datetime(last_visit_time)
            results.append({
                "url": url,
                "title": name,
                "last_visit_time": readable_time
            })

        conn.close()
        return results
# history_path = r'C:\Users\USER\AppData\Local\Google\Chrome\User Data\Default\History'

# data = get_last_visited_sites(limit=10)

# for item in data:
#     print(item["title"], item["last_visit_time"])


lis=["hi","hello","goof"]
x=f"user_choices {" ".join(lis)}"
print (x)
x_split=x.split()
print(x_split)
y= x_split[1:]
print (y)