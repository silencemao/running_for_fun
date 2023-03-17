import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder='template')
CORS(app)

key = 'your_amap_key'


# 定义路由
@app.route('/')
def index():
    return render_template('index.html')


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
    track_id = request.form.get('track_id')

    #发送GET请求获取轨迹数据
    res = requests.get('http://example.com/track', params={'track_id': track_id})
    # data = res.json()

    data = [{'longitude': 116.4192, 'latitude': 40.0762}, {'longitude': 116.41921, 'latitude': 40.07618}, {'longitude': 116.41926, 'latitude': 40.07618}, {'longitude': 116.41937, 'latitude': 40.07617}, {'longitude': 116.4195, 'latitude': 40.07618}, {'longitude': 116.4194, 'latitude': 40.07618}, {'longitude': 116.41962, 'latitude': 40.07609}, {'longitude': 116.41961, 'latitude': 40.07597}, {'longitude': 116.41959, 'latitude': 40.07585}, {'longitude': 116.41952, 'latitude': 40.07574}, {'longitude': 116.41944, 'latitude': 40.07564}, {'longitude': 116.41936, 'latitude': 40.07553}, {'longitude': 116.41933, 'latitude': 40.07541}, {'longitude': 116.41922, 'latitude': 40.07531}, {'longitude': 116.41908, 'latitude': 40.07523}, {'longitude': 116.41895, 'latitude': 40.07515}, {'longitude': 116.41885, 'latitude': 40.07506}, {'longitude': 116.41874, 'latitude': 40.07502}, {'longitude': 116.41872, 'latitude': 40.0749}, {'longitude': 116.4187, 'latitude': 40.07477}, {'longitude': 116.41873, 'latitude': 40.07464}, {'longitude': 116.41874, 'latitude': 40.07451}, {'longitude': 116.41871, 'latitude': 40.07439}, {'longitude': 116.41872, 'latitude': 40.07426}, {'longitude': 116.41872, 'latitude': 40.07415}, {'longitude': 116.41878, 'latitude': 40.07413}, {'longitude': 116.41882, 'latitude': 40.07406}, {'longitude': 116.41882, 'latitude': 40.07393}, {'longitude': 116.41883, 'latitude': 40.07375}, {'longitude': 116.41884, 'latitude': 40.07359}, {'longitude': 116.41878, 'latitude': 40.07346}, {'longitude': 116.41876, 'latitude': 40.07332}, {'longitude': 116.41876, 'latitude': 40.07319}, {'longitude': 116.41877, 'latitude': 40.07305}, {'longitude': 116.41873, 'latitude': 40.07292}, {'longitude': 116.41855, 'latitude': 40.07292}, {'longitude': 116.41837, 'latitude': 40.07293}, {'longitude': 116.4182, 'latitude': 40.07292}, {'longitude': 116.41804, 'latitude': 40.07294}, {'longitude': 116.41785, 'latitude': 40.07293}, {'longitude': 116.41768, 'latitude': 40.07294}, {'longitude': 116.41751, 'latitude': 40.07294}, {'longitude': 116.41732, 'latitude': 40.07294}, {'longitude': 116.41714, 'latitude': 40.07294}, {'longitude': 116.41698, 'latitude': 40.07293}, {'longitude': 116.41681, 'latitude': 40.07293}, {'longitude': 116.41665, 'latitude': 40.07293}, {'longitude': 116.41647, 'latitude': 40.07292}, {'longitude': 116.41632, 'latitude': 40.07291}, {'longitude': 116.41617, 'latitude': 40.07292}, {'longitude': 116.41601, 'latitude': 40.07292}, {'longitude': 116.41588, 'latitude': 40.07293}, {'longitude': 116.41572, 'latitude': 40.07293}, {'longitude': 116.41557, 'latitude': 40.07293}, {'longitude': 116.41543, 'latitude': 40.07293}, {'longitude': 116.41533, 'latitude': 40.07301}, {'longitude': 116.41532, 'latitude': 40.07313}, {'longitude': 116.41534, 'latitude': 40.07324}, {'longitude': 116.41533, 'latitude': 40.07335}, {'longitude': 116.41531, 'latitude': 40.07347}, {'longitude': 116.41528, 'latitude': 40.07359}, {'longitude': 116.4153, 'latitude': 40.07371}, {'longitude': 116.41528, 'latitude': 40.07384}, {'longitude': 116.41528, 'latitude': 40.07395}, {'longitude': 116.41529, 'latitude': 40.0741}, {'longitude': 116.41528, 'latitude': 40.07423}, {'longitude': 116.41528, 'latitude': 40.07434}, {'longitude': 116.41528, 'latitude': 40.07446}, {'longitude': 116.41529, 'latitude': 40.07458}, {'longitude': 116.4153, 'latitude': 40.07468}, {'longitude': 116.41534, 'latitude': 40.07475}, {'longitude': 116.41528, 'latitude': 40.07487}, {'longitude': 116.41529, 'latitude': 40.075}, {'longitude': 116.41528, 'latitude': 40.07512}, {'longitude': 116.41529, 'latitude': 40.07525}, {'longitude': 116.41528, 'latitude': 40.07537}, {'longitude': 116.41527, 'latitude': 40.07549}, {'longitude': 116.41528, 'latitude': 40.07561}, {'longitude': 116.41529, 'latitude': 40.07573}, {'longitude': 116.41528, 'latitude': 40.07585}, {'longitude': 116.41528, 'latitude': 40.07597}, {'longitude': 116.41529, 'latitude': 40.07611}, {'longitude': 116.41528, 'latitude': 40.07624}, {'longitude': 116.41529, 'latitude': 40.07637}, {'longitude': 116.41529, 'latitude': 40.07651}, {'longitude': 116.41529, 'latitude': 40.07664}, {'longitude': 116.41528, 'latitude': 40.07676}, {'longitude': 116.41527, 'latitude': 40.07688}, {'longitude': 116.41528, 'latitude': 40.07701}, {'longitude': 116.41528, 'latitude': 40.07715}, {'longitude': 116.41528, 'latitude': 40.07727}, {'longitude': 116.41528, 'latitude': 40.07741}, {'longitude': 116.4153, 'latitude': 40.07753}, {'longitude': 116.41528, 'latitude': 40.07767}, {'longitude': 116.41529, 'latitude': 40.0778}, {'longitude': 116.41531, 'latitude': 40.07793}, {'longitude': 116.41537, 'latitude': 40.07806}, {'longitude': 116.41553, 'latitude': 40.07807}, {'longitude': 116.41571, 'latitude': 40.07807}, {'longitude': 116.41589, 'latitude': 40.07809}, {'longitude': 116.41605, 'latitude': 40.07809}, {'longitude': 116.41621, 'latitude': 40.07809}, {'longitude': 116.41636, 'latitude': 40.07809}, {'longitude': 116.41653, 'latitude': 40.07809}, {'longitude': 116.4167, 'latitude': 40.0781}, {'longitude': 116.41685, 'latitude': 40.07809}, {'longitude': 116.41701, 'latitude': 40.07806}, {'longitude': 116.41719, 'latitude': 40.07806}, {'longitude': 116.41737, 'latitude': 40.07805}, {'longitude': 116.41756, 'latitude': 40.07811}, {'longitude': 116.41768, 'latitude': 40.07816}, {'longitude': 116.41783, 'latitude': 40.07809}, {'longitude': 116.41799, 'latitude': 40.07809}, {'longitude': 116.41817, 'latitude': 40.07811}, {'longitude': 116.41833, 'latitude': 40.07808}, {'longitude': 116.41849, 'latitude': 40.07809}, {'longitude': 116.41865, 'latitude': 40.07808}, {'longitude': 116.41882, 'latitude': 40.07807}, {'longitude': 116.41901, 'latitude': 40.07808}, {'longitude': 116.4192, 'latitude': 40.07807}, {'longitude': 116.41938, 'latitude': 40.07807}, {'longitude': 116.41956, 'latitude': 40.07807}, {'longitude': 116.41974, 'latitude': 40.07807}, {'longitude': 116.41991, 'latitude': 40.07808}, {'longitude': 116.42008, 'latitude': 40.07806}, {'longitude': 116.42025, 'latitude': 40.07806}, {'longitude': 116.42044, 'latitude': 40.07807}, {'longitude': 116.4206, 'latitude': 40.07806}, {'longitude': 116.42078, 'latitude': 40.07807}, {'longitude': 116.42096, 'latitude': 40.07807}, {'longitude': 116.42116, 'latitude': 40.07807}, {'longitude': 116.42134, 'latitude': 40.07806}, {'longitude': 116.42152, 'latitude': 40.07807}, {'longitude': 116.42171, 'latitude': 40.07806}, {'longitude': 116.42188, 'latitude': 40.07806}, {'longitude': 116.42205, 'latitude': 40.07805}, {'longitude': 116.4222, 'latitude': 40.07797}, {'longitude': 116.42219, 'latitude': 40.07782}, {'longitude': 116.42219, 'latitude': 40.07766}, {'longitude': 116.42219, 'latitude': 40.07753}, {'longitude': 116.4222, 'latitude': 40.07739}, {'longitude': 116.42222, 'latitude': 40.07725}, {'longitude': 116.42219, 'latitude': 40.07711}, {'longitude': 116.4222, 'latitude': 40.07697}, {'longitude': 116.42221, 'latitude': 40.07684}, {'longitude': 116.4222, 'latitude': 40.0767}, {'longitude': 116.42221, 'latitude': 40.07657}, {'longitude': 116.4222, 'latitude': 40.07643}, {'longitude': 116.4222, 'latitude': 40.0763}, {'longitude': 116.42221, 'latitude': 40.07616}, {'longitude': 116.4222, 'latitude': 40.07602}, {'longitude': 116.42222, 'latitude': 40.07589}, {'longitude': 116.42222, 'latitude': 40.07575}, {'longitude': 116.42222, 'latitude': 40.07562}, {'longitude': 116.42226, 'latitude': 40.0755}, {'longitude': 116.42221, 'latitude': 40.07539}, {'longitude': 116.42217, 'latitude': 40.07525}, {'longitude': 116.42217, 'latitude': 40.07513}, {'longitude': 116.42217, 'latitude': 40.07501}, {'longitude': 116.42219, 'latitude': 40.0749}, {'longitude': 116.42218, 'latitude': 40.07476}, {'longitude': 116.4222, 'latitude': 40.07464}, {'longitude': 116.4222, 'latitude': 40.07452}, {'longitude': 116.4222, 'latitude': 40.07438}, {'longitude': 116.4222, 'latitude': 40.07425}, {'longitude': 116.42224, 'latitude': 40.07414}, {'longitude': 116.42224, 'latitude': 40.07401}, {'longitude': 116.42223, 'latitude': 40.07389}, {'longitude': 116.42221, 'latitude': 40.07376}, {'longitude': 116.42223, 'latitude': 40.07363}, {'longitude': 116.42221, 'latitude': 40.0735}, {'longitude': 116.4222, 'latitude': 40.07338}, {'longitude': 116.42222, 'latitude': 40.07324}, {'longitude': 116.42221, 'latitude': 40.07312}, {'longitude': 116.42221, 'latitude': 40.07299}, {'longitude': 116.42217, 'latitude': 40.07289}, {'longitude': 116.42201, 'latitude': 40.07292}, {'longitude': 116.42185, 'latitude': 40.07293}, {'longitude': 116.42168, 'latitude': 40.07292}, {'longitude': 116.42152, 'latitude': 40.07293}, {'longitude': 116.42137, 'latitude': 40.07292}, {'longitude': 116.42122, 'latitude': 40.07292}, {'longitude': 116.42105, 'latitude': 40.07292}, {'longitude': 116.4209, 'latitude': 40.07293}, {'longitude': 116.42073, 'latitude': 40.07292}, {'longitude': 116.42056, 'latitude': 40.07291}, {'longitude': 116.4204, 'latitude': 40.07291}, {'longitude': 116.42024, 'latitude': 40.07292}, {'longitude': 116.42009, 'latitude': 40.07292}, {'longitude': 116.41992, 'latitude': 40.07293}, {'longitude': 116.41975, 'latitude': 40.07292}, {'longitude': 116.41958, 'latitude': 40.07292}, {'longitude': 116.4194, 'latitude': 40.07291}, {'longitude': 116.41923, 'latitude': 40.07291}, {'longitude': 116.41907, 'latitude': 40.0729}, {'longitude': 116.41891, 'latitude': 40.0729}, {'longitude': 116.41892, 'latitude': 40.07303}, {'longitude': 116.4189, 'latitude': 40.07315}, {'longitude': 116.41891, 'latitude': 40.07327}]

    print(jsonify(data))
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
