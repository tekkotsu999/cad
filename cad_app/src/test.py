import uuid
import numpy as np
from scipy.optimize import minimize
from plot_results import plot_points_with_lines

# Shapeクラス（基底クラス）
class Shape:
    def __init__(self):
        self.unique_id = str(uuid.uuid4())  # 一意なIDを生成
        self.is_selected = False  # 選択状態を表すフラグ

# 座標を持つPointクラスを定義
class Point(Shape):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(id={self.unique_id}, x={self.x}, y={self.y})"

# 2つのPointインスタンスを結ぶLineクラスを定義
# Lineインスタンスはその長さも計算
class Line(Shape):
    def __init__(self, p1, p2):
        super().__init__()
        self.p1 = p1
        self.p2 = p2

    # Lineインスタンスの長さを計算するメソッド
    @property
    def length(self):
        return np.sqrt((self.p1.x - self.p2.x) ** 2 + (self.p1.y - self.p2.y) ** 2)

# ShapeManagerクラス
class ShapeManager:
    def __init__(self):
        self.shapes = []

    def get_points(self):
        points = []
        for shape in self.shapes:
            if isinstance(shape, Point):
                points.append(shape)
            elif isinstance(shape, Line):
                points.append(shape.p1)
                points.append(shape.p2)
        return points

# FixedPointConstraintクラス
class FixedPointConstraint:
    def __init__(self, point_id, fixed_x, fixed_y):
        self.constraint_id = str(uuid.uuid4())
        self.point_id = point_id
        self.fixed_x = fixed_x
        self.fixed_y = fixed_y

    def __call__(self, points_flat, original_points):
        points = [Point(points_flat[i], points_flat[i+1]) for i in range(0, len(points_flat), 2)]
        for i, p in enumerate(original_points):
            points[i].unique_id = p.unique_id  # unique_idを元のPointオブジェクトからコピー

        # 以降は同じ
        point = next(p for p in points if p.unique_id == self.point_id)
        dx = point.x - self.fixed_x
        dy = point.y - self.fixed_y
        return np.sqrt(dx**2 + dy**2)

# FixedLengthConstraintクラス
class FixedLengthConstraint:
    def __init__(self, point1_id, point2_id, length):
        self.constraint_id = str(uuid.uuid4())
        self.point1_id = point1_id
        self.point2_id = point2_id
        self.length = length

    def __call__(self, points_flat, original_points):
        # points_flatからPointオブジェクトのリストを生成
        points = [Point(points_flat[i], points_flat[i+1]) for i in range(0, len(points_flat), 2)]
        
        # unique_idを元のPointオブジェクトからコピー
        for i, p in enumerate(original_points):
            points[i].unique_id = p.unique_id

        # unique_idを使って、対象となるPointオブジェクトを見つける
        point1 = next(p for p in points if p.unique_id == self.point1_id)
        point2 = next(p for p in points if p.unique_id == self.point2_id)

        # 点間の距離を計算
        dx = point1.x - point2.x
        dy = point1.y - point2.y
        return np.sqrt(dx**2 + dy**2) - self.length

# ConstraintManagerクラス
class ConstraintManager:
    def __init__(self):
        self.constraints = []

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

# 最適化関数
def optimization(constraints, points):
    initial_points_flat = []
    for point in points:
        initial_points_flat.extend([point.x, point.y])
    initial_points_flat = np.array(initial_points_flat)

    # argsフィールドを使用して、original_pointsを制約関数に渡す
    constraints_for_optimization = [{'type': 'eq', 'fun': c, 'args': (points,)} for c in constraints]

    def target_distance(points_flat):
        return 0

    res = minimize(target_distance, initial_points_flat, constraints=constraints_for_optimization, method='SLSQP')

    if not res.success:
        print("Warning: Optimization did not converge! Message:", res.message)

    updated_points_flat = res.x
    updated_points = [Point(updated_points_flat[i], updated_points_flat[i+1]) for i in range(0, len(updated_points_flat), 2)]

    return updated_points



# 使用例
shape_manager = ShapeManager()
constraint_manager = ConstraintManager()

lines = [ Line(Point(0, 0),Point(1, 1)) ]
shape_manager.shapes.extend( lines )

# FixedPointConstraintを作成してConstraintManagerに追加
constraint1 = FixedPointConstraint( lines[0].p1.unique_id, 0, 0.5 )
constraint_manager.add_constraint(constraint1)

# FixedLengthConstraintを作成してConstraintManagerに追加
constraint2 = FixedLengthConstraint( lines[0].p1.unique_id, lines[0].p2.unique_id, lines[0].length)
constraint_manager.add_constraint(constraint2)

# 最適化を実行
points = shape_manager.get_points()
constraints = constraint_manager.constraints
updated_points = optimization(constraints, points)

updated_lines = [ Line(updated_points[0], updated_points[1]) ]

plot_points_with_lines(points, updated_points, lines, updated_lines)
