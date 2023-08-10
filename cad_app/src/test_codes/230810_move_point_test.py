from points import Point
from lines import Line
from constraints import *
from optimize import move_point
from plot_results import plot_points

# 初期座標と目標座標を設定します。
a = Point(200, 100)
b = Point(200, 300)
c = Point(500, 400)
d = Point(500, 100)
points =[a,b,c,d]

ab = Line(a, b)
bc = Line(b, c)
cd = Line(c, d)
lines = [ab,bc,cd]


# 固定ポイントと固定長さの制約を定義します。ポイントのインデックスとラインの初期長さを使用します。
constraints = [
    FixedPointConstraint(0, points),
    FixedPointConstraint(3, points),
    FixedLengthConstraint(0, 1, ab.length),
    FixedLengthConstraint(1, 2, bc.length),
    FixedLengthConstraint(2, 3, cd.length)]

# 目標点
target_position = Point(600, 300)

# 点cを目標点に移動させます。
new_points = move_point(c, target_position, constraints, points)

print(new_points)

plot_points(points, new_points)