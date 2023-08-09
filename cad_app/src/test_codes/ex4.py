from points import Point
from lines import Line
from constraints import FixedPointConstraint, FixedLengthConstraint, VerticalConstraint
from optimize import move_point, apply_constraints_and_move
import matplotlib.pyplot as plt

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
updated_points = apply_constraints_and_move(b, None, initial_constraints, additional_constraints, points)

print(updated_points)


### 以下、結果のプロット ###
# 初期座標を抽出
initial_x_values = [point.x for point in points]
initial_y_values = [point.y for point in points]

fig, ax = plt.subplots()

# 初期座標をプロット
ax.scatter(initial_x_values, initial_y_values)
ax.plot(initial_x_values, initial_y_values, linestyle='dashed', label='Initial Position')

# 結果の座標を抽出
x_values = [point.x for point in updated_points]
y_values = [point.y for point in updated_points]

# 結果をプロット
ax.scatter(x_values, y_values)
ax.plot(x_values, y_values)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Point Movement')
ax.legend()
ax.grid(True)
ax.set_aspect('equal')
plt.axis('square')

plt.show()