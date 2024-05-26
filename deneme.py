import pandas as pd
import networkx as nx
from pyvis.network import Network

# Excel dosyasını yükleyin
df = pd.read_excel('veriler5.xlsx')

# Boş bir grafik oluşturma
G = nx.DiGraph()

# Veriyi yıllara göre filtreleyin ve düğümleri oluşturun
for year in df['Yil'].unique():
    year_node_label = f"{year} Yılı"
    G.add_node(year_node_label, label=year_node_label, size=50, font={'size': 25, 'color': 'white'})
    year_matches = df[df['Yil'] == year]

    for stage in year_matches['Asama'].unique():
        stage_matches = year_matches[year_matches['Asama'] == stage]
        stage_node_label = f"{year} - {stage}"
        G.add_node(stage_node_label, label=stage_node_label, size=40, font={'size': 20, 'color': 'white'})
        G.add_edge(year_node_label, stage_node_label, label="Asama", color='blue')

        for index, match in stage_matches.iterrows():
            match_label = f"{match['Ev Sahibi Takim']} vs {match['Deplasman Takim']}: {match['Sonuc']}"
            G.add_node(match_label, label=match_label, size=30, font={'size': 15, 'color': 'white'})
            G.add_edge(stage_node_label, match_label, label="Maç", color='green')

# Pyvis için ağ oluşturma ve grafik boyutunu belirleme
pyvis_graph = Network(height='1000px', width='70%', bgcolor='#222222', font_color='white', directed=True,
                      notebook=True)

# Düğümleri ve kenarları ekleme
for node in G.nodes(data=True):
    pyvis_graph.add_node(node[0], label=node[1]['label'], size=node[1].get('size', 20),
                         font=node[1].get('font', {'size': 12}))

for edge in G.edges(data=True):
    pyvis_graph.add_edge(edge[0], edge[1], title=edge[2]['label'], color=edge[2].get('color', 'gray'))

# Etkileşimli özellikler ve fiziksel algoritma ayarları
pyvis_graph.show_buttons(filter_=['nodes', 'edges', 'physics', 'interaction', 'selection'])
pyvis_graph.set_edge_smooth('dynamic')
pyvis_graph.barnes_hut()

# Görseli HTML dosyasına kaydetme
html_file = 'example.html'
pyvis_graph.show(html_file)

# HTML dosyasını düzenleme
with open(html_file, 'r') as file:
    html_content = file.read()

# Arama kutusu ve butonunu ekranın sol üst köşesine yerleştirme
search_code = """
<div style="position: fixed; top: 20px; left: 20px;">
    <input type="text" id="searchInput" onkeyup="searchNodes()" placeholder="Yıl girin..." title="Arama kutusu">
    <button onclick="searchNodes()" style="background-color: #4CAF50; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;">Ara</button>
</div>
<script>
function searchNodes() {
    var input, filter, li, i, txtValue;
    input = document.getElementById("searchInput");
    filter = input.value.toUpperCase();
    li = document.getElementsByTagName("text");
    for (i = 0; i < li.length; i++) {
        txtValue = li[i].textContent || li[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].parentNode.parentNode.style.display = "";
        } else {
            li[i].parentNode.parentNode.style.display = "none";
        }
    }
}
</script>
"""

# Arama kutusu kodunu HTML içeriğine ekleme
html_content = html_content.replace('</body>', f'{search_code}</body>')

# Filtreleme özelliklerini sağ üst köşeye taşıma
filter_code = """
<div class="vis-configuration-wrapper" style="position: fixed; top: 20px; right: 20px;">
    <!-- Filtreleme özellikleri buraya gelecek -->
</div>
"""

# Filtreleme özelliklerini HTML içeriğine ekleme
html_content = html_content.replace('</body>', f'{filter_code}</body>')

# Güncellenmiş HTML içeriğini kaydetme
with open(html_file, 'w') as file:
    file.write(html_content)
