from points import Point
import numpy as np

# FixedPointConstraintクラスは、ある点が固定されていることを表現する
# ポイントのインデックスを引数として取り、そのポイントの位置を最適化変数から取得する
class FixedPointConstraint:
    def __init__(self, point_idx):
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