import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Excel dosyasını oku
df = pd.read_excel('veriler5.xlsx')

# Yıllara göre ev sahibi ve deplasman takımların attığı gol ortalamalarını hesapla
average_goals_by_year_home = df.groupby('Yil')['Ev Sahibi Skor'].mean()
average_goals_by_year_away = df.groupby('Yil')['Deplasman Skor'].mean()

# Boş bir graf oluştur
G = nx.Graph()

# Merkez düğümü ekleyelim
central_node = 'Years'
G.add_node(central_node, label=central_node)

# Her yıl için ayrı bir düğüm oluştur
for year in df['Yil'].unique():
    # Yıl düğümünü ekleyelim
    G.add_node(year, label=f"{year}")

    # Ev sahibi ve deplasman ortalamalarını ayrı düğümlere ekleyelim
    G.add_node(f"{year} (Home)", label=f"Home Avg: {average_goals_by_year_home.get(year, 0):.2f}")
    G.add_node(f"{year} (Away)", label=f"Away Avg: {average_goals_by_year_away.get(year, 0):.2f}")

    # Merkez düğüm ile yıl düğümleri arasında bağlantılar oluşturalım
    G.add_edge(central_node, year)

    # Yıl düğümü ile ev sahibi ve deplasman düğümleri arasında bağlantılar oluşturalım
    G.add_edge(year, f"{year} (Home)")
    G.add_edge(year, f"{year} (Away)")

# Grafı çiz
pos = nx.spring_layout(G, dim=2)  # Grafı çizmek için pozisyon belirleme, 2 boyutlu

# Düğümleri çizme
nx.draw_networkx_nodes(G, pos, nodelist=[node for node in G.nodes() if "Home" in G.nodes[node]['label']], node_color='green', node_size=2000)
nx.draw_networkx_nodes(G, pos, nodelist=[node for node in G.nodes() if "Away" in G.nodes[node]['label']], node_color='yellow', node_size=2000)
nx.draw_networkx_nodes(G, pos, nodelist=[central_node], node_color='red', node_size=2000)

# Yılları daire içine almak için farklı renklerde düğümleri çizme
for year in df['Yil'].unique():
    nx.draw_networkx_nodes(G, pos, nodelist=[year], node_color='skyblue', node_size=2000)

nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif', labels=nx.get_node_attributes(G, 'label'))

# Kenarları çizme
nx.draw_networkx_edges(G, pos)

plt.title('Yıllara Göre Ev Sahibi ve Deplasman Takımların Attığı Gol Ortalamaları')
plt.axis('off')  # Eksenleri kapat
plt.show()
