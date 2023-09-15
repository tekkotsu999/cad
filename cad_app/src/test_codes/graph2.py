import networkx as nx
import matplotlib.pyplot as plt

# グラフの初期化
G = nx.Graph()

# 各点と各線をノードで定義
# 初期の自由度は2とする（2次元座標なので）
G.add_nodes_from([
    ('a', {'type': 'point', 'freedom': 2}),
    ('b', {'type': 'point', 'freedom': 2}),
    ('c', {'type': 'point', 'freedom': 2}),
    ('d', {'type': 'point', 'freedom': 2}),
    ('ab', {'type': 'line', 'freedom': 2}),
    ('cd', {'type': 'line', 'freedom': 2})])

# 拘束条件をエッジで定義
G.add_edges_from([
    ('a', 'ab', {'constraint': 'on_line'}),
    ('b', 'ab', {'constraint': 'on_line'}),
    ('c', 'cd', {'constraint': 'on_line'}),
    ('d', 'cd', {'constraint': 'on_line'}),
    ('c', 'ab', {'constraint': 'on_line'}),
    ('ab', 'cd', {'constraint': 'perpendicular'})
])

# 位置固定拘束を適用
fixed_points = ['a', 'b', 'd']
for point in fixed_points:
    G.nodes[point]['freedom'] = 0

# 自由度の計算（深さ優先探索）
def dfs(node):
    for neighbor, edge_data in G[node].items():
        if G.nodes[neighbor]['freedom'] > 0:
            G.nodes[neighbor]['freedom'] -= 1
            if G.nodes[neighbor]['freedom'] == 0:
                dfs(neighbor)

# 自由度が0の点から探索を開始
for point in fixed_points:
    dfs(point)

# 結果の出力
for node, data in G.nodes(data=True):
    print(f"Node: {node}, Type: {data['type']}, Freedom: {data['freedom']}")

# 座標を自動で生成
pos = nx.spring_layout(G, seed=42)

shapes = {'point': 'o', 'line': 's'}
node_shapes = {'o': [], 's': []}

# ノードのラベルと色を設定
labels = {}

# エッジのラベルを設定
edge_labels = nx.get_edge_attributes(G, 'constraint')

# ノードの色を設定
node_colors = {}

# ノードの枠線の色を設定
node_edge_colors = {}

for node, data in G.nodes(data=True):
    # ノードのラベル
    label = node
    labels[node] = f"{label}\n({data['freedom']})"

    # ノードの種類によって、形状を変更
    node_shapes[shapes[data['type']]].append(node)

    # fixedされた点なら赤く赤く縁取る
    if node in fixed_points:
        node_edge_colors[node] = 'red'
    else:
        node_edge_colors[node] = 'white'

    # 自由度が0なら、グレー
    if data['freedom'] == 0:
        node_colors[node] = 'gray'
    else:
        node_colors[node] = '#1E90FF'


# グラフを描画
for shape, nodes in node_shapes.items():
    nx.draw_networkx_nodes(G, pos, nodelist=nodes, 
                           node_color=[node_colors[node] for node in nodes], 
                           edgecolors=[node_edge_colors[node] for node in nodes], 
                           linewidths=1.5,  # 枠線の太さ
                           node_shape=shape)


nx.draw_networkx_labels(G, pos, labels=labels)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()
