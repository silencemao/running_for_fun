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
    summary_data = dict()

    print(data["Date"].max()[:4])
    summary_data["year"] = data["Date"].max()[:4]
    summary_data["runs"] = data[data["Date"] >= summary_data["year"]].shape[0]
    summary_data["all_km"] = data["KM"].sum()
    print(summary_data)

    return render_template('index.html', table_data=g.table_data, data=summary_data)


@app.route('/api/get_trajectory', methods=['POST'])
def get_trajectory():
    # 在此处从数据库或其他数据源获取轨迹数据
    # 并返回 JSON 格式的数据
    trajectory_id = request.form.get('trajectory_id')
    # 假设我们从数据库中获取轨迹数据
    trajectory = [[1, 2], [3, 4]]
    # 将轨迹数据封装成 JSON 格式并返回
    return jsonify({'trajectory': trajectory})


@app.route('/get_track', methods=['POST'])
def get_track():
    #从前端获取请求参数
    print(request.form.to_dict())
    track_id = request.form.get('track_id')
    print(track_id, type(track_id))

    #发送GET请求获取轨迹数据
    res = requests.get('http://example.com/track', params={'track_id': track_id})
    # data = res.json()

    if track_id == '1':
        data = [{'longitude': 116.4192, 'latitude': 40.0762}, {'longitude': 116.41921, 'latitude': 40.07618}, {'longitude': 116.41926, 'latitude': 40.07618}, {'longitude': 116.41937, 'latitude': 40.07617}, {'longitude': 116.4195, 'latitude': 40.07618}, {'longitude': 116.4194, 'latitude': 40.07618}, {'longitude': 116.41962, 'latitude': 40.07609}, {'longitude': 116.41961, 'latitude': 40.07597}, {'longitude': 116.41959, 'latitude': 40.07585}, {'longitude': 116.41952, 'latitude': 40.07574}, {'longitude': 116.41944, 'latitude': 40.07564}, {'longitude': 116.41936, 'latitude': 40.07553}, {'longitude': 116.41933, 'latitude': 40.07541}, {'longitude': 116.41922, 'latitude': 40.07531}, {'longitude': 116.41908, 'latitude': 40.07523}, {'longitude': 116.41895, 'latitude': 40.07515}, {'longitude': 116.41885, 'latitude': 40.07506}, {'longitude': 116.41874, 'latitude': 40.07502}, {'longitude': 116.41872, 'latitude': 40.0749}, {'longitude': 116.4187, 'latitude': 40.07477}, {'longitude': 116.41873, 'latitude': 40.07464}, {'longitude': 116.41874, 'latitude': 40.07451}, {'longitude': 116.41871, 'latitude': 40.07439}, {'longitude': 116.41872, 'latitude': 40.07426}, {'longitude': 116.41872, 'latitude': 40.07415}, {'longitude': 116.41878, 'latitude': 40.07413}, {'longitude': 116.41882, 'latitude': 40.07406}, {'longitude': 116.41882, 'latitude': 40.07393}, {'longitude': 116.41883, 'latitude': 40.07375}, {'longitude': 116.41884, 'latitude': 40.07359}, {'longitude': 116.41878, 'latitude': 40.07346}, {'longitude': 116.41876, 'latitude': 40.07332}, {'longitude': 116.41876, 'latitude': 40.07319}, {'longitude': 116.41877, 'latitude': 40.07305}, {'longitude': 116.41873, 'latitude': 40.07292}, {'longitude': 116.41855, 'latitude': 40.07292}, {'longitude': 116.41837, 'latitude': 40.07293}, {'longitude': 116.4182, 'latitude': 40.07292}, {'longitude': 116.41804, 'latitude': 40.07294}, {'longitude': 116.41785, 'latitude': 40.07293}, {'longitude': 116.41768, 'latitude': 40.07294}, {'longitude': 116.41751, 'latitude': 40.07294}, {'longitude': 116.41732, 'latitude': 40.07294}, {'longitude': 116.41714, 'latitude': 40.07294}, {'longitude': 116.41698, 'latitude': 40.07293}, {'longitude': 116.41681, 'latitude': 40.07293}, {'longitude': 116.41665, 'latitude': 40.07293}, {'longitude': 116.41647, 'latitude': 40.07292}, {'longitude': 116.41632, 'latitude': 40.07291}, {'longitude': 116.41617, 'latitude': 40.07292}, {'longitude': 116.41601, 'latitude': 40.07292}, {'longitude': 116.41588, 'latitude': 40.07293}, {'longitude': 116.41572, 'latitude': 40.07293}, {'longitude': 116.41557, 'latitude': 40.07293}, {'longitude': 116.41543, 'latitude': 40.07293}, {'longitude': 116.41533, 'latitude': 40.07301}, {'longitude': 116.41532, 'latitude': 40.07313}, {'longitude': 116.41534, 'latitude': 40.07324}, {'longitude': 116.41533, 'latitude': 40.07335}, {'longitude': 116.41531, 'latitude': 40.07347}, {'longitude': 116.41528, 'latitude': 40.07359}, {'longitude': 116.4153, 'latitude': 40.07371}, {'longitude': 116.41528, 'latitude': 40.07384}, {'longitude': 116.41528, 'latitude': 40.07395}, {'longitude': 116.41529, 'latitude': 40.0741}, {'longitude': 116.41528, 'latitude': 40.07423}, {'longitude': 116.41528, 'latitude': 40.07434}, {'longitude': 116.41528, 'latitude': 40.07446}, {'longitude': 116.41529, 'latitude': 40.07458}, {'longitude': 116.4153, 'latitude': 40.07468}, {'longitude': 116.41534, 'latitude': 40.07475}, {'longitude': 116.41528, 'latitude': 40.07487}, {'longitude': 116.41529, 'latitude': 40.075}, {'longitude': 116.41528, 'latitude': 40.07512}, {'longitude': 116.41529, 'latitude': 40.07525}, {'longitude': 116.41528, 'latitude': 40.07537}, {'longitude': 116.41527, 'latitude': 40.07549}, {'longitude': 116.41528, 'latitude': 40.07561}, {'longitude': 116.41529, 'latitude': 40.07573}, {'longitude': 116.41528, 'latitude': 40.07585}, {'longitude': 116.41528, 'latitude': 40.07597}, {'longitude': 116.41529, 'latitude': 40.07611}, {'longitude': 116.41528, 'latitude': 40.07624}, {'longitude': 116.41529, 'latitude': 40.07637}, {'longitude': 116.41529, 'latitude': 40.07651}, {'longitude': 116.41529, 'latitude': 40.07664}, {'longitude': 116.41528, 'latitude': 40.07676}, {'longitude': 116.41527, 'latitude': 40.07688}, {'longitude': 116.41528, 'latitude': 40.07701}, {'longitude': 116.41528, 'latitude': 40.07715}, {'longitude': 116.41528, 'latitude': 40.07727}, {'longitude': 116.41528, 'latitude': 40.07741}, {'longitude': 116.4153, 'latitude': 40.07753}, {'longitude': 116.41528, 'latitude': 40.07767}, {'longitude': 116.41529, 'latitude': 40.0778}, {'longitude': 116.41531, 'latitude': 40.07793}, {'longitude': 116.41537, 'latitude': 40.07806}, {'longitude': 116.41553, 'latitude': 40.07807}, {'longitude': 116.41571, 'latitude': 40.07807}, {'longitude': 116.41589, 'latitude': 40.07809}, {'longitude': 116.41605, 'latitude': 40.07809}, {'longitude': 116.41621, 'latitude': 40.07809}, {'longitude': 116.41636, 'latitude': 40.07809}, {'longitude': 116.41653, 'latitude': 40.07809}, {'longitude': 116.4167, 'latitude': 40.0781}, {'longitude': 116.41685, 'latitude': 40.07809}, {'longitude': 116.41701, 'latitude': 40.07806}, {'longitude': 116.41719, 'latitude': 40.07806}, {'longitude': 116.41737, 'latitude': 40.07805}, {'longitude': 116.41756, 'latitude': 40.07811}, {'longitude': 116.41768, 'latitude': 40.07816}, {'longitude': 116.41783, 'latitude': 40.07809}, {'longitude': 116.41799, 'latitude': 40.07809}, {'longitude': 116.41817, 'latitude': 40.07811}, {'longitude': 116.41833, 'latitude': 40.07808}, {'longitude': 116.41849, 'latitude': 40.07809}, {'longitude': 116.41865, 'latitude': 40.07808}, {'longitude': 116.41882, 'latitude': 40.07807}, {'longitude': 116.41901, 'latitude': 40.07808}, {'longitude': 116.4192, 'latitude': 40.07807}, {'longitude': 116.41938, 'latitude': 40.07807}, {'longitude': 116.41956, 'latitude': 40.07807}, {'longitude': 116.41974, 'latitude': 40.07807}, {'longitude': 116.41991, 'latitude': 40.07808}, {'longitude': 116.42008, 'latitude': 40.07806}, {'longitude': 116.42025, 'latitude': 40.07806}, {'longitude': 116.42044, 'latitude': 40.07807}, {'longitude': 116.4206, 'latitude': 40.07806}, {'longitude': 116.42078, 'latitude': 40.07807}, {'longitude': 116.42096, 'latitude': 40.07807}, {'longitude': 116.42116, 'latitude': 40.07807}, {'longitude': 116.42134, 'latitude': 40.07806}, {'longitude': 116.42152, 'latitude': 40.07807}, {'longitude': 116.42171, 'latitude': 40.07806}, {'longitude': 116.42188, 'latitude': 40.07806}, {'longitude': 116.42205, 'latitude': 40.07805}, {'longitude': 116.4222, 'latitude': 40.07797}, {'longitude': 116.42219, 'latitude': 40.07782}, {'longitude': 116.42219, 'latitude': 40.07766}, {'longitude': 116.42219, 'latitude': 40.07753}, {'longitude': 116.4222, 'latitude': 40.07739}, {'longitude': 116.42222, 'latitude': 40.07725}, {'longitude': 116.42219, 'latitude': 40.07711}, {'longitude': 116.4222, 'latitude': 40.07697}, {'longitude': 116.42221, 'latitude': 40.07684}, {'longitude': 116.4222, 'latitude': 40.0767}, {'longitude': 116.42221, 'latitude': 40.07657}, {'longitude': 116.4222, 'latitude': 40.07643}, {'longitude': 116.4222, 'latitude': 40.0763}, {'longitude': 116.42221, 'latitude': 40.07616}, {'longitude': 116.4222, 'latitude': 40.07602}, {'longitude': 116.42222, 'latitude': 40.07589}, {'longitude': 116.42222, 'latitude': 40.07575}, {'longitude': 116.42222, 'latitude': 40.07562}, {'longitude': 116.42226, 'latitude': 40.0755}, {'longitude': 116.42221, 'latitude': 40.07539}, {'longitude': 116.42217, 'latitude': 40.07525}, {'longitude': 116.42217, 'latitude': 40.07513}, {'longitude': 116.42217, 'latitude': 40.07501}, {'longitude': 116.42219, 'latitude': 40.0749}, {'longitude': 116.42218, 'latitude': 40.07476}, {'longitude': 116.4222, 'latitude': 40.07464}, {'longitude': 116.4222, 'latitude': 40.07452}, {'longitude': 116.4222, 'latitude': 40.07438}, {'longitude': 116.4222, 'latitude': 40.07425}, {'longitude': 116.42224, 'latitude': 40.07414}, {'longitude': 116.42224, 'latitude': 40.07401}, {'longitude': 116.42223, 'latitude': 40.07389}, {'longitude': 116.42221, 'latitude': 40.07376}, {'longitude': 116.42223, 'latitude': 40.07363}, {'longitude': 116.42221, 'latitude': 40.0735}, {'longitude': 116.4222, 'latitude': 40.07338}, {'longitude': 116.42222, 'latitude': 40.07324}, {'longitude': 116.42221, 'latitude': 40.07312}, {'longitude': 116.42221, 'latitude': 40.07299}, {'longitude': 116.42217, 'latitude': 40.07289}, {'longitude': 116.42201, 'latitude': 40.07292}, {'longitude': 116.42185, 'latitude': 40.07293}, {'longitude': 116.42168, 'latitude': 40.07292}, {'longitude': 116.42152, 'latitude': 40.07293}, {'longitude': 116.42137, 'latitude': 40.07292}, {'longitude': 116.42122, 'latitude': 40.07292}, {'longitude': 116.42105, 'latitude': 40.07292}, {'longitude': 116.4209, 'latitude': 40.07293}, {'longitude': 116.42073, 'latitude': 40.07292}, {'longitude': 116.42056, 'latitude': 40.07291}, {'longitude': 116.4204, 'latitude': 40.07291}, {'longitude': 116.42024, 'latitude': 40.07292}, {'longitude': 116.42009, 'latitude': 40.07292}, {'longitude': 116.41992, 'latitude': 40.07293}, {'longitude': 116.41975, 'latitude': 40.07292}, {'longitude': 116.41958, 'latitude': 40.07292}, {'longitude': 116.4194, 'latitude': 40.07291}, {'longitude': 116.41923, 'latitude': 40.07291}, {'longitude': 116.41907, 'latitude': 40.0729}, {'longitude': 116.41891, 'latitude': 40.0729}, {'longitude': 116.41892, 'latitude': 40.07303}, {'longitude': 116.4189, 'latitude': 40.07315}, {'longitude': 116.41891, 'latitude': 40.07327}]
    elif track_id == '2':
        data = [{'longitude': 120.68747, 'latitude': 36.36037}, {'longitude': 120.68758, 'latitude': 36.36024}, {'longitude': 120.68769, 'latitude': 36.36017}, {'longitude': 120.68833, 'latitude': 36.36037}, {'longitude': 120.68838, 'latitude': 36.36057}, {'longitude': 120.68839, 'latitude': 36.36068}, {'longitude': 120.6884, 'latitude': 36.36084}, {'longitude': 120.6884, 'latitude': 36.36091}, {'longitude': 120.68841, 'latitude': 36.36099}, {'longitude': 120.68841, 'latitude': 36.36118}, {'longitude': 120.68828, 'latitude': 36.36147}, {'longitude': 120.68798, 'latitude': 36.3616}, {'longitude': 120.68786, 'latitude': 36.36161}, {'longitude': 120.68756, 'latitude': 36.36148}, {'longitude': 120.68749, 'latitude': 36.36137}, {'longitude': 120.68745, 'latitude': 36.36118}, {'longitude': 120.68746, 'latitude': 36.3611}, {'longitude': 120.68745, 'latitude': 36.3609}, {'longitude': 120.68742, 'latitude': 36.36069}, {'longitude': 120.6874, 'latitude': 36.3606}, {'longitude': 120.68738, 'latitude': 36.36041}, {'longitude': 120.68746, 'latitude': 36.36021}, {'longitude': 120.68796, 'latitude': 36.36008}, {'longitude': 120.68833, 'latitude': 36.36039}, {'longitude': 120.68835, 'latitude': 36.3606}, {'longitude': 120.68835, 'latitude': 36.36068}, {'longitude': 120.68835, 'latitude': 36.36087}, {'longitude': 120.68835, 'latitude': 36.36095}, {'longitude': 120.68836, 'latitude': 36.36115}, {'longitude': 120.68837, 'latitude': 36.36122}, {'longitude': 120.68782, 'latitude': 36.36157}, {'longitude': 120.68743, 'latitude': 36.36119}, {'longitude': 120.68743, 'latitude': 36.3611}, {'longitude': 120.68743, 'latitude': 36.36093}, {'longitude': 120.68742, 'latitude': 36.36086}, {'longitude': 120.68741, 'latitude': 36.36068}, {'longitude': 120.6874, 'latitude': 36.36058}, {'longitude': 120.6874, 'latitude': 36.3605}, {'longitude': 120.68834, 'latitude': 36.36041}, {'longitude': 120.68838, 'latitude': 36.36058}, {'longitude': 120.68839, 'latitude': 36.36066}, {'longitude': 120.6884, 'latitude': 36.36099}, {'longitude': 120.68841, 'latitude': 36.3611}, {'longitude': 120.6878, 'latitude': 36.3616}, {'longitude': 120.68745, 'latitude': 36.36117}, {'longitude': 120.68745, 'latitude': 36.36108}, {'longitude': 120.68746, 'latitude': 36.36088}, {'longitude': 120.68743, 'latitude': 36.36071}, {'longitude': 120.68743, 'latitude': 36.36051}, {'longitude': 120.68744, 'latitude': 36.3604}, {'longitude': 120.68803, 'latitude': 36.3601}, {'longitude': 120.68839, 'latitude': 36.36048}, {'longitude': 120.68838, 'latitude': 36.3606}, {'longitude': 120.68837, 'latitude': 36.36093}, {'longitude': 120.68837, 'latitude': 36.36105}, {'longitude': 120.68745, 'latitude': 36.3611}, {'longitude': 120.68746, 'latitude': 36.36098}, {'longitude': 120.68746, 'latitude': 36.36078}, {'longitude': 120.68747, 'latitude': 36.36069}, {'longitude': 120.68746, 'latitude': 36.36048}, {'longitude': 120.68816, 'latitude': 36.36017}, {'longitude': 120.68839, 'latitude': 36.36053}, {'longitude': 120.68838, 'latitude': 36.36062}, {'longitude': 120.68839, 'latitude': 36.36088}, {'longitude': 120.68841, 'latitude': 36.36101}, {'longitude': 120.68842, 'latitude': 36.36123}, {'longitude': 120.68799, 'latitude': 36.36165}, {'longitude': 120.68741, 'latitude': 36.3613}, {'longitude': 120.68739, 'latitude': 36.3612}, {'longitude': 120.68738, 'latitude': 36.36098}, {'longitude': 120.68739, 'latitude': 36.36087}, {'longitude': 120.68739, 'latitude': 36.36067}, {'longitude': 120.6874, 'latitude': 36.36056}, {'longitude': 120.68744, 'latitude': 36.36039}, {'longitude': 120.6884, 'latitude': 36.36031}, {'longitude': 120.68846, 'latitude': 36.36054}, {'longitude': 120.68845, 'latitude': 36.36076}, {'longitude': 120.68844, 'latitude': 36.36099}, {'longitude': 120.68844, 'latitude': 36.36108}, {'longitude': 120.68741, 'latitude': 36.36125}, {'longitude': 120.68743, 'latitude': 36.36099}, {'longitude': 120.68741, 'latitude': 36.36078}, {'longitude': 120.68741, 'latitude': 36.36066}, {'longitude': 120.68741, 'latitude': 36.36046}, {'longitude': 120.68842, 'latitude': 36.3606}, {'longitude': 120.68843, 'latitude': 36.36073}, {'longitude': 120.68843, 'latitude': 36.36095}, {'longitude': 120.68843, 'latitude': 36.36107}, {'longitude': 120.68779, 'latitude': 36.36163}, {'longitude': 120.68741, 'latitude': 36.36128}, {'longitude': 120.68741, 'latitude': 36.3612}, {'longitude': 120.68742, 'latitude': 36.36112}, {'longitude': 120.68742, 'latitude': 36.36095}, {'longitude': 120.68743, 'latitude': 36.36085}, {'longitude': 120.68742, 'latitude': 36.36062}, {'longitude': 120.68741, 'latitude': 36.36054}, {'longitude': 120.68783, 'latitude': 36.36007}, {'longitude': 120.68847, 'latitude': 36.36051}, {'longitude': 120.68846, 'latitude': 36.36062}, {'longitude': 120.68844, 'latitude': 36.36079}, {'longitude': 120.68844, 'latitude': 36.36088}, {'longitude': 120.68845, 'latitude': 36.36112}, {'longitude': 120.68845, 'latitude': 36.36121}, {'longitude': 120.68801, 'latitude': 36.36166}, {'longitude': 120.68777, 'latitude': 36.36164}, {'longitude': 120.68748, 'latitude': 36.36148}, {'longitude': 120.68736, 'latitude': 36.36118}, {'longitude': 120.68741, 'latitude': 36.36084}, {'longitude': 120.6874, 'latitude': 36.36072}, {'longitude': 120.68737, 'latitude': 36.36051}, {'longitude': 120.68846, 'latitude': 36.36032}, {'longitude': 120.6885, 'latitude': 36.36054}, {'longitude': 120.68849, 'latitude': 36.36066}, {'longitude': 120.68848, 'latitude': 36.3609}, {'longitude': 120.68848, 'latitude': 36.36098}, {'longitude': 120.68847, 'latitude': 36.36119}, {'longitude': 120.68838, 'latitude': 36.36148}, {'longitude': 120.68791, 'latitude': 36.36167}, {'longitude': 120.68773, 'latitude': 36.36165}, {'longitude': 120.68743, 'latitude': 36.36141}, {'longitude': 120.68739, 'latitude': 36.36123}, {'longitude': 120.6874, 'latitude': 36.36115}, {'longitude': 120.6874, 'latitude': 36.36105}, {'longitude': 120.68741, 'latitude': 36.36089}, {'longitude': 120.6874, 'latitude': 36.36079}, {'longitude': 120.68739, 'latitude': 36.36055}, {'longitude': 120.68738, 'latitude': 36.36044}, {'longitude': 120.68808, 'latitude': 36.36008}, {'longitude': 120.68844, 'latitude': 36.36039}, {'longitude': 120.68847, 'latitude': 36.36075}, {'longitude': 120.68848, 'latitude': 36.36088}, {'longitude': 120.68848, 'latitude': 36.36135}, {'longitude': 120.68838, 'latitude': 36.36151}, {'longitude': 120.68829, 'latitude': 36.36157}, {'longitude': 120.6875, 'latitude': 36.36152}, {'longitude': 120.6874, 'latitude': 36.36119}, {'longitude': 120.6874, 'latitude': 36.36108}, {'longitude': 120.68738, 'latitude': 36.36087}, {'longitude': 120.68737, 'latitude': 36.36076}, {'longitude': 120.68738, 'latitude': 36.36059}, {'longitude': 120.68739, 'latitude': 36.36048}, {'longitude': 120.68743, 'latitude': 36.36031}, {'longitude': 120.68839, 'latitude': 36.3603}, {'longitude': 120.68847, 'latitude': 36.3606}, {'longitude': 120.68848, 'latitude': 36.36074}, {'longitude': 120.68847, 'latitude': 36.36099}, {'longitude': 120.68846, 'latitude': 36.3611}, {'longitude': 120.68846, 'latitude': 36.36135}, {'longitude': 120.68792, 'latitude': 36.36168}, {'longitude': 120.6874, 'latitude': 36.36108}, {'longitude': 120.68739, 'latitude': 36.36098}, {'longitude': 120.68739, 'latitude': 36.36076}, {'longitude': 120.68739, 'latitude': 36.36063}, {'longitude': 120.68814, 'latitude': 36.36009}, {'longitude': 120.68821, 'latitude': 36.36012}, {'longitude': 120.68837, 'latitude': 36.36024}, {'longitude': 120.68846, 'latitude': 36.36037}, {'longitude': 120.68847, 'latitude': 36.36052}, {'longitude': 120.68846, 'latitude': 36.36055}, {'longitude': 120.68845, 'latitude': 36.36058}, {'longitude': 120.68845, 'latitude': 36.36061}, {'longitude': 120.68845, 'latitude': 36.36065}, {'longitude': 120.68845, 'latitude': 36.36071}, {'longitude': 120.68845, 'latitude': 36.36074}, {'longitude': 120.68845, 'latitude': 36.36083}, {'longitude': 120.68846, 'latitude': 36.36088}, {'longitude': 120.68846, 'latitude': 36.36093}, {'longitude': 120.68846, 'latitude': 36.36101}, {'longitude': 120.68845, 'latitude': 36.36107}, {'longitude': 120.68845, 'latitude': 36.3611}, {'longitude': 120.68845, 'latitude': 36.36115}, {'longitude': 120.68845, 'latitude': 36.36118}, {'longitude': 120.68844, 'latitude': 36.36123}, {'longitude': 120.68843, 'latitude': 36.36127}, {'longitude': 120.68843, 'latitude': 36.36136}, {'longitude': 120.6884, 'latitude': 36.36142}, {'longitude': 120.68836, 'latitude': 36.3615}, {'longitude': 120.68833, 'latitude': 36.36154}, {'longitude': 120.68825, 'latitude': 36.36159}, {'longitude': 120.68822, 'latitude': 36.3616}, {'longitude': 120.68817, 'latitude': 36.36162}, {'longitude': 120.68814, 'latitude': 36.36163}, {'longitude': 120.68809, 'latitude': 36.36165}, {'longitude': 120.68798, 'latitude': 36.36166}, {'longitude': 120.68791, 'latitude': 36.36166}, {'longitude': 120.68785, 'latitude': 36.36167}, {'longitude': 120.6878, 'latitude': 36.36167}, {'longitude': 120.68772, 'latitude': 36.36166}, {'longitude': 120.68764, 'latitude': 36.36164}, {'longitude': 120.6876, 'latitude': 36.36162}, {'longitude': 120.68755, 'latitude': 36.3616}, {'longitude': 120.68749, 'latitude': 36.36154}, {'longitude': 120.68747, 'latitude': 36.36145}, {'longitude': 120.68746, 'latitude': 36.3614}, {'longitude': 120.68745, 'latitude': 36.36137}, {'longitude': 120.68745, 'latitude': 36.36132}]
    else :
        data = [{'longitude': 116.36376, 'latitude': 40.03471}, {'longitude': 116.36343, 'latitude': 40.03469}, {'longitude': 116.3633, 'latitude': 40.03468}, {'longitude': 116.36294, 'latitude': 40.03452}, {'longitude': 116.36281, 'latitude': 40.0345}, {'longitude': 116.36256, 'latitude': 40.03442}, {'longitude': 116.36207, 'latitude': 40.03429}, {'longitude': 116.36192, 'latitude': 40.03427}, {'longitude': 116.36154, 'latitude': 40.03406}, {'longitude': 116.36157, 'latitude': 40.03379}, {'longitude': 116.3616, 'latitude': 40.03367}, {'longitude': 116.36174, 'latitude': 40.03331}, {'longitude': 116.36183, 'latitude': 40.03308}, {'longitude': 116.36251, 'latitude': 40.03236}, {'longitude': 116.36265, 'latitude': 40.03241}, {'longitude': 116.36354, 'latitude': 40.03302}, {'longitude': 116.36347, 'latitude': 40.03311}, {'longitude': 116.36305, 'latitude': 40.0341}, {'longitude': 116.36295, 'latitude': 40.03437}, {'longitude': 116.36286, 'latitude': 40.03446}, {'longitude': 116.36138, 'latitude': 40.03384}, {'longitude': 116.36158, 'latitude': 40.0335}, {'longitude': 116.36176, 'latitude': 40.03324}, {'longitude': 116.36182, 'latitude': 40.03313}, {'longitude': 116.36198, 'latitude': 40.03283}, {'longitude': 116.36204, 'latitude': 40.03273}, {'longitude': 116.36248, 'latitude': 40.03232}, {'longitude': 116.36264, 'latitude': 40.03236}, {'longitude': 116.36339, 'latitude': 40.03266}, {'longitude': 116.36362, 'latitude': 40.03294}, {'longitude': 116.36355, 'latitude': 40.03301}, {'longitude': 116.36306, 'latitude': 40.03395}, {'longitude': 116.36306, 'latitude': 40.03401}, {'longitude': 116.36305, 'latitude': 40.03414}, {'longitude': 116.36304, 'latitude': 40.03423}, {'longitude': 116.36251, 'latitude': 40.0345}, {'longitude': 116.36145, 'latitude': 40.03432}, {'longitude': 116.36148, 'latitude': 40.03379}, {'longitude': 116.36153, 'latitude': 40.03369}, {'longitude': 116.36195, 'latitude': 40.03286}, {'longitude': 116.362, 'latitude': 40.03278}, {'longitude': 116.36246, 'latitude': 40.03239}, {'longitude': 116.36259, 'latitude': 40.03243}, {'longitude': 116.36325, 'latitude': 40.03261}, {'longitude': 116.36337, 'latitude': 40.03264}, {'longitude': 116.36363, 'latitude': 40.0329}, {'longitude': 116.36357, 'latitude': 40.033}, {'longitude': 116.36233, 'latitude': 40.03458}, {'longitude': 116.36155, 'latitude': 40.03439}, {'longitude': 116.36262, 'latitude': 40.03237}, {'longitude': 116.36276, 'latitude': 40.0324}, {'longitude': 116.36301, 'latitude': 40.03246}, {'longitude': 116.36309, 'latitude': 40.03249}, {'longitude': 116.36319, 'latitude': 40.03251}, {'longitude': 116.36367, 'latitude': 40.03289}, {'longitude': 116.36305, 'latitude': 40.034}, {'longitude': 116.36306, 'latitude': 40.0342}, {'longitude': 116.36205, 'latitude': 40.03442}, {'longitude': 116.36154, 'latitude': 40.03369}, {'longitude': 116.36178, 'latitude': 40.03318}, {'longitude': 116.36198, 'latitude': 40.03278}, {'longitude': 116.36245, 'latitude': 40.03232}, {'longitude': 116.36349, 'latitude': 40.03265}, {'longitude': 116.36357, 'latitude': 40.03296}, {'longitude': 116.36291, 'latitude': 40.03452}, {'longitude': 116.36251, 'latitude': 40.03449}, {'longitude': 116.3621, 'latitude': 40.03446}, {'longitude': 116.3616, 'latitude': 40.03369}, {'longitude': 116.36166, 'latitude': 40.03357}, {'longitude': 116.36206, 'latitude': 40.03268}, {'longitude': 116.36214, 'latitude': 40.03258}, {'longitude': 116.36248, 'latitude': 40.03234}, {'longitude': 116.36361, 'latitude': 40.03295}, {'longitude': 116.36344, 'latitude': 40.03319}, {'longitude': 116.36341, 'latitude': 40.03327}, {'longitude': 116.36232, 'latitude': 40.03456}, {'longitude': 116.36217, 'latitude': 40.0345}, {'longitude': 116.3618, 'latitude': 40.03426}, {'longitude': 116.36151, 'latitude': 40.03403}, {'longitude': 116.36155, 'latitude': 40.03376}, {'longitude': 116.362, 'latitude': 40.03286}, {'longitude': 116.36218, 'latitude': 40.03251}, {'longitude': 116.36323, 'latitude': 40.0326}, {'longitude': 116.36357, 'latitude': 40.03298}, {'longitude': 116.36351, 'latitude': 40.0331}]

    print(jsonify(data))
    return jsonify(data)


@app.route('/get_track1', methods=['POST'])
def get_track1():
    #从前端获取请求参数
    print(request.form.to_dict())
    track_id = request.form.get('track_id')
    print(track_id, type(track_id))

    db = get_db()
    data = pd.read_sql_query("select * from activities", db)
    data["run_id"] = data["run_id"].astype("str")
    print(data[:3])
    tmp = data[data["run_id"] == track_id]
    print(tmp)
    print(tmp["summary_polyline"], type(tmp["summary_polyline"].to_list()[0]))

    tmp_data = polyline.decode(tmp["summary_polyline"].to_list()[0])

    res_data = []
    for latlng in tmp_data:
        res_data.append({"longitude": latlng[1], "latitude": latlng[0]})
    print(res_data)
    return jsonify(res_data)


if __name__ == '__main__':
    # print(g.table_data)
    app.run(debug=True)
