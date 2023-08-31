from flask import render_template
from . import app  # __init__.pyからFlaskアプリケーションインスタンスをインポート

from flask import jsonify, request
# from .src.optimize import run_optimization

from .src.shapes import ShapeManager,Point,Line

# ---------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------------------------------------------------------
@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.get_json()
    
    # run_optimization関数を呼び出して最適化問題を解く
    # result = run_optimization(data)

    # 結果をJSON形式で返す
    return jsonify(result)

# ---------------------------------------------------------------

shape_manager = ShapeManager()

@app.route('/add_shape', methods=['POST'])
def add_shape():
    data = request.json
    shape_type = data['shape_type']
    coordinates = data['coordinates']

    shape_manager.add_shape(shape_type, coordinates)

    # フロントエンドに送り返すデータ
    # ※このデータはフロントエンドでは使用していない（今のところ）
    response_data = {
        'shape': shape_type,
        'coordinates': coordinates
    }
    return jsonify(response_data)

# ---------------------------------------------------------------
# 全ての図形を取得するためのルート
@app.route('/get_shapes', methods=['GET'])
def get_shapes():
    shapes_data = []
    for shape in shape_manager.shapes:
        if isinstance(shape, Point):
            shapes_data.append({
                'shape_type': 'Point',
                'coordinates' : { 'x': shape.x, 'y': shape.y}
            })
        elif isinstance(shape, Line):
            shapes_data.append({
                'shape_type': 'Line',
                'coordinates': {
                    'p1': {'x': shape.p1.x, 'y': shape.p1.y},
                    'p2': {'x': shape.p2.x, 'y': shape.p2.y}}
            })
    # print("Shapes data:", shapes_data)
    return jsonify(shapes_data)