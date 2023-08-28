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
            start = Point(coordinates['start']['x'], coordinates['start']['y'])
            end = Point(coordinates['end']['x'], coordinates['end']['y'])
            line = Line(start, end)
            self.shapes.append(line)

    def get_shapes(self):
        return self.shapes