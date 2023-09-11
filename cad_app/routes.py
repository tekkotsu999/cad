from flask import render_template
from . import app  # __init__.pyからFlaskアプリケーションインスタンスをインポート
import math

from flask import jsonify, request
# from .src.optimize import run_optimization

from .src.shapes import ShapeManager,Point,Line
from .src.constraints import *

shape_manager = ShapeManager()
constraint_manager = ConstraintManager()

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
    shapes_data = [shape.to_json() for shape in shape_manager.shapes]
    # print("Shapes data:", shapes_data)
    return jsonify(shapes_data)

# ---------------------------------------------------------------
@app.route('/select_shape', methods=['POST'])
def select_shape():
    data = request.json
    click_x = data['coordinates']['x']
    click_y = data['coordinates']['y']
    tolerance = data['tolerance']

    # 点の選択
    for shape in shape_manager.get_shapes():
        if isinstance(shape, Point):
            distance = math.sqrt((shape.x - click_x)**2 + (shape.y - click_y)**2)
            if distance <= tolerance:

                # 全てのshapeのis_selectedをリセット
                for shape_tmp in shape_manager.get_shapes():
                    shape_tmp.is_selected = False

                shape.is_selected = True
                return jsonify({'status': 'success', 'selected_shape': shape_to_dict(shape)})

    # 線の選択
    for shape in shape_manager.get_shapes():
        if isinstance(shape, Line):
            # 線とクリック位置との距離を計算（実装が必要）
            distance = calculate_line_distance(shape, click_x, click_y)
            if distance <= tolerance:

                # 全てのshapeのis_selectedをリセット
                for shape_tmp in shape_manager.get_shapes():
                    shape_tmp.is_selected = False

                shape.is_selected = True
                return jsonify({'status': 'success', 'selected_shape': shape_to_dict(shape)})

    return jsonify({'status': 'no_shape_selected'})

# 線の方程式と点との距離を計算
def calculate_line_distance(line, click_x, click_y):
    # 線分の両端の点
    x1, y1 = line.p1.x, line.p1.y
    x2, y2 = line.p2.x, line.p2.y
    
    # 線分のベクトル
    dx = x2 - x1
    dy = y2 - y1
    
    # 線分の長さの二乗
    l2 = dx*dx + dy*dy
    
    # 線分が点である（長さが0）場合
    if l2 == 0:
        return math.sqrt((click_x - x1)**2 + (click_y - y1)**2)
    
    # 線分上で最もクリック位置に近い点を求める
    t = ((click_x - x1) * dx + (click_y - y1) * dy) / l2
    
    # tを[0, 1]の範囲にクリッピング
    t = max(0, min(1, t))
    
    # 最も近い点の座標
    nearest_x = x1 + t * dx
    nearest_y = y1 + t * dy
    
    # 最も近い点とクリック位置との距離
    distance = math.sqrt((click_x - nearest_x)**2 + (click_y - nearest_y)**2)
    
    return distance

# shape_to_dict関数の実装
def shape_to_dict(shape):
    if isinstance(shape, Point):
        return {'type': 'Point', 'x': shape.x, 'y': shape.y, 'is_selected': shape.is_selected}
    elif isinstance(shape, Line):
        return {'type': 'Line', 'p1': shape.p1.__dict__, 'p2': shape.p2.__dict__, 'is_selected': shape.is_selected}

# ---------------------------------------------------------------
# "Apply FixedPointConstraint" ボタンがクリックされたときの処理
@app.route('/apply_fixed_point_constraint', methods=['POST'])
def apply_fixed_point_constraint():
    # 選択状態にある図形を取得
    selected_shape = shape_manager.get_selected_shape()
    # print(selected_shape)

    # 選択された図形に対する、FixedPointConstraintオブジェクトの生成
    constraint = FixedPointConstraint(selected_shape.id, selected_shape.x, selected_shape.y)

    # 現在の全ての座標情報を取得
    current_points = shape_manager.get_points()

    # 現在の座標状態の下で、選択された図形に拘束条件を適用（最適化計算を実施）
    updated_points = constraint_manager.apply_constraints(constraint, current_points)

    # その結果でshape_manager.shapesを更新する
    shape_manager.update_shapes(updated_points)

    shapes_data = [shape.to_json() for shape in shape_manager.shapes]
    constraints_data = [constraint.to_json() for constraint in constraint_manager.constraints]

    # 拘束条件を適用した後の図形データをフロントエンドに送り返す
    return jsonify({'status': 'success', 'updated_shapes': shapes_data, 'constraints': constraints_data})

# ---------------------------------------------------------------
# "Apply FixedLengthConstraint" ボタンがクリックされたときの処理
@app.route('/apply_fixed_length_constraint', methods=['POST'])
def apply_fixed_length_constraint():
    # 選択状態にある図形を取得
    selected_shape = shape_manager.get_selected_shape()
    # print(selected_shape)

    # 選択された図形に対する、FixedLengthConstraintオブジェクトの生成
    constraint = FixedLengthConstraint(selected_shape.p1.id,selected_shape.p2.id, selected_shape.length)

    # 現在の全ての座標情報を取得
    current_points = shape_manager.get_points()

    # 現在の座標状態の下で、選択された図形に拘束条件を適用（最適化計算を実施）
    updated_points = constraint_manager.apply_constraints(constraint, current_points)

    # その結果でshape_manager.shapesを更新する
    shape_manager.update_shapes(updated_points)

    shapes_data = [shape.to_json() for shape in shape_manager.shapes]
    constraints_data = [constraint.to_json() for constraint in constraint_manager.constraints]

    # 拘束条件を適用した後の図形データをフロントエンドに送り返す
    return jsonify({'status': 'success', 'updated_shapes': shapes_data, 'constraints': constraints_data})

