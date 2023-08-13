import matplotlib.pyplot as plt

def plot_points_with_lines(points, updated_points, lines=None, updated_lines=None):
    # Extract initial coordinates
    initial_x_values = [point.x for point in points]
    initial_y_values = [point.y for point in points]

    fig, ax = plt.subplots()

    # Plot initial coordinates
    ax.scatter(initial_x_values, initial_y_values, label='Initial Points')
    if lines:
        for line in lines:
            ax.plot([line.point1.x, line.point2.x], [line.point1.y, line.point2.y], linestyle='dashed', color='blue')

    # Extract result coordinates
    x_values = [point.x for point in updated_points]
    y_values = [point.y for point in updated_points]

    # Plot results
    ax.scatter(x_values, y_values, label='Updated Points')
    if updated_lines:
        for line in updated_lines:
            ax.plot([line.point1.x, line.point2.x], [line.point1.y, line.point2.y], color='red')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Point and Line Movement')
    ax.legend()
    ax.grid(True)
    ax.set_aspect('equal')
    plt.axis('square')

    plt.show()