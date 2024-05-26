import pandas as pd
import networkx as nx
from pyvis.network import Network

# Excel tablosunu DataFrame'e yükleme
df = pd.read_excel('veriler5.xlsx')

# Boş bir graf oluşturma
G = nx.DiGraph()

# Yalnızca 2010 yılı için aşamaları ve oynanan maçları dallandırma
year = 2010
year_node_label = f"{year} Yili"
G.add_node(year_node_label, label=year_node_label)
year_matches = df[df['Yil'] == year]
for stage in year_matches['Asama'].unique():
    stage_matches = year_matches[year_matches['Asama'] == stage]
    stage_node_label = f"{year} - {stage}"
    G.add_node(stage_node_label, label=stage_node_label)
    G.add_edge(year_node_label, stage_node_label, label="Asama")
    for index, match in stage_matches.iterrows():
        match_label = f"{match['Ev Sahibi Takim']} vs {match['Deplasman Takim']}: {match['Sonuc']}"
        G.add_node(match_label, label=match_label)
        G.add_edge(stage_node_label, match_label, label="Mac")

# Pyvis için boş bir ağ oluşturma ve grafik boyutunu belirleme
pyvis_graph = Network(height='1000px', width='100%', directed=True, notebook=True)

# Düğümleri ve kenarları ekleyin
for node in G.nodes():
    pyvis_graph.add_node(node, label=node)
for edge in G.edges():
    pyvis_graph.add_edge(edge[0], edge[1], label=G.edges[edge]['label'])

# Görseli görüntüleme
pyvis_graph.show('example.html')
