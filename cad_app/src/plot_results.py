import matplotlib.pyplot as plt
from .shapes import *


def plot_results(initial_shapes, current_shapes):
    fig, ax = plt.subplots()

    # 過去のshapesを描画
    for shape in initial_shapes:
        if isinstance(shape, Point):
            ax.scatter(shape.x, shape.y, color='blue', label='Initial Point')
        elif isinstance(shape, Line):
            ax.plot([shape.p1.x, shape.p2.x], [shape.p1.y, shape.p2.y], linestyle='dashed', color='blue', label='Initial Line')

    # 現在のshapesを描画
    for shape in current_shapes:
        if isinstance(shape, Point):
            ax.scatter(shape.x, shape.y, color='red', label='Current Point')
        elif isinstance(shape, Line):
            ax.plot([shape.p1.x, shape.p2.x], [shape.p1.y, shape.p2.y], color='red', label='Current Line')


    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Point and Line Movement')
    ax.legend()
    ax.grid(True)
    ax.set_aspect('equal')
    plt.axis('square')

    plt.show()