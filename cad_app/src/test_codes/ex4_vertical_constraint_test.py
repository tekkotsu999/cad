from points import Point
from lines import Line
from constraints import *
from optimize import apply_constraints
from plot_results import plot_points

# Define the points and lines
a = Point(2, 1)
b = Point(4, 5)
points = [a, b]
ab = Line(a, b)

# Define the initial constraints (State 1)
initial_constraints = [
    FixedPointConstraint(0, points), # Fix point a
    FixedLengthConstraint(0, 1, ab.length) # Fix length of line ab
]

# Define the additional constraint for State 2 (making line ab vertical)
additional_constraints = [VerticalConstraint(0, 1)]

# Apply the constraints and get the updated positions
updated_points = apply_constraints(initial_constraints + additional_constraints, points)

print(updated_points)

plot_points(points, updated_points)
