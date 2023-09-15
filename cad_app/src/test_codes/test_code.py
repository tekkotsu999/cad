from sympy import symbols, Eq, solve

# 各点の座標をシンボルとして定義
x_a, y_a, x_b, y_b, x_c, y_c, x_d, y_d, x_e, y_e = symbols('x_a y_a x_b y_b x_c y_c x_d y_d x_e y_e')

# 点Aと点Bの位置は固定。例として、点Aを(0, 0), 点Bを(3, 4)とします。
a = (0, 0)
b = (3, 4)

# 線ABの長さは固定。この例ではsqrt((3-0)^2 + (4-0)^2) = 5とします。
length_ab = 5

# 点Cが線AB上にある条件。線の方程式を用いる
# 点Cの座標は、(x_a + t*(x_b - x_a), y_a + t*(y_b - y_a))となる（0 <= t <= 1）
t = symbols('t')
equation1 = Eq(x_c, x_a + t * (x_b - x_a))
equation2 = Eq(y_c, y_a + t * (y_b - y_a))

# 線CDが線ABに垂直である条件。
# (y_d - y_c) / (x_d - x_c) * (y_b - y_a) / (x_b - x_a) = -1
equation3 = Eq((y_d - y_c) * (x_b - x_a), -(x_d - x_c) * (y_b - y_a))

# 点Dと点Eが一致する条件。
equation4 = Eq(x_d, x_e)
equation5 = Eq(y_d, y_e)

# 拘束条件による方程式を解く
solution = solve([equation1, equation2, equation3, equation4, equation5],
                 {x_c, y_c, x_d, y_d, x_e, y_e},
                 dict=True,
                 subs={x_a: a[0], y_a: a[1], x_b: b[0], y_b: b[1]})

# 結果を表示
print(f"解は {solution} です。")
