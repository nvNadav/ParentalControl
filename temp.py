# import sqlite3
# import shutil
# from datetime import datetime, timedelta

# def chrome_time_to_datetime(chrome_time):
#     return datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)

# def get_last_visited_sites(limit=50):
#         # Copy file to avoid lock issues
#         shutil.copy2(history_path,"te")

#         conn = sqlite3.connect("te")
#         cursor = conn.cursor()

#         # Get visited URLs
#         cursor.execute("""
#         SELECT url, title, last_visit_time
#         FROM urls
#         ORDER BY last_visit_time DESC
#         LIMIT ?
#         """, (limit,))
#         results = []

#         for url, name, last_visit_time in cursor.fetchall():
#             readable_time = chrome_time_to_datetime(last_visit_time)
#             results.append({
#                 "url": url,
#                 "title": name,
#                 "last_visit_time": readable_time
#             })

#         conn.close()
#         return results
# # history_path = r'C:\Users\USER\AppData\Local\Google\Chrome\User Data\Default\History'

# # data = get_last_visited_sites(limit=10)

# # for item in data:
# #     print(item["title"], item["last_visit_time"])
import google_history
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

gh=google_history.GoogleHistory()
attributes=gh.get_attributes()
df = pd.DataFrame(attributes)
def chrome_time_to_datetime(chrome_time):
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)


df["datetime"] = df["last_visit_time"].apply(chrome_time_to_datetime)

df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")


df["date"] = df["datetime"].dt.date
df["hour"] = df["datetime"].dt.hour
df["day_name"] = df["datetime"].dt.day_name()


# Visit count bar plot

df_grouped = df.groupby("url")["visit_count"].sum().reset_index()
df_grouped = df_grouped[df_grouped["visit_count"] > 5]
df_grouped = df_grouped.sort_values(by="visit_count",ascending=False).head(10)


# plt.figure(figsize=(10, 6))
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

sns.barplot(data=df_grouped, x="url" , y="visit_count" , ax=axes[0, 0])
axes[0, 0].set_title("Top Sites")


# plt.title("Top 10 Most Visited Websites")
# plt.ylabel("Visit Count")
# plt.xlabel("Website")
# plt.xticks(rotation=45) 
# plt.tight_layout()
# plt.show()


# Visits per day

visits_per_day = df.groupby("date").size().reset_index(name="visits")

#plt.figure(figsize=(12, 5))

sns.lineplot(data=visits_per_day, x="date", y="visits" , marker="o" ,ax=axes[0, 1])
axes[0, 1].set_title("Visits Per Day")

# plt.title("Visits Per Day")
# plt.xlabel("Date")
# plt.ylabel("Number of Visits")
# plt.xticks(rotation=45)

# plt.tight_layout()
# plt.show()


# Visit per hour

visits_per_hour = df.groupby("hour").size().reset_index(name="visits")

#plt.figure(figsize=(10, 5))
sns.lineplot(data=visits_per_hour, x="hour", y="visits", ax=axes[1,0])
axes[1, 0].set_title("Active Hours")

# plt.title("Most Active Hours of the Day")
# plt.xlabel("Hour (0–23)")
# plt.ylabel("Number of Visits")

# plt.tight_layout()
# plt.show()

# Heatmap Hour of day number of visitations

heatmap_data = df.pivot_table(
    index="day_name",
    columns="hour",
    values="visit_count",
    aggfunc="sum"
)

# Order days correctly
days_order = ["Sunday","Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
heatmap_data = heatmap_data.reindex(days_order)

#plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap="coolwarm", linewidths=0.2, linecolor="black", ax=axes[1, 1])
axes[1, 1].set_title("Heatmap")

plt.tight_layout()
plt.show()

# plt.title("Browsing Activity Heatmap")
# plt.xlabel("Hour")
# plt.ylabel("Day")

# plt.show()
def show_visits_per_day():
        visits_per_day = df.groupby("date").size().reset_index(name="visits")
        plt.figure(figsize=(12, 5))

        sns.lineplot(data=visits_per_day, x="date", y="visits" , marker="o")

        plt.title("Visits Per Day")
        plt.xlabel("Date")
        plt.ylabel("Number of Visits")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
show_visits_per_day()