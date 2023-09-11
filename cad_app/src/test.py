from shapes import *
from constraints import *
from plot_results import plot_results
from scipy.optimize import minimize
from copy import deepcopy

shape_manager = ShapeManager()
constraint_manager = ConstraintManager()

lines = [ Line(Point(0, 0), Point(1, 1)) ]
shape_manager.shapes.extend( lines )
initial_shapes = deepcopy(shape_manager.shapes)


constraint = FixedLengthConstraint( lines[0].p1.id, lines[0].p2.id, lines[0].length )
current_points = shape_manager.get_points()
updated_points = constraint_manager.apply_constraints(constraint, current_points)
shape_manager.update_shapes(updated_points)


constraint = FixedPointConstraint( lines[0].p1.id, 0, 0.5 )
current_points = shape_manager.get_points()
updated_points = constraint_manager.apply_constraints(constraint, current_points)
shape_manager.update_shapes(updated_points)


plot_results(initial_shapes, shape_manager.shapes)
