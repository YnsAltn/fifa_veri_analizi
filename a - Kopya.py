import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Excel dosyasını oku
df = pd.read_excel('veriler5.xlsx')

# Yıllara göre final maçlarını grupla
final_matches_by_year = df[df['Asama'] == 'Final'].groupby('Yil')

# Boş bir graf oluştur
G = nx.Graph()

# En ortadaki düğüm
central_node = 'Years'

# Her yıl için
for year, matches in final_matches_by_year:
    # Grafı güncelle (Yıl ile final maçları arasında bağlantı oluştur)
    G.add_edge(central_node, year)
    for _, match in matches.iterrows():
        home_team = match['Ev Sahibi Takim']
        away_team = match['Deplasman Takim']
        score = f"{match['Ev Sahibi Skor']} - {match['Deplasman Skor']}"
        G.add_edge(year, (home_team, away_team), score=score)

# Grafı çiz
pos = nx.spring_layout(G)  # Grafı çizmek için pozisyon belirleme

# Düğümleri çizme
nx.draw_networkx_nodes(G, pos, nodelist=[node for node in G.nodes() if node == 'Years'], node_size=2000, node_color='skyblue')
nx.draw_networkx_nodes(G, pos, nodelist=[node for node in G.nodes() if node != 'Years'], node_size=2000, node_color='skyblue')
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

# Kenarları çizme
nx.draw_networkx_edges(G, pos, edge_color='skyblue')
edge_labels = nx.get_edge_attributes(G, 'score')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.title('Yıllara Göre Final Maçları ve Skorları')
plt.axis('off')  # Eksenleri kapat
plt.show()
