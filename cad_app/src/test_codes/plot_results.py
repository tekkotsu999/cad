import matplotlib.pyplot as plt

def plot_points(points, updated_points):
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
    ax.plot(x_values, y_values,label='Updated Position')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Point Movement')
    ax.legend()
    ax.grid(True)
    ax.set_aspect('equal')
    plt.axis('square')

    plt.show()