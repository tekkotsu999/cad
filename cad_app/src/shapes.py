from .points import Point
from .lines import Line

class ShapeManager:
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape_type, coordinates):
        if shape_type == 'Point':
            point = Point(coordinates['x'], coordinates['y'])
            self.shapes.append(point)
        elif shape_type == 'Line':
            # 線の場合の処理
            pass
        # 他の図形もここに追加

    def get_shapes(self):
        return self.shapes