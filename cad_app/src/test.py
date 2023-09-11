from shapes import *
from constraints import *
from optimize import *
from plot_results import plot_points_with_lines

# 使用例
shape_manager = ShapeManager()
constraint_manager = ConstraintManager()

lines = [ Line(Point(0, 0),Point(1, 1)) ]
shape_manager.shapes.extend( lines )

# FixedPointConstraintを作成してConstraintManagerに追加
constraint1 = FixedPointConstraint( lines[0].p1.id, 0, 0.5 )
constraint_manager.add_constraint(constraint1)

# FixedLengthConstraintを作成してConstraintManagerに追加
constraint2 = FixedLengthConstraint( lines[0].p1.id, lines[0].p2.id, lines[0].length)
constraint_manager.add_constraint(constraint2)

# 最適化を実行
points = shape_manager.get_points()
constraints = constraint_manager.constraints
updated_points = optimization(constraints, points)

updated_lines = [ Line(updated_points[0], updated_points[1]) ]

plot_points_with_lines(points, updated_points, lines, updated_lines)
