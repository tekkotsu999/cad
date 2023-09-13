from flask import render_template
from . import app  # __init__.pyからFlaskアプリケーションインスタンスをインポート
import math
import time  # 時間計測用

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

    added_shape = shape_manager.add_shape(shape_type, coordinates)

    return jsonify({'status': 'success', 'added_shape': added_shape.to_json()})

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
                    if isinstance(shape_tmp, Line):
                        shape_tmp.p1.is_selected = False
                        shape_tmp.p2.is_selected = False

                shape.is_selected = True
                return jsonify({'status': 'success', 'selected_shape': shape.to_json()})
    
    # 線の選択と端点の選択
    for shape in shape_manager.get_shapes():
        if isinstance(shape, Line):
            # 線とクリック位置との距離を計算
            distance_line = calculate_line_distance(shape, click_x, click_y)
            
            # 線の両端点とクリック位置との距離を計算
            distance_p1 = math.sqrt((shape.p1.x - click_x)**2 + (shape.p1.y - click_y)**2)
            distance_p2 = math.sqrt((shape.p2.x - click_x)**2 + (shape.p2.y - click_y)**2)

            # 線または端点がクリックされたかどうかの判定
            if distance_line < tolerance or distance_p1 < tolerance or distance_p2 < tolerance:
                # 全てのshapeのis_selectedをリセット
                for shape_tmp in shape_manager.get_shapes():
                    shape_tmp.is_selected = False
                    if isinstance(shape_tmp, Line):
                        shape_tmp.p1.is_selected = False
                        shape_tmp.p2.is_selected = False
                
                # 端点が選択された場合
                if distance_p1 < tolerance:
                    shape.p1.is_selected = True
                    return jsonify({'status': 'success', 'selected_shape': shape.p1.to_json()})
                if distance_p2 < tolerance:
                    shape.p2.is_selected = True
                    return jsonify({'status': 'success', 'selected_shape': shape.p2.to_json()})

                # 線自体が選択された場合
                if distance_line < tolerance:
                    shape.is_selected = True
                    return jsonify({'status': 'success', 'selected_shape': shape.to_json()})              

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

# ---------------------------------------------------------------
# 最後に処理されたリクエストのID
last_processed_request_id = 0
request_id = 0

@app.route('/move_point', methods=['POST'])
def move_point():
    global last_processed_request_id
    global request_id
    
    # これから処理するrequest_id
    request_id = request_id + 1

    # フロントエンドから送られてくるデータを取得
    data = request.json
    new_point = data.get('new_point')
    target_point_id = data.get('target_point_id')
    # request_id = data.get('request_id')  # 一意のリクエストID

    #print('* last req:',last_processed_request_id)
    #print('* new req:',request_id)
    # 古いリクエストを無視
    if request_id - 1 > last_processed_request_id:
        print('Ignored. request_id :',request_id)
        return jsonify({"status": "ignored"})

    # ShapeManagerから現在の全ての点を取得
    points = shape_manager.get_points()
    
    #print(f"* start req: {request_id}")

    # 処理開始時間を記録
    start_time = time.time()

    # 拘束条件をを適用
    updated_points = constraint_manager.apply_constraints(points, new_point, target_point_id)
    
    # 処理終了時間を記録
    end_time = time.time()

    # その結果でshape_manager.shapesを更新する
    shape_manager.update_shapes(updated_points)

    shapes_data = [shape.to_json() for shape in shape_manager.shapes]
    constraints_data = [constraint.to_json() for constraint in constraint_manager.constraints]

    # 最後に処理されたリクエストのIDを更新
    last_processed_request_id = request_id

    # 処理時間を計算
    elapsed_time = end_time - start_time

    # 処理時間とリクエストIDをログに出力
    print(f"* done req: {request_id}, Elapsed Time: {elapsed_time} seconds")

    # 拘束条件を適用した後の図形データをフロントエンドに送り返す
    return jsonify({'status': 'success', 'updated_shapes': shapes_data, 'constraints': constraints_data})


@app.route('/reset_request_id', methods=['POST'])
def reset_request_id():
    global last_processed_request_id
    global request_id
    last_processed_request_id = 0
    request_id = 0
    return jsonify({'status': 'success'})

# ---------------------------------------------------------------
# "Apply FixedPointConstraint" ボタンがクリックされたときの処理
@app.route('/apply_fixed_point_constraint', methods=['POST'])
def apply_fixed_point_constraint():
    # 選択状態にある図形を取得
    selected_shape = shape_manager.get_selected_shape()

    # selected_shapeの内容によって処理を分岐
    if selected_shape is None:
        # selected_shapeがNoneの場合は何もしない
        return jsonify({'status': 'no shape selected'})

    elif isinstance(selected_shape, Point):
        # selected_shapeがPointオブジェクトの場合

        # 選択された図形に対する、FixedPointConstraintオブジェクトを生成
        constraint = FixedPointConstraint(selected_shape.id, selected_shape.x, selected_shape.y)
        constraint_manager.add_constraint(constraint)

        # 現在の全ての座標情報を取得
        current_points = shape_manager.get_points()

        # 現在の座標状態の下で、選択された図形に拘束条件を適用（最適化計算を実施）
        updated_points = constraint_manager.apply_constraints(current_points)

        # その結果でshape_manager.shapesを更新する
        shape_manager.update_shapes(updated_points)

        shapes_data = [shape.to_json() for shape in shape_manager.shapes]
        constraints_data = [constraint.to_json() for constraint in constraint_manager.constraints]

        # 拘束条件を適用した後の図形データをフロントエンドに送り返す
        return jsonify({'status': 'success', 'updated_shapes': shapes_data, 'constraints': constraints_data})

    elif isinstance(selected_shape, Line):
        # selected_shapeがLineオブジェクトの場合

        # 線の端点（２点）に対する、FixedPointConstraintオブジェクトを生成
        constraint1 = FixedPointConstraint(selected_shape.p1.id, selected_shape.p1.x, selected_shape.p1.y)
        constraint2 = FixedPointConstraint(selected_shape.p2.id, selected_shape.p2.x, selected_shape.p2.y)
        constraint_manager.add_constraint(constraint1)
        constraint_manager.add_constraint(constraint2)

        # 現在の全ての座標情報を取得
        current_points = shape_manager.get_points()

        # 現在の座標状態の下で、選択された図形に拘束条件を適用（最適化計算を実施）
        updated_points = constraint_manager.apply_constraints(current_points)

        # その結果でshape_manager.shapesを更新する
        shape_manager.update_shapes(updated_points)

        shapes_data = [shape.to_json() for shape in shape_manager.shapes]
        constraints_data = [constraint.to_json() for constraint in constraint_manager.constraints]

        # 拘束条件を適用した後の図形データをフロントエンドに送り返す
        return jsonify({'status': 'success', 'updated_shapes': shapes_data, 'constraints': constraints_data})

    else:
        return jsonify({'status': 'unknown shape type'})




# ---------------------------------------------------------------
# "Apply FixedLengthConstraint" ボタンがクリックされたときの処理
@app.route('/apply_fixed_length_constraint', methods=['POST'])
def apply_fixed_length_constraint():
    # 選択状態にある図形を取得
    selected_shape = shape_manager.get_selected_shape()

    # selected_shapeの内容によって処理を分岐
    if selected_shape is None:
        # selected_shapeがNoneの場合は何もしない
        return jsonify({'status': 'no shape selected'})

    elif isinstance(selected_shape, Point):
        # selected_shapeがPointオブジェクトの場合はエラーを出力
        return jsonify({'status': 'error', 'message': 'Cannot apply length constraint to a Point'})

    elif isinstance(selected_shape, Line):
        # selected_shapeがLineオブジェクトの場合

        # 選択された図形に対する、FixedLengthConstraintオブジェクトの生成
        constraint = FixedLengthConstraint(selected_shape.p1.id,selected_shape.p2.id, selected_shape.length)
        constraint_manager.add_constraint(constraint)

        # 現在の全ての座標情報を取得
        current_points = shape_manager.get_points()

        # 現在の座標状態の下で、選択された図形に拘束条件を適用（最適化計算を実施）
        updated_points = constraint_manager.apply_constraints(current_points)

        # その結果でshape_manager.shapesを更新する
        shape_manager.update_shapes(updated_points)

        shapes_data = [shape.to_json() for shape in shape_manager.shapes]
        constraints_data = [constraint.to_json() for constraint in constraint_manager.constraints]

        # 拘束条件を適用した後の図形データをフロントエンドに送り返す
        return jsonify({'status': 'success', 'updated_shapes': shapes_data, 'constraints': constraints_data})

    else:
        return jsonify({'status': 'unknown shape type'})

