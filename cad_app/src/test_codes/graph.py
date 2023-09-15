import networkx as nx
import matplotlib.pyplot as plt

# 自由度を更新する関数
def update_freedom(node, G):
    # 点の場合
    if G.nodes[node].get('type', '') == 'point':
        freedom = G.nodes[node].get('freedom', 2)  # 初期自由度は通常2
        for neighbor, edge_attr in G[node].items():
            constraint = edge_attr.get('constraint', None)
            # 拘束条件に応じて自由度を更新
            if constraint == 'fixed':
                freedom = 0
            elif constraint == 'on_line':
                freedom = min(freedom, 1)
            # その他の拘束条件もここで処理できます
        G.nodes[node]['freedom'] = freedom
    # 線の場合
    elif G.nodes[node].get('type', '') == 'line':
        end_points = [n for n, attr in G[node].items() if attr.get('constraint', '') != 'perpendicular']
        freedom = min([G.nodes[p].get('freedom', 2) for p in end_points])
        G.nodes[node]['freedom'] = freedom


# グラフを作成
G = nx.Graph()
G.add_nodes_from([('a', {'type': 'point'}),
                  ('b', {'type': 'point'}),
                  ('c', {'type': 'point'}),
                  ('d', {'type': 'point'}),
                  ('ab', {'type': 'line'}),
                  ('cd', {'type': 'line'})])

G.add_edges_from([('a', 'ab', {'constraint': 'fixed'}),
                  ('b', 'ab', {'constraint': 'fixed'}),
                  ('c', 'ab', {'constraint': 'on_line'}),
                  ('ab', 'cd', {'constraint': 'perpendicular'}),
                  ('d', 'cd', {'constraint': 'fixed'})])

# 自動で自由度を更新
for node in G.nodes():
    update_freedom(node, G)

# 自由度を出力
for node, attr in G.nodes(data=True):
    print(f"{node}の自由度: {attr.get('freedom', 'N/A')}")

# 座標を自動で生成
pos = nx.spring_layout(G, seed=42)

f_labels = nx.get_node_attributes(G, 'freedom')
f_labels = {k: f"{k}\n({v})" for k, v in f_labels.items()}

c_labels = nx.get_edge_attributes(G, 'constraint')
nx.draw_networkx_edge_labels(G, pos, edge_labels=c_labels)


nx.draw(G, pos, with_labels=True,labels=f_labels)
plt.show()