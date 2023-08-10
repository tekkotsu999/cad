from points import Point
from lines import Line
from constraints import *
from optimize import apply_constraints
from plot_results import plot_points

# Define the points and lines
a = Point(2, 1)
b = Point(4, 5)
c = Point(6, 2)
points = [a, b, c]
ab = Line(a, b)
bc = Line(b, c)

# Define the constraints
constraints = [
    FixedPointConstraint(0, points), # Fix point a
    FixedLengthConstraint(0, 1, ab.length), # Fix length of line ab
    FixedLengthConstraint(1, 2, bc.length), # Fix length of line ab
    HorizontalConstraint(0, 1),
    VerticalConstraint(1, 2)
]

# Apply the constraints and get the updated positions
updated_points = apply_constraints(constraints, points)

print(updated_points)

plot_points(points, updated_points)
