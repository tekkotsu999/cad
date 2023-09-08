from flask import render_template
from . import app  # __init__.pyからFlaskアプリケーションインスタンスをインポート
import math

from flask import jsonify, request
# from .src.optimize import run_optimization

from .src.shapes import ShapeManager,Point,Line


shape_manager = ShapeManager()


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
                'coordinates' : { 'x': shape.x, 'y': shape.y},
                'is_selected' : shape.is_selected
            })
        elif isinstance(shape, Line):
            shapes_data.append({
                'shape_type': 'Line',
                'coordinates': {
                    'p1': {'x': shape.p1.x, 'y': shape.p1.y},
                    'p2': {'x': shape.p2.x, 'y': shape.p2.y}},
                'is_selected' : shape.is_selected
            })
    # print("Shapes data:", shapes_data)
    return jsonify(shapes_data)

# ---------------------------------------------------------------
@app.route('/select_point', methods=['POST'])
def select_point():
    data = request.json
    click_x = data['coordinates']['x']  # 座標のx値
    click_y = data['coordinates']['y']  # 座標のy値
    tolerance = data['tolerance']  # 許容値

    for point in shape_manager.get_shapes():
        if isinstance(point, Point):
            # 2点間の距離を計算
            distance = math.sqrt((point.x - click_x)**2 + (point.y - click_y)**2)
            if distance <= tolerance:  # 許容値以内
                point.is_selected = True
                return jsonify({'status': 'success', 'selected_point': point.__dict__})
    
    return jsonify({'status': 'no_point_selected'})

