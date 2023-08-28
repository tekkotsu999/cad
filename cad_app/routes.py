from flask import render_template
from . import app  # __init__.pyからFlaskアプリケーションインスタンスをインポート

from flask import jsonify, request
# from .src.optimize import run_optimization

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.get_json()
    
    # run_optimization関数を呼び出して最適化問題を解く
    # result = run_optimization(data)

    # 結果をJSON形式で返す
    return jsonify(result)


from .src.shapes import ShapeManager
shape_manager = ShapeManager()

@app.route('/add_shape', methods=['POST'])
def add_shape():
    data = request.json
    shape_type = data['shape']
    coordinates = data['coordinates']

    shape_manager.add_shape(shape_type, coordinates)

    # フロントエンドに送り返すデータ
    response_data = {
        'shape': shape_type,
        'coordinates': coordinates
    }
    return jsonify(response_data)


# 全ての図形を取得するためのルート
@app.route('/get_shapes', methods=['GET'])
def get_shapes():
    shapes_data = []
    for shape in shape_manager.get_shapes():
        shape_data = {
            'type': type(shape).__name__,
            'coordinates': {'x': shape.x, 'y': shape.y}  # 例: Pointクラスの場合
        }
        shapes_data.append(shape_data)

    # print(shapes_data)

    return jsonify({'shapes': shapes_data})