import sqlite3
import pandas as pd
import polyline


con = sqlite3.connect("./data.db")
data = pd.read_sql_query("select * from activities", con)
print(data[:3])

summary_polyline = data["summary_polyline"].tolist()
print(summary_polyline[0])
print(polyline.decode(summary_polyline[0]))

