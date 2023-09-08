import numpy as np


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


# 座標を持つPointクラスを定義
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_selected = False

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"


# 2つのPointインスタンスを結ぶLineクラスを定義
# Lineインスタンスはその長さも計算
class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.is_selected = False
        self.length = self.calculate_length()

    # Lineインスタンスの長さを計算するメソッド
    def calculate_length(self):
        return np.sqrt((self.p1.x - self.p2.x) ** 2 + (self.p1.y - self.p2.y) ** 2)