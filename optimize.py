import numpy as np
from scipy.optimize import minimize

###########################################

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    @property
    def length(self):
        return np.sqrt((self.p1.x - self.p2.x) ** 2 + (self.p1.y - self.p2.y) ** 2)

###########################################

class Constraint:
    def evaluate(self, points):
        """
        Evaluate the constraint.
        :param points: A dictionary of points.
        :return: The value of the constraint function.
        """
        raise NotImplementedError

class FixedDistanceConstraint(Constraint):
    def __init__(self, point1, point2, distance):
        self.point1 = point1
        self.point2 = point2
        self.distance = distance

    def evaluate(self, points):
        p1 = points[self.point1]
        p2 = points[self.point2]
        return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5 - self.distance

class FixedPointConstraint(Constraint):
    def __init__(self, point, x, y):
        self.point = point
        self.x = x
        self.y = y

    def evaluate(self, points):
        p = points[self.point]
        return (p.x - self.x) ** 2 + (p.y - self.y) ** 2


###########################################

def objective_function(point_array, target_x, target_y):
    x, y = point_array
    # 点と目標点との距離の二乗を計算
    distance_squared = (x - target_x) ** 2 + (y - target_y) ** 2
    return distance_squared

def constraint_function(points_array, constraint):
    points = {f'p{i}': Point(points_array[2*i], points_array[2*i + 1]) for i in range(len(points_array) // 2)}
    return constraint.evaluate(points)

###########################################

def run_optimization(constraints, initial_point, target_x, target_y):  #data):
    # 空のリストを作成して、scipyの制約条件を格納します。
    scipy_constraints = []

    # constraintsリスト内の各制約オブジェクトに対してループを実行します。
    for constraint in constraints:
        # scipyの制約条件の辞書を作成します。
        scipy_constraint = {
            'type': 'eq',               # 等式制約を指定します。
            'fun': constraint_function, # 制約関数を指定します。
            'args': (constraint,)       # 制約関数に渡す追加の引数を指定します。
        }
        
        # 作成した辞書をリストに追加します。
        scipy_constraints.append(scipy_constraint)


    # 目的関数に渡す追加の引数
    additional_args = (target_x, target_y)

    # 最適化を実行
    result = minimize(
        fun = objective_function,        # 最小化する目的関数
        x0 = initial_point,              # 最適化の初期推定値
        args = additional_args,          # 目的関数に渡す追加の引数
        constraints = scipy_constraints  # 最適化に適用する制約条件
    )
    
    print(result)

    # The optimized point is in result.x
    optimized_point = result.x


    return optimized_point


    #a = Point(data['a']['x'], data['a']['y'])
    #b = Point(data['b']['x'], data['b']['y'])
    #c = Point(data['c']['x'], data['c']['y'])
    #d = Point(data['d']['x'], data['d']['y'])
    #dx, dy = data['displacement']
    
    #ab = Line(a, b)
    #bc = Line(b, c)
    #cd = Line(c, d)
    #da = Line(d, a)

    # def objective(z):
    #    return ((c.x+dx)-z[2]) ** 2 + ((c.y+dy)-z[3]) ** 2

    #def constraint1(z):
    #    return np.sqrt((a.x - z[0]) ** 2 + (a.y - z[1]) ** 2) - ab.length

    #def constraint2(z):
    #    return np.sqrt((z[2] - z[0]) ** 2 + (z[3] - z[1]) ** 2) - bc.length

    #def constraint3(z):
    #    return np.sqrt((z[2] - d.x) ** 2 + (z[3] - d.y) ** 2) - cd.length

    #cons = [{'type': 'eq', 'fun': constraint1},
    #        {'type': 'eq', 'fun': constraint2},
    #        {'type': 'eq', 'fun': constraint3}]

    #x0 = np.array([b.x, b.y, c.x, c.y])

    #sol = minimize(objective, x0, constraints=cons, method='SLSQP')

    #result = {
    #    'b': {'x': sol.x[0], 'y': sol.x[1]},
    #    'c': {'x': sol.x[2], 'y': sol.x[3]}
    #}

    #return result


###########################################

# Example usage:
constraints = [
    FixedDistanceConstraint('p0', 'p1', 3),
    FixedPointConstraint('p1', 2, 2)
]

initial_point = np.array([0.5, 0.5])  # Initial point (x=0.5, y=0.5)
target_x = 5
target_y = 5

# Run the optimization
optimized_point = run_optimization(constraints, initial_point, target_x, target_y)

# Output the result

print("\n")
print(f"Optimized point: x={optimized_point[0]}, y={optimized_point[1]}")


###########################################

input("Waiting for key press...")
