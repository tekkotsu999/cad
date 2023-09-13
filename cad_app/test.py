# \cad\cad_app> python -m test で実行

from src.shapes import *
from src.constraints import *
from src.plot_results import plot_results

from scipy.optimize import minimize
from copy import deepcopy
import time  # 時間計測用

shape_manager = ShapeManager()
constraint_manager = ConstraintManager()

lines = [ Line(Point(1, 0.8), Point(2, 1)) ]
shape_manager.shapes.extend( lines )
initial_shapes = deepcopy(shape_manager.shapes)

target_point_id = shape_manager.shapes[0].p2.id
target_point = {'x':-0.5, 'y':0.2}

constraint1 = FixedLengthConstraint( lines[0].p1.id, lines[0].p2.id, lines[0].length )
constraint2 = FixedPointConstraint( lines[0].p1.id, lines[0].p1.x, lines[0].p1.y )

constraint_manager.add_constraint(constraint1)
constraint_manager.add_constraint(constraint2)

current_points = shape_manager.get_points()

# 処理開始時間を記録
start_time = time.time()

updated_points = constraint_manager.apply_constraints(current_points, target_point, target_point_id)
shape_manager.update_shapes(updated_points)

# 処理終了時間を記録
end_time = time.time()

# 処理時間を計算
elapsed_time = end_time - start_time

# 処理時間とリクエストIDをログに出力
print(f"Elapsed Time: {elapsed_time} seconds")

plot_results(initial_shapes, shape_manager.shapes)
