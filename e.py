import pandas as pd
import numpy as np
from pyvis.network import Network

# Excel dosyasını oku
df = pd.read_excel('veriler5.xlsx')

# Yıllara göre ev sahibi ve deplasman takımların attığı gol ortalamalarını hesapla
average_goals_by_year_home = df.groupby('Yil')['Ev Sahibi Skor'].mean()
average_goals_by_year_away = df.groupby('Yil')['Deplasman Skor'].mean()

# Boş bir graf oluştur
pyvis_graph = Network(height='800px', width='100%', directed=True, notebook=True)

# Merkezi düğümü oluştur
pyvis_graph.add_node('Yıllar', label='Yıllar')

# Her yıl için ayrı bir düğüm oluştur ve ev sahibi takım ile bağlantı oluştur
for year, avg_home_goals in average_goals_by_year_home.items():
    # Her yıl düğümü
    pyvis_graph.add_node(year, label=f"{year}")
    # Ev sahibi skor düğümü ve bağlantı
    pyvis_graph.add_node(f"{year}_home", label=f"Ev Sahibi Ortalama Gol: {avg_home_goals:.2f}")
    pyvis_graph.add_edge('Yıllar', year)
    pyvis_graph.add_edge(year, f"{year}_home")

# Her yıl için deplasman takımı ile bağlantı oluştur
for year, avg_away_goals in average_goals_by_year_away.items():
    # Deplasman skor düğümü ve bağlantı
    pyvis_graph.add_node(f"{year}_away", label=f"Deplasman Ortalama Gol: {avg_away_goals:.2f}")
    pyvis_graph.add_edge(year, f"{year}_away")

# Görseli görüntüleme
pyvis_graph.show('example.html')
