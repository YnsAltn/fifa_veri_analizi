import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

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

# İlişkili grafik çizdirme
plt.figure(figsize=(30, 20))  # Sayfa boyutunu genişletme
pos = nx.spring_layout(G, k=0.25, iterations=50)

# Düğümleri çizme
nx.draw_networkx_nodes(G, pos, node_size=2500, node_color='lightblue')

# Dairelerin içine etiketleri yazma
node_labels = nx.get_node_attributes(G, 'label')
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8, font_weight='bold', font_family='sans-serif')

# Kenarları çizme
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edges(G, pos, edge_color='gray', width=1.0, alpha=0.7)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.title('2010 Yilina Ait Asamalarin ve Maçlarin Iliskili Grafigi')
plt.axis('off')
plt.show()
