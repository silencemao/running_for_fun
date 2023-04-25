import polyline
import requests
from flask import Flask, jsonify, request, render_template, g
from flask_cors import CORS

import sqlite3
import pandas as pd
import numpy as np

app = Flask(__name__, template_folder='template')
app.config.update({
    'DATABASE': './data.db'
})

CORS(app)

key = 'your_amap_key'

# 设置全局变量
@app.before_request
def before_request():
    con = sqlite3.connect("./data.db")
    data = pd.read_sql_query("select * from activities", con)
    data.sort_values(by=["start_date_local"], inplace=True, ascending=[False])

    data["type"] = np.where(data["name"] == "run from gpx", "BIKE", "RUN")
    data["start_date_local"] = np.where(data["name"] == "run from gpx", data["start_date"], data["start_date_local"])

    print(data[:3]["start_date_local"].to_list(), data[:3]["start_date"].to_list())

    data["distance"] = round(data["distance"] / 1000, 1)

    data["minute"], data["second"] = data["moving_time"].map(lambda x: int(x[14:19].split(":")[0])), data["moving_time"].map(lambda x: int(x[14:19].split(":")[1]))
    data["mt"] = data["minute"] * 60 + data["second"]
    data["Pace"] = (data["mt"] / data["distance"]).astype("int")
    data["minute"], data["second"] = (data["Pace"] // 60).astype("str"), (data["Pace"] % 60).apply(lambda x: '{:0>2d}'.format(x)).astype("str")
    data["Pace"] = data["minute"] + ":" + data["second"]

    columns = ["run_id", "distance", "Pace", "average_heartrate", "type", "start_date_local", "summary_polyline"]
    data = data[columns]

    columns1 = ["id", "KM", "Pace", "BMP", "TYPE", "Date", "summary"]
    print(data[:3])

    data = data[columns]
    data.columns = columns1
    d_records = data.to_dict("records")
    table_data = d_records

    g.data = data
    g.table_data = table_data


def get_db():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(app.config['DATABASE'])
    return g.db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


# 定义路由
@app.route('/')
def index():
    data = g.data
    print(data[:3])
    print(data.columns)

    data["year"] = data["Date"].apply(lambda x: x[:4])
    years = sorted(data["year"].unique(), reverse=True)
    summary_data = []
    for year in years:
        tmp = dict()
        cur_year_data = data[data["year"] == year]
        tmp["year"] = year
        tmp["runs"] = cur_year_data[cur_year_data["TYPE"] == "RUN"].shape[0]
        tmp["run_km"] = round(cur_year_data[cur_year_data["TYPE"] == "RUN"]["KM"].sum(), 2)

        tmp["rides"] = cur_year_data[cur_year_data["TYPE"] == "BIKE"].shape[0]
        tmp["ride_km"] = round(cur_year_data[cur_year_data["TYPE"] == "BIKE"]["KM"].sum(), 2)

        summary_data.append(tmp)

    print(summary_data)

    return render_template('index.html', table_data=g.table_data, data=summary_data)


@app.route('/get_year_track', methods=['POST'])
def get_year_track():
    # 在此处从数据库或其他数据源获取轨迹数据
    # 并返回 JSON 格式的数据
    year_id = request.form.get('year_id')
    print("year_id", year_id)

    data = g.data
    data["year"] = data["Date"].apply(lambda x: x[:4])
    tmp = data[data["year"] == year_id]

    res_data = []
    for line_summary in tmp["summary"].to_list():
        line = polyline.decode(line_summary)
        for latlng in line:
            res_data.append({"longitude": latlng[1], "latitude": latlng[0]})

    return jsonify(res_data)


@app.route('/get_track1', methods=['POST'])
def get_track1():
    #从前端获取请求参数
    print(request.form.to_dict())
    track_id = request.form.get('track_id')
    print(track_id, type(track_id))

    data = g.data
    data["id"] = data["id"].astype("str")
    print(data[:3])
    tmp = data[data["id"] == track_id]
    print(tmp)
    print(tmp["summary"], type(tmp["summary"].to_list()[0]))

    tmp_data = polyline.decode(tmp["summary"].to_list()[0])

    res_data = []
    for latlng in tmp_data:
        res_data.append({"longitude": latlng[1], "latitude": latlng[0]})
    print(res_data)
    return jsonify(res_data)


if __name__ == '__main__':
    # print(g.table_data)
    app.run(debug=True)
