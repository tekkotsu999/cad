from points import Point
from lines import Line
from constraints import FixedPointConstraint, FixedLengthConstraint
from optimize import move_point
from plot_results import plot_points

a = Point(2, 2)
b = Point(5, 3)
points = [a, b]
ab = Line(a, b)
constraints = [FixedPointConstraint(0, points), FixedLengthConstraint(0, 1, ab.length)]
target_position = Point(5, 6)

new_points = move_point(b, target_position, constraints, points)

print(new_points)

plot_points(points, new_points)