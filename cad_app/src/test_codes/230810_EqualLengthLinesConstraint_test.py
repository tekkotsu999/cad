from points import *
from lines import *
from constraints import *
from optimize import *
from plot_results import *

# Now, let's manually run the test based on the given scenario
a = Point(1, 2)
b = Point(2, 4)
c = Point(3, 1)
d = Point(8, 6)
points = [a, b, c, d]

ab = Line(a,b)
bc = Line(b,c)
cd = Line(c,d)

lines = [ab, bc, cd]

# Define the constraints
constraints = [
    FixedPointConstraint(0, points),  # Fix point a
    FixedPointConstraint(3, points),  # Fix point d
    EqualLengthLinesConstraint(0, 1, 1, 2),  # Make lengths of lines ab and bc equal
    EqualLengthLinesConstraint(1, 2, 2, 3),  # Make lengths of lines bc and cd equal
    ParallelLinesConstraint(0, 1, 1, 2),  # Make lines ab and bc parallel
    ParallelLinesConstraint(1, 2, 2, 3),  # Make lines bc and cd parallel
    FixedLengthConstraint(0, 3, Line(a,d).length)
]

# Apply the constraints and get the updated positions
updated_points = apply_constraints(constraints, points)
updated_lines = [
    Line(updated_points[0], updated_points[1]),
    Line(updated_points[1], updated_points[2]),
    Line(updated_points[2], updated_points[3])
]

# Plotting the results
plot_points_with_lines(points, updated_points, lines, updated_lines)