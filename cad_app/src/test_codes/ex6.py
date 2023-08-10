from points import Point
from lines import Line
from constraints import FixedPointConstraint, FixedLengthConstraint, VerticalConstraint, HorizontalConstraint
from optimize import move_point, apply_constraints_and_move
from plot_results import plot_points

# Define the points and lines
a = Point(2, 1)
b = Point(4, 5)
c = Point(6, 2)
points = [a, b, c]
ab = Line(a, b)
bc = Line(b, c)

# Define the initial constraints (State 1)
initial_constraints = [
    FixedPointConstraint(0, points), # Fix point a
    FixedLengthConstraint(0, 1, ab.length), # Fix length of line ab
    FixedLengthConstraint(1, 2, bc.length) # Fix length of line ab
]

# Define the additional constraint for State 2 (making line ab vertical)
additional_constraints = [HorizontalConstraint(0, 1), VerticalConstraint(1, 2)]

# Apply the constraints and get the updated positions
updated_points = apply_constraints_and_move(initial_constraints, additional_constraints, points)

print(updated_points)

plot_points(points, updated_points)
