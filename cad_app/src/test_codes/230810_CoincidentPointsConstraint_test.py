from points import *
from lines import *
from constraints import *
from optimize import *
from plot_results import *

a = Point(1, 2)
b = Point(2, 4)
c = Point(2, 1)
d = Point(4, 1)
points = [a, b, c, d]


ab = Line(a, b)
cd = Line(c, d)
lines = [ab, cd]

# Define the constraints
constraints = [
    FixedPointConstraint(0, points),         # Fix point a
    FixedPointConstraint(2, points),         # Fix point c
    FixedLengthConstraint(0, 1, 1),          # abの長さは2
    FixedLengthConstraint(2, 3, cd.length),  # cdの長さは固定
    CoincidentPointsConstraint(1, 3)  # Make points b and d coincide
]

# Apply the constraints and get the updated positions
updated_points = apply_constraints(constraints, points)
print(updated_points)

updated_lines = [Line(updated_points[0], updated_points[1]), Line(updated_points[2], updated_points[3])]

# Plotting the results
plot_points_with_lines(points, updated_points, lines, updated_lines)