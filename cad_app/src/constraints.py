import numpy as np
import uuid  # 一意なIDを生成するためのモジュール
from scipy.optimize import minimize
import math
import time  # 時間計測用

from .shapes import *

# ConstraintManagerクラス
class ConstraintManager:
    def __init__(self):
        self.constraints = []

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def apply_constraints(self, initial_points, new_point=None, target_point_id=None):
        # print('initial_points:',initial_points)
        # print('new_point:',new_point)
        # print('target_point_id:',target_point_id)

        # Flatten the points for optimization
        initial_points_flat = []
        id_to_index = {}  # IDとindexのマッピング
        for i, point in enumerate(initial_points):
            if point.id == target_point_id:
                # target pointだけ、初期値をtarget pointの位置に近づけておく（高速化目的）
                initial_points_flat.extend([new_point['x'], new_point['y']])
            else:
                initial_points_flat.extend([point.x, point.y])
            id_to_index[point.id] = i  # IDに対応するindexを保存
        initial_points_flat = np.array(initial_points_flat)
        # print('initial_points_flat:',initial_points_flat)
        # print('id_to_index')
        
        target_index = id_to_index.get(target_point_id, None)

        # 目的関数の事前計算（高速化目的）
        if target_index is not None:
            target_index_x = 2 * target_index
            target_index_y = 2 * target_index + 1
            new_x = new_point['x']
            new_y = new_point['y']

        # 目的関数の定義
        def target_distance(initial_points_flat):
            # print(time.time()-start_time)
            return (new_x - initial_points_flat[target_index_x])**2 + (new_y - initial_points_flat[target_index_y])**2

        def target_distance_without_new_point(initial_points_flat):
            return 0

        # Convert constraints to format suitable for scipy's minimize function
        # argsフィールドを使用して、original_pointsを制約関数に渡す  
        constraints_for_optimization = []
        for constraint in self.constraints:
            constraint.get_target_index(initial_points)     # constraintを定義している点に対するindexを更新する（内部に持っているpointのidでindexを特定する）
            constraint_dict = {'type': 'eq', 'fun': constraint}
            constraints_for_optimization.append(constraint_dict)

        # print('optimization start.')
        # Use 'SLSQP' method as it supports equality constraints
        # res = minimize(target_distance, initial_points_flat, constraints = constraints_for_optimization, method='SLSQP')
        if new_point is None or target_point_id is None:
            res = minimize(target_distance_without_new_point, initial_points_flat, constraints = constraints_for_optimization, method='SLSQP')
        else:
            start_time = time.time()
            res = minimize(
                target_distance,
                initial_points_flat,
                constraints = constraints_for_optimization,
                method='SLSQP')
            print('minimize:', time.time()-start_time)

        # print(res.message)
        
        # Check if the optimizer has converged
        if not res.success:
            print("Warning: Optimization did not converge! Message:", res.message)

        # Extract the updated points from the result
        updated_points_flat = res.x
        updated_points = []
        for i, original_point in enumerate(initial_points):
            new_x = updated_points_flat[i * 2]
            new_y = updated_points_flat[i * 2 + 1]
            updated_point = Point(new_x, new_y)
            updated_point.id = original_point.id  # 元のPointオブジェクトからidをコピー
            updated_points.append(updated_point)
        
        # print('updated_points:',updated_points)
        return updated_points
    
    

# -----------------------------------------------------------------------
# FixedPointConstraintクラスは、ある点が固定されていることを表現する
# ポイントのインデックスを引数として取り、そのポイントの位置を最適化変数から取得する
class FixedPointConstraint:
    def __init__(self, fixed_point_id, fixed_x, fixed_y):
        self.id = str(uuid.uuid4())
        self.fixed_point_id = fixed_point_id
        self.fixed_x = fixed_x
        self.fixed_y = fixed_y

    # constraintを定義している点に対するindexを更新する（内部に持っているpointのidでindexを特定する）
    def get_target_index(self, original_points):
        id_to_index = {p.id: i for i, p in enumerate(original_points)}
        self.target_index_x = id_to_index.get(self.fixed_point_id) * 2
        self.target_index_y = self.target_index_x + 1
        return self.target_index_x, self.target_index_y

    def __call__(self, points_flat):
        # 高速化のため平方根は取らない
        return (points_flat[self.target_index_x] - self.fixed_x)**2 + (points_flat[self.target_index_y] - self.fixed_y)**2

    def to_json(self):
        return {
            'constraint_type': 'FixedPointConstraint',
            'fixed_point_id': self.fixed_point_id
        }

# -----------------------------------------------------------------------
# FixedLengthConstraintクラスは、ある線の長さが固定されていることを表現する
# ポイントのインデックスと初期の長さを引数として取り、そのラインの現在の長さを最適化変数から計算する
class FixedLengthConstraint:
    def __init__(self, point1_id, point2_id, length):
        self.id = str(uuid.uuid4())
        self.point1_id = point1_id
        self.point2_id = point2_id
        self.length2 = length ** 2
    
    # constraintを定義している点に対するindexを更新する（内部に持っているpointのidでindexを特定する）
    def get_target_index(self, original_points):
        id_to_index = {p.id: i for i, p in enumerate(original_points)}
        self.point1_index_x = id_to_index.get(self.point1_id) * 2
        self.point1_index_y = self.point1_index_x + 1
        self.point2_index_x = id_to_index.get(self.point2_id) * 2
        self.point2_index_y = self.point2_index_x + 1
        return self.point1_index_x, self.point1_index_y, self.point2_index_x, self.point2_index_y

    def __call__(self, points_flat):
        # 高速化のため平方根は取らない
        return (points_flat[self.point1_index_x] - points_flat[self.point2_index_x])**2 + (points_flat[self.point1_index_y] - points_flat[self.point2_index_y])**2 - self.length2

    def to_json(self):
        return {
            'constraint_type': 'FixedLengthConstraint',
            'p1_id': self.point1_id,
            'p2_id': self.point2_id
        }

# -----------------------------------------------------------------------
# Defining VerticalConstraint class
# このクラスは、2つの点間の線が垂直であることを保証するための制約を提供する
class VerticalConstraint:
    def __init__(self, point1_idx, point2_idx):
        self.point1_idx = point1_idx
        self.point2_idx = point2_idx
    
    # This constraint ensures that the x-coordinates of the two points are the same.
    # 制約としてはこの差が0とすることで扱う
    def __call__(self, points_flat):
        x1 = points_flat[self.point1_idx * 2]
        x2 = points_flat[self.point2_idx * 2]
        return x1 - x2

# Testing the VerticalConstraint class
# points_flat_example = [2, 1, 4, 5]  # Represents points a(2,1) and b(4,5)
# vc = VerticalConstraint(0, 1)
# vc(points_flat_example)  # This should return the difference between x-coordinates of points a and b.


# -----------------------------------------------------------------------
# Defining HorizontalConstraint class
# このクラスは、2つの点間の線が水平であることを保証するための制約を提供する
class HorizontalConstraint:
    def __init__(self, point1_idy, point2_idy):
        self.point1_idy = point1_idy
        self.point2_idy = point2_idy
    

    # This constraint ensures that the y-coordinates of the two points are the same.
    # 制約としてはこの差が0とすることで扱う
    def __call__(self, points_flat):
        y1 = points_flat[self.point1_idy * 2 + 1]
        y2 = points_flat[self.point2_idy * 2 + 1]
        return y1 - y2

# -----------------------------------------------------------------------
# Define the CoincidentPointsConstraint class
# 点と点の一致拘束
class CoincidentPointsConstraint:
    def __init__(self, point1_idx, point2_idx):
        self.point1_idx = point1_idx
        self.point2_idx = point2_idx

    def __call__(self, points_flat):
        # Extract the positions of the two points
        point1_position = np.array(points_flat[self.point1_idx * 2: self.point1_idx * 2 + 2])
        point2_position = np.array(points_flat[self.point2_idx * 2: self.point2_idx * 2 + 2])
        
        # Compute the difference vector between the two points
        diff_vector = point1_position - point2_position
        
        # Return the norm of the difference vector. This value should be minimized to zero for the two points to coincide.
        return np.linalg.norm(diff_vector)

# -----------------------------------------------------------------------
# Define the PointOnLineConstraint class
# 点と線の一致拘束
# 線上の任意の点は、線の両端の点を使って、以下のパラメータ方程式で表現できる：
#   x = x_1 + t * ( x_2 - x_1 )
#   y = y_1 + t * ( y_2 - y_2 )
# ここで、tは0から1の間のパラメータである。
# 点が直線上にある場合、その点のxとy座標は、上記の方程式を満たすtが存在する。
# これを利用して「点と線の一致拘束」を定義する。
class PointOnLineConstraint:
    def __init__(self, point_idx, line_point1_idx, line_point2_idx):
        self.point_idx = point_idx
        self.line_point1_idx = line_point1_idx
        self.line_point2_idx = line_point2_idx

    def __call__(self, points_flat):
        # Extract the positions of the point and the line's endpoints
        point_position = np.array(points_flat[self.point_idx * 2: self.point_idx * 2 + 2])
        line_point1_position = np.array(points_flat[self.line_point1_idx * 2: self.line_point1_idx * 2 + 2])
        line_point2_position = np.array(points_flat[self.line_point2_idx * 2: self.line_point2_idx * 2 + 2])
        
        # Compute the t values for x and y
        if line_point2_position[0] - line_point1_position[0] != 0:  # Avoid division by zero
            t_x = (point_position[0] - line_point1_position[0]) / (line_point2_position[0] - line_point1_position[0])
        else:
            t_x = 0
        
        if line_point2_position[1] - line_point1_position[1] != 0:  # Avoid division by zero
            t_y = (point_position[1] - line_point1_position[1]) / (line_point2_position[1] - line_point1_position[1])
        else:
            t_y = 0
        
        # Return the difference between the computed t values. This value should be minimized to zero for the point to lie on the line.
        return t_x - t_y

# -----------------------------------------------------------------------
# Define the ParallelLinesConstraint class
# 線と線の平行拘束
# 2つの線が平行である場合、それらの線の方向ベクトルが一致するか、または逆向きである必要がある。
# 方向ベクトルは線の両端の点を使用して計算する
class ParallelLinesConstraint:
    def __init__(self, line1_point1_idx, line1_point2_idx, line2_point1_idx, line2_point2_idx):
        self.line1_point1_idx = line1_point1_idx
        self.line1_point2_idx = line1_point2_idx
        self.line2_point1_idx = line2_point1_idx
        self.line2_point2_idx = line2_point2_idx

    def __call__(self, points_flat):
        # Extract the positions of the line's endpoints
        line1_point1_position = np.array(points_flat[self.line1_point1_idx * 2: self.line1_point1_idx * 2 + 2])
        line1_point2_position = np.array(points_flat[self.line1_point2_idx * 2: self.line1_point2_idx * 2 + 2])
        line2_point1_position = np.array(points_flat[self.line2_point1_idx * 2: self.line2_point1_idx * 2 + 2])
        line2_point2_position = np.array(points_flat[self.line2_point2_idx * 2: self.line2_point2_idx * 2 + 2])
        
        # Calculate the direction vectors for each line
        dir_vector1 = line1_point2_position - line1_point1_position
        dir_vector2 = line2_point2_position - line2_point1_position
        
        # Calculate the cross product of the two direction vectors. If they are parallel, this value will be zero.
        cross_product = np.cross(dir_vector1, dir_vector2)
        
        return cross_product

# -----------------------------------------------------------------------
# Define the PerpendicularLinesConstraint class
# 線と線の垂直拘束
# 2つの線が垂直である場合、それらの線の方向ベクトルのドット積は0である必要がある
# 方向ベクトルは線の両端の点を使用して計算する
class PerpendicularLinesConstraint:
    def __init__(self, line1_point1_idx, line1_point2_idx, line2_point1_idx, line2_point2_idx):
        self.line1_point1_idx = line1_point1_idx
        self.line1_point2_idx = line1_point2_idx
        self.line2_point1_idx = line2_point1_idx
        self.line2_point2_idx = line2_point2_idx

    def __call__(self, points_flat):
        # Extract the positions of the line's endpoints
        line1_point1_position = np.array(points_flat[self.line1_point1_idx * 2: self.line1_point1_idx * 2 + 2])
        line1_point2_position = np.array(points_flat[self.line1_point2_idx * 2: self.line1_point2_idx * 2 + 2])
        line2_point1_position = np.array(points_flat[self.line2_point1_idx * 2: self.line2_point1_idx * 2 + 2])
        line2_point2_position = np.array(points_flat[self.line2_point2_idx * 2: self.line2_point2_idx * 2 + 2])
        
        # Calculate the direction vectors for each line
        dir_vector1 = line1_point2_position - line1_point1_position
        dir_vector2 = line2_point2_position - line2_point1_position
        
        # Calculate the dot product of the two direction vectors. If they are perpendicular, this value will be zero.
        dot_product = np.dot(dir_vector1, dir_vector2)
        
        return dot_product

# -----------------------------------------------------------------------
# Define the EqualLengthLinesConstraint class
# 線長一致拘束
# 2つの線の長さの差を計算し、その差が0になるように制約を適用する
class EqualLengthLinesConstraint:
    def __init__(self, line1_point1_idx, line1_point2_idx, line2_point1_idx, line2_point2_idx):
        self.line1_point1_idx = line1_point1_idx
        self.line1_point2_idx = line1_point2_idx
        self.line2_point1_idx = line2_point1_idx
        self.line2_point2_idx = line2_point2_idx

    def __call__(self, points_flat):
        # Extract the positions of the line's endpoints
        line1_point1_position = np.array(points_flat[self.line1_point1_idx * 2: self.line1_point1_idx * 2 + 2])
        line1_point2_position = np.array(points_flat[self.line1_point2_idx * 2: self.line1_point2_idx * 2 + 2])
        line2_point1_position = np.array(points_flat[self.line2_point1_idx * 2: self.line2_point1_idx * 2 + 2])
        line2_point2_position = np.array(points_flat[self.line2_point2_idx * 2: self.line2_point2_idx * 2 + 2])
        
        # Calculate the lengths of each line
        length1 = np.linalg.norm(line1_point2_position - line1_point1_position)
        length2 = np.linalg.norm(line2_point2_position - line2_point1_position)
        
        # Return the difference in lengths
        return length1 - length2