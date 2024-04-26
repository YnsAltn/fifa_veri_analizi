import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Excel dosyasını oku
df = pd.read_excel('veriler5.xlsx')

# Yıllara göre ev sahibi ve deplasman takımların attığı gol ortalamalarını hesapla
average_goals_by_year_home = df.groupby('Yil')['Ev Sahibi Skor'].mean()
average_goals_by_year_away = df.groupby('Yil')['Deplasman Skor'].mean()

# Ortalama gol değerlerini diziye ata
average_goals_home = list(average_goals_by_year_home.values)
average_goals_away = list(average_goals_by_year_away.values)

# Renk skalası
colors_home = plt.cm.viridis(np.linspace(0, 1, len(average_goals_home)*2))
colors_away = plt.cm.viridis(np.linspace(0, 1, len(average_goals_away)*2))

# Boş bir graf oluştur
G = nx.Graph()

# En ortadaki düğüm
central_node = 'Years'

# Her yıl için ev sahibi takım
for idx, (year, avg_home_goals) in enumerate(average_goals_by_year_home.items()):
    # Grafı güncelle (Merkez düğüm ile yıl arasında bağlantı oluştur)
    G.add_edge(central_node, year)
    G.nodes[year]['label'] = f"{year} (Home Goals: {avg_home_goals:.2f})"

# Her yıl için deplasman takım
for idx, (year, avg_away_goals) in enumerate(average_goals_by_year_away.items()):
    # Grafı güncelle (Yıl ile deplasman takım arasında bağlantı oluştur)
    G.add_edge(year, f"{year} (Away)")
    G.nodes[f"{year} (Away)"]['label'] = f"{year} (Away Goals: {avg_away_goals:.2f})"

# Grafı çiz
pos = nx.spring_layout(G)  # Grafı çizmek için pozisyon belirleme

# Düğümleri çizme
nx.draw_networkx_nodes(G, pos, nodelist=[node for node in G.nodes() if node != central_node], node_color=colors_home, node_size=2000)
nx.draw_networkx_nodes(G, pos, nodelist=[central_node], node_color='red', node_size=2000)
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif', labels=nx.get_node_attributes(G, 'label'))

# Kenarları çizme
nx.draw_networkx_edges(G, pos)

plt.title('Yıllara Göre Ev Sahibi ve Deplasman Takımların Attığı Gol Ortalamaları')
plt.axis('off')  # Eksenleri kapat
plt.show()
