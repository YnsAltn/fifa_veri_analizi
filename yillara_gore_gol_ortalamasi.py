import pandas as pd
import networkx as nx
import numpy as np
from pyvis.network import Network

# Excel dosyasını oku
df = pd.read_excel('veriler5.xlsx')

# Yıllara göre ev sahibi ve deplasman takımların attığı gol ortalamalarını hesapla
average_goals_by_year_home = df.groupby('Yil')['Ev Sahibi Skor'].mean()
average_goals_by_year_away = df.groupby('Yil')['Deplasman Skor'].mean()

# Ev sahibi ve deplasman gol ortalamalarını birleştir ve aralıkları belirle
all_goals = list(average_goals_by_year_home) + list(average_goals_by_year_away)
min_goal, max_goal = min(all_goals), max(all_goals)
intervals = np.linspace(min_goal, max_goal, 5)

# Aralıkları yazdır
print(f"Aralıklar: {intervals}")

# Renk skalası
colors = ['#d7191c', '#fdae61', '#abdda4', '#2b83ba']


def get_color(value):
    for i in range(4):
        if intervals[i] <= value < intervals[i + 1]:
            return colors[i]
    return colors[-1]  # En büyük değeri son renkle eşleştir


# Boş bir graf oluştur
G = nx.Graph()

# En ortadaki düğüm
central_node = 'Years'
G.add_node(central_node, label=central_node, color='red')

# Her yıl için ev sahibi ve deplasman takım düğümlerini ekle
for year in average_goals_by_year_home.index:
    # Yıl düğümünü ekle
    G.add_node(year, label=f"{year}", color='blue')
    G.add_edge(central_node, year, color='black')

    # Ev sahibi takım düğümü
    avg_home_goals = average_goals_by_year_home[year]
    home_node = f"{year} (Home)"
    G.add_node(home_node, label=f"{year} (Home Goals: {avg_home_goals:.2f})", color=get_color(avg_home_goals))
    G.add_edge(year, home_node, color='black')

    # Deplasman takım düğümü
    avg_away_goals = average_goals_by_year_away[year]
    away_node = f"{year} (Away)"
    G.add_node(away_node, label=f"{year} (Away Goals: {avg_away_goals:.2f})", color=get_color(avg_away_goals))
    G.add_edge(year, away_node, color='black')

# Pyvis için ağ oluşturma
net = Network(height='1000px', width='100%', directed=False, notebook=True)

# Düğümleri ve kenarları ekle
for node, data in G.nodes(data=True):
    net.add_node(node, label=data['label'], color=data['color'])

for source, target, data in G.edges(data=True):
    net.add_edge(source, target, color=data['color'])

# HTML dosyasını kaydet ve göster
net.show('yillara_gore_gol_ortalaması.html')
