import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

veri_seti = pd.read_csv(r"C:\Users\yunus\OneDrive\Masaüstü\enes\movies.csv").head(10)
print(veri_seti.head())

filmler = veri_seti["Series_Title"]
yonetmenler = veri_seti["Director"]
basroller = veri_seti["Star1"]
turler = veri_seti["Genre"]

G = nx.Graph()

for film in filmler:
    G.add_node(film, size=1000, color="yellow")
for yonetmen, basrol, tur_listesi in zip(yonetmenler, basroller, turler):
    G.add_node(yonetmen, color="red")
    G.add_node(basrol, color="blue")
    for tur in tur_listesi.split(","):
        G.add_node(tur.strip(), color="green")

for film, yonetmen, basrol, tur_listesi in zip(filmler, yonetmenler, basroller, turler):
    G.add_edge(film, yonetmen, relationship="Yonetmen", color="red")
    G.add_edge(film, basrol, relationship="Basrol", color="blue")
    for tur in tur_listesi.split(","):
        G.add_edge(film, tur.strip(), relationship="Tur", color="green")


plt.figure(figsize=(15, 10))  # Matplotlib ile tam ekran pencere oluştur

pos = nx.spring_layout(G)
edges = G.edges()
edge_colors = [G[u][v]['color'] for u, v in edges]
node_colors = [G.nodes[node]['color'] for node in G.nodes()]
sizes = [node[1]['size'] if 'size' in node[1] else 600 for node in G.nodes(data=True)]


nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=sizes, alpha=0.7)

nx.draw_networkx_edges(G, pos, edge_color=edge_colors)

nx.draw_networkx_labels(G, pos, font_size=6, font_weight='bold')

plt.axis('off')
plt.tight_layout()  # Grafikleri sıkıştır
plt.show()
