from points import Point
from lines import Line
from constraints import FixedPointConstraint, FixedLengthConstraint
import numpy as np
from scipy.optimize import minimize
from copy import deepcopy
import matplotlib.pyplot as plt


# 目標点までの距離を計算する関数
# これが最小化の対象となる
def target_point_distance(target_point_index, target_position):
    def distance(points_flat):
        moving_point_position = points_flat[target_point_index * 2: target_point_index * 2 + 2]
        diff_vector = moving_point_position - np.array([target_position.x, target_position.y])
        return np.linalg.norm(diff_vector)
    return distance


# 目標点への移動を試みる関数
def move_point(target_point, target_position, constraints):
    initial_points_flat = []
    for point in points:
        initial_points_flat.extend([point.x, point.y])
    initial_points_flat = np.array(initial_points_flat)

    target_point_index = points.index(target_point)
    target_distance = target_point_distance(target_point_index, target_position)

    constraints_for_optimization = []
    for c in constraints:
        constraint_dict = {'type': 'eq', 'fun': c}
        constraints_for_optimization.append(constraint_dict)

    res = minimize(target_distance, initial_points_flat, constraints=constraints_for_optimization, method='SLSQP')
    print(res)

    # 初期座標を抽出
    initial_x_values = [point.x for point in points]
    initial_y_values = [point.y for point in points]

    # 初期座標をプロット
    plt.figure()
    plt.scatter(initial_x_values, initial_y_values)
    plt.plot(initial_x_values, initial_y_values, linestyle='dashed', label='Initial Position')

    updated_points_flat = res.x
    updated_points = []
    for i in range(0, len(updated_points_flat), 2):
        updated_points.append(Point(updated_points_flat[i], updated_points_flat[i+1]))
    
    
    # 結果の座標を抽出
    x_values = [point.x for point in updated_points]
    y_values = [point.y for point in updated_points]

    # 結果をプロット
    plt.scatter(x_values, y_values)
    plt.plot(x_values, y_values)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Point Movement')
    plt.legend()
    plt.grid(True)
    plt.show()

    return updated_points