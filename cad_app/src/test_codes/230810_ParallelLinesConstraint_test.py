from points import *
from lines import *
from constraints import *
from optimize import *
from plot_results import *

# Now, let's manually run the test based on the given scenario
a = Point(1, 2)
b = Point(4, 4)
c = Point(3, 1)
d = Point(2, 2)
points = [a, b, c, d]
lines = [Line(a, b), Line(c, d)]

# Define the constraints
constraints = [
    FixedPointConstraint(0, points),  # Fix point a
    FixedPointConstraint(1, points),  # Fix point b
    FixedPointConstraint(2, points),  # Fix point c
    ParallelLinesConstraint(0, 1, 2, 3),  # Make lines ab and cd parallel
    FixedLengthConstraint(2, 3, Line(c,d).length),  # cdの長さは固定
]

# Apply the constraints and get the updated positions
updated_points = apply_constraints(constraints, points)
updated_lines = [Line(updated_points[0], updated_points[1]), Line(updated_points[2], updated_points[3])]

# Plotting the results
plot_points_with_lines(points, updated_points, lines, updated_lines)