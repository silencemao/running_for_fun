from flask import Flask, render_template, jsonify

app = Flask(__name__)

# 模拟表格数据
table_data = [
    {'id': 1, 'name': 'John', 'age': 25},
    {'id': 2, 'name': 'Mary', 'age': 30},
    {'id': 3, 'name': 'Peter', 'age': 35},
]

# 模拟经纬度数据
locations = {
  1: [
    { "lng": -74.005974, "lat": 40.712776 },
    { "lng": -74.00473, "lat": 40.74287 },
    { "lng": -73.9851, "lat": 40.7587 }
  ],
  2: [
    {"lng": -74.005974, "lat": 40.712776},
    {"lng": -73.98488, "lat": 40.72813},
    {"lng": -73.986, "lat": 40.7397}
  ],
  3: [
    {"lng": -74.005974, "lat": 40.712776},
    {"lng": -73.99496, "lat": 40.75489},
    {"lng": -73.9867, "lat": 40.7559}
  ]
}

@app.route('/')
def index():
    return render_template('index.html', table_data=table_data)


@app.route('/locations/<int:id>')
def get_locations(id):
    print(id, type(id))
    print(locations[id])
    print(jsonify(locations[id]))

    return jsonify(locations[id])


if __name__ == '__main__':
    app.run(debug=True)
