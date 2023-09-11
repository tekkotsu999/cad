import numpy as np
import uuid  # 一意なIDを生成するためのモジュール

class ShapeManager:
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape_type, coordinates):
        if shape_type == 'Point':
            point = Point(coordinates['x'], coordinates['y'])
            self.shapes.append(point)
        elif shape_type == 'Line':
            p1 = Point(coordinates['p1']['x'], coordinates['p1']['y'])
            p2 = Point(coordinates['p2']['x'], coordinates['p2']['y'])
            line = Line(p1, p2)
            self.shapes.append(line)

    def get_shapes(self):
        return self.shapes

    # shapeを定義している全ての点を取得（最適化計算用）
    # 例えば、LIneの場合は、端点の２点を取得し、points配列に格納
    def get_points(self):
        points = []
        for shape in self.shapes:
            if isinstance(shape, Point):
                points.append(shape)
            elif isinstance(shape, Line):
                points.append(shape.p1)
                points.append(shape.p2)
        return points

    # 選択状態にあるshapeを返すメソッド
    def get_selected_shape(self):
        for shape in self.shapes:
            if shape.is_selected:  # 選択状態を確認
                return shape  # 選択状態にあるshapeを返す
        return None  # 選択状態にあるshapeがない場合はNoneを返す

    # 最適化計算の後、self.shapesを更新する
    def update_shapes(self, updated_points):
            updated_points_dict = {point.id: point for point in updated_points}
            for shape in self.shapes:
                if isinstance(shape, Point):
                    if shape.id in updated_points_dict:
                        shape.x = updated_points_dict[shape.id].x
                        shape.y = updated_points_dict[shape.id].y
                elif isinstance(shape, Line):
                    if shape.p1.id in updated_points_dict:
                        shape.p1 = updated_points_dict[shape.p1.id]
                    if shape.p2.id in updated_points_dict:
                        shape.p2 = updated_points_dict[shape.p2.id]

    # idを指定して、shapesからshapeを取得する関数
    def get_shape_by_id(self, shape_id):
        for shape in self.shapes:
            if shape.id == shape_id:
                return shape
        return None  # 指定されたidに対応するshapeが見つからない場合はNoneを返す


# -----------------------------------------------------------------------
# Shapeクラス（基底クラス）
class Shape:
    def __init__(self):
        self.id = str(uuid.uuid4())  # 一意なIDを生成
        self.is_selected = False  # 選択状態を表すフラグ

# -----------------------------------------------------------------------
# 座標を持つPointクラスを定義
class Point(Shape):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(id={self.id}, x={self.x}, y={self.y})"

    def to_json(self):
        return {
            'shape_type': 'Point',
            'id': self.id,
            'coordinates': {'x': self.x, 'y': self.y},
            'is_selected': self.is_selected
        }


# -----------------------------------------------------------------------
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

    def __repr__(self):
        return f"Line(id={self.id}, p1={self.p1}, p2={self.p2}], "

    def to_json(self):
        return {
            'shape_type': 'Line',
            'id': self.id,
            'coordinates': {
                'p1': {'x': self.p1.x, 'y': self.p1.y},
                'p2': {'x': self.p2.x, 'y': self.p2.y}
            },
            'is_selected': self.is_selected
        }