from points import Point
from lines import Line
import numpy as np

# FixedPointConstraintクラスは、ある点が固定されていることを表現する
# ポイントのインデックスを引数として取り、そのポイントの位置を最適化変数から取得する
class FixedPointConstraint:
    def __init__(self, point_idx, points):
        self.point_idx = point_idx
        self.initial_point = points[point_idx]

    # 初期位置からの変位を計算します。
    # 制約としてはこの変位が0であることで扱う
    def __call__(self, points_flat):
        current_point = Point(*points_flat[self.point_idx * 2: self.point_idx * 2 + 2])
        diff_vector =  np.array([self.initial_point.x, self.initial_point.y]) - np.array([current_point.x,current_point.y])
        return np.linalg.norm(diff_vector)


# FixedLengthConstraintクラスは、ある線の長さが固定されていることを表現する
# ポイントのインデックスと初期の長さを引数として取り、そのラインの現在の長さを最適化変数から計算する
class FixedLengthConstraint:
    def __init__(self, point1_idx, point2_idx, initial_length):
        self.point1_idx = point1_idx
        self.point2_idx = point2_idx
        self.initial_length = initial_length

    # 線の現在の長さと初期の長さとの差を計算します。
    # 制約としてはこの差が0とすることで扱う
    def __call__(self, points_flat):
        point1 = Point(*points_flat[self.point1_idx * 2: self.point1_idx * 2 + 2])
        point2 = Point(*points_flat[self.point2_idx * 2: self.point2_idx * 2 + 2])
        current_length = Line(point1, point2).length
        return current_length - self.initial_length


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