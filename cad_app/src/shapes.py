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
            p1 = Point(coordinates['p1']['x'], coordinates['p1']['y'])
            p2 = Point(coordinates['p2']['x'], coordinates['p2']['y'])
            line = Line(p1, p2)
            self.shapes.append(line)

    def get_shapes(self):
        return self.shapes