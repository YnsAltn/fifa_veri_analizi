import pandas as pd
from pyvis.network import Network

# Excel tablosunu DataFrame'e yükleme
df = pd.read_excel('veriler5.xlsx')

# Boş bir ağ oluşturma
pyvis_graph = Network(height='1000px', width='100%', directed=True, notebook=True)

# Yalnızca 2010 yılı için aşamaları ve oynanan maçları dallandırma
year = 2010
year_node_label = f"{year} Yili"
pyvis_graph.add_node(year_node_label, label=year_node_label, color='blue')
year_matches = df[df['Yil'] == year]
for stage in year_matches['Asama'].unique():
    stage_matches = year_matches[year_matches['Asama'] == stage]
    stage_node_label = f"{year} - {stage}"
    pyvis_graph.add_node(stage_node_label, label=stage_node_label, color='green')
    pyvis_graph.add_edge(year_node_label, stage_node_label, label="Asama", color='black')
    for index, match in stage_matches.iterrows():
        match_label = f"{match['Ev Sahibi Takim']} vs {match['Deplasman Takim']}: {match['Sonuc']}"
        match_info = (f"<b>Şehir:</b> {match['Sehir']}<br>"
                      f"<b>Tarih:</b> {match['Tarih']}<br>"
                      f"<b>Ev Sahibi Skor:</b> {match['Ev Sahibi Skor']}<br>"
                      f"<b>Deplasman Skor:</b> {match['Deplasman Skor']}<br>"
                      f"<b>Kazanma Koşulları:</b> {match['Kazanma Kosullari']}<br>"
                      f"<b>Kazanan Takım:</b> {match['Kazanan Takim']}<br>"
                      f"<b>Kaybeden Takım:</b> {match['Kaybeden Takim']}")
        pyvis_graph.add_node(match_label, label=match_label, color='orange', title=match_info)
        pyvis_graph.add_edge(stage_node_label, match_label, label="Mac", color='gray')

import json

# Pyvis'ten alınan düğüm ve kenar verilerini JSON formatına dönüştürme
pyvis_nodes_json = json.dumps(pyvis_graph.nodes)
pyvis_edges_json = json.dumps(pyvis_graph.edges)

# HTML dosyasının içeriğini oluşturma
html_content = f'''
<!doctype html>
<html>
<head>
  <title>Football Matches</title>
  <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet" type="text/css" />
  <style>
    body, html {{
      height: 100%;
      margin: 0;
      padding: 0;
    }}
    #mynetwork {{
      width: 100%;
      height: 100%;
    }}
  </style>
</head>
<body>
<div id="mynetwork"></div>
<script type="text/javascript">
  var nodes = new vis.DataSet({pyvis_nodes_json});
  var edges = new vis.DataSet({pyvis_edges_json});

  var container = document.getElementById('mynetwork');
  var data = {{
    nodes: nodes,
    edges: edges
  }};
  var options = {{}};
  var network = new vis.Network(container, data, options);

  network.on("click", function (params) {{
    if (params.nodes.length > 0) {{
      var nodeId = params.nodes[0];
      var node = nodes.get(nodeId);
      if (node.title) {{
        var infoBox = document.createElement("div");
        infoBox.innerHTML = node.title;
        infoBox.style.position = "absolute";
        infoBox.style.left = params.pointer.DOM.x + 'px';
        infoBox.style.top = params.pointer.DOM.y + 'px';
        infoBox.style.background = "white";
        infoBox.style.border = "1px solid black";
        document.body.appendChild(infoBox);
        setTimeout(function () {{
          infoBox.parentNode.removeChild(infoBox);
        }}, 5000);
      }}
    }}
  }});
</script>
</body>
</html>
'''

# HTML dosyasını oluşturma ve içeriği yazma
with open('football_matches.html', 'w') as file:
    file.write(html_content)

print("HTML dosyası oluşturuldu: football_matches.html")
