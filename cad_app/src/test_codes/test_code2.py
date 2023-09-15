from sympy import symbols, Eq, solve, sqrt
import time  # 時間計測用

# 点のクラス定義
class Point:
    def __init__(self, x, y):
        self.x, self.y = symbols(f"{x} {y}")

# 線のクラス定義
class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

# 拘束条件を適用する関数
def apply_constraints(constraints, *objects):
    equations = []

    for constraint, params in constraints:
        if constraint == "fixed":
            point = params[0]
            x_val, y_val = params[1]
            equations.append(Eq(point.x, x_val))
            equations.append(Eq(point.y, y_val))

        elif constraint == "on_line":
            point, line = params
            t = symbols('t')
            equations.append(Eq(point.x, line.point1.x + t * (line.point2.x - line.point1.x)))
            equations.append(Eq(point.y, line.point1.y + t * (line.point2.y - line.point1.y)))

        elif constraint == "length":
            line, length = params
            equations.append(Eq(sqrt((line.point2.x - line.point1.x)**2 + (line.point2.y - line.point1.y)**2), length))

        elif constraint == "parallel":
            line1, line2 = params
            equations.append(Eq((line1.point2.y - line1.point1.y) * (line2.point2.x - line2.point1.x),
                                (line1.point2.x - line1.point1.x) * (line2.point2.y - line2.point1.y)))

        elif constraint == "perpendicular":
            line1, line2 = params
            equations.append(Eq((line1.point2.y - line1.point1.y) * (line2.point2.y - line2.point1.y),
                                -(line1.point2.x - line1.point1.x) * (line2.point2.x - line2.point1.x)))

        elif constraint == "coincident":
            point1, point2 = params
            equations.append(Eq(point1.x, point2.x))
            equations.append(Eq(point1.y, point2.y))

    solution = solve(equations, dict=True)
    
    if len(solution) == 0:
        return "解が存在しません。", None
    elif len(solution) == 1:
        return "一意の解が存在します。", solution
    else:
        return "複数の解が存在します。", solution

# 点と線の定義
A = Point('Ax', 'Ay')
B = Point('Bx', 'By')
C = Point('Cx', 'Cy')
D = Point('Dx', 'Dy')
E = Point('Ex', 'Ey')
line1 = Line(A, B)
line2 = Line(B, C)
line3 = Line(C, D)
line4 = Line(D, E)

# 拘束条件の定義と適用
constraints = [
    ("fixed", [A, (0, 0)]),
    ("fixed", [D, (3, 0)]),
    #("on_line", [C, line1]),
    ("length", [line1, 3]),
    ("length", [line2, 3]),
    ("length", [line3, 2]),
    #("parallel", [line1, line3]),
    #("perpendicular", [line1, line2]),
    #("parallel", [line1, line3]),
    ("coincident", [A, E])
]

start_time = time.time()

message, solution = apply_constraints(constraints)

print('time:', time.time()-start_time)

# 結果とメッセージの表示
print(message)
if solution is not None:
    print(f"解は {solution} です。")
