from points import Point
from lines import Line
from constraints import *
import numpy as np
from scipy.optimize import minimize
from copy import deepcopy
import matplotlib.pyplot as plt


# 目標点までの距離を計算する関数
# これが最小化の対象となる
def target_point_distance(target_point_index, target_position):

    # この関数は、指定された点と目標位置との距離を計算するための関数を返します。
    def distance(points_flat):

        # もし目標位置が指定されていない場合、0を返します。
        if target_position is None:
            return 0

        # 指定された点の位置を取得します。
        moving_point_position = points_flat[target_point_index * 2: target_point_index * 2 + 2]

        # 指定された点と目標位置との差を計算します。
        diff_vector = moving_point_position - np.array([target_position.x, target_position.y])

        # 計算した差のノルム（大きさ）を返します。これが距離となります。
        return np.linalg.norm(diff_vector)

    return distance


# 目標点への移動を試みる関数
def move_point(target_point, target_position, constraints, points):
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

    res = minimize(target_distance, initial_points_flat, constraints = constraints_for_optimization, method='SLSQP')
    print(res)

    updated_points_flat = res.x
    updated_points = []
    for i in range(0, len(updated_points_flat), 2):
        updated_points.append(Point(updated_points_flat[i], updated_points_flat[i+1]))

    return updated_points


def apply_constraints(constraints, points):
    # Flatten the points for optimization
    initial_points_flat = []
    for point in points:
        initial_points_flat.extend([point.x, point.y])
    initial_points_flat = np.array(initial_points_flat)
    
    # Convert constraints to format suitable for scipy's minimize function    
    constraints_for_optimization = []
    for c in constraints:
        constraint_dict = {'type': 'eq', 'fun': c}
        constraints_for_optimization.append(constraint_dict)

    def target_distance(points_flat):
        return 0
    
    # Use 'SLSQP' method as it supports equality constraints
    res = minimize(target_distance, initial_points_flat, constraints = constraints_for_optimization, method='SLSQP')
    
    # Extract the updated points from the result
    updated_points_flat = res.x
    updated_points = []
    for i in range(0, len(updated_points_flat), 2):
        updated_points.append(Point(updated_points_flat[i], updated_points_flat[i+1]))
    
    return updated_points