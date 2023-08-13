import numpy as np
from scipy.optimize import minimize

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    @property
    def length(self):
        return np.sqrt((self.p1.x - self.p2.x) ** 2 + (self.p1.y - self.p2.y) ** 2)

def run_optimization(data):

    a = Point(data['a']['x'], data['a']['y'])
    b = Point(data['b']['x'], data['b']['y'])
    c = Point(data['c']['x'], data['c']['y'])
    d = Point(data['d']['x'], data['d']['y'])
    dx, dy = data['displacement']
    
    ab = Line(a, b)
    bc = Line(b, c)
    cd = Line(c, d)
    da = Line(d, a)
    
    # print(a)
    # print(b)
    # print(c)
    # print(d)
    # print(dx,dy)
    
    def objective(z):
        return ((c.x+dx)-z[2]) ** 2 + ((c.y+dy)-z[3]) ** 2

    def constraint1(z):
        return np.sqrt((a.x - z[0]) ** 2 + (a.y - z[1]) ** 2) - ab.length

    def constraint2(z):
        return np.sqrt((z[2] - z[0]) ** 2 + (z[3] - z[1]) ** 2) - bc.length

    def constraint3(z):
        return np.sqrt((z[2] - d.x) ** 2 + (z[3] - d.y) ** 2) - cd.length

    cons = [{'type': 'eq', 'fun': constraint1},
            {'type': 'eq', 'fun': constraint2},
            {'type': 'eq', 'fun': constraint3}]

    x0 = np.array([b.x, b.y, c.x, c.y])

    sol = minimize(objective, x0, constraints=cons, method='SLSQP')

    result = {
        'a': { 'x': a.x, 'y': a.y },
        'b': { 'x': sol.x[0], 'y': sol.x[1] },
        'c': { 'x': sol.x[2], 'y': sol.x[3] },
        'd': { 'x': d.x, 'y': d.y }
    }
    
    # print(result)

    return result

