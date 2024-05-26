import pandas as pd
import webbrowser
from pyvis.network import Network

# Excel dosyasını oku
veri_yolu = r"veriler5.xlsx"
veriler = pd.read_excel(veri_yolu)

# Sadece belirli bir yıla ait verileri seç
yil = 2010
veriler_yil = veriler[veriler['Yil'] == yil]

# Verileri işle
takimlar = {}
for index, row in veriler_yil.iterrows():
    # Takımları ve maç sonuçlarını işle
    ev_sahibi = row['Ev Sahibi Takim']
    deplasman = row['Deplasman Takim']
    ev_sahibi_skor = row['Ev Sahibi Skor']
    deplasman_skor = row['Deplasman Skor']
    sonuc = row['Sonuc']

    # Ev sahibi takımı işle
    if ev_sahibi not in takimlar:
        takimlar[ev_sahibi] = {'galibiyet': 0, 'beraberlik': 0, 'maglubiyet': 0, 'attigi_gol': 0, 'yedigi_gol': 0}
    if sonuc == 'H':
        takimlar[ev_sahibi]['galibiyet'] += 1
    elif sonuc == 'D':
        takimlar[ev_sahibi]['beraberlik'] += 1
    else:
        takimlar[ev_sahibi]['maglubiyet'] += 1
    takimlar[ev_sahibi]['attigi_gol'] += ev_sahibi_skor
    takimlar[ev_sahibi]['yedigi_gol'] += deplasman_skor

    # Deplasman takımını işle
    if deplasman not in takimlar:
        takimlar[deplasman] = {'galibiyet': 0, 'beraberlik': 0, 'maglubiyet': 0, 'attigi_gol': 0, 'yedigi_gol': 0}
    if sonuc == 'A':
        takimlar[deplasman]['galibiyet'] += 1
    elif sonuc == 'D':
        takimlar[deplasman]['beraberlik'] += 1
    else:
        takimlar[deplasman]['maglubiyet'] += 1
    takimlar[deplasman]['attigi_gol'] += deplasman_skor
    takimlar[deplasman]['yedigi_gol'] += ev_sahibi_skor

# Başarı puanını hesapla
for takim, bilgiler in takimlar.items():
    galibiyet = bilgiler['galibiyet']
    beraberlik = bilgiler['beraberlik']
    maglubiyet = bilgiler['maglubiyet']
    attigi_gol = bilgiler['attigi_gol']
    yedigi_gol = bilgiler['yedigi_gol']

    # Puanlama kriterleri
    puanlama = {
        "galibiyet": 3,
        "beraberlik": 1,
        "maglubiyet": 0,
        "attigi_gol": 0.1,
        "yedigi_gol": -0.1,
    }

    # Puanlamayı hesapla
    puan = (
            galibiyet * puanlama['galibiyet'] +
            beraberlik * puanlama['beraberlik'] +
            maglubiyet * puanlama['maglubiyet'] +
            attigi_gol * puanlama['attigi_gol'] +
            yedigi_gol * puanlama['yedigi_gol']
    )

    takimlar[takim]['puan'] = puan

# Takımları başarı puanına göre sırala
sirali_takimlar = sorted(takimlar.items(), key=lambda x: x[1]['puan'], reverse=True)

# Özel durumlar için ek puanlar
ozel_puanlama = {
    "Eleme Turunu Geçme": 2,
    "Grup Lideri Olarak Çıkma": 1.5,
    "Grup İkincisi Olarak Çıkma": 1,
    "Üçüncü veya Dördüncü Olarak Çıkma": 0.5,
    "Çeyrek Finale Çıkma": 3,
    "Yarı Finale Çıkma": 5,
    "Finalde Yer Alma": 8,
    "Turnuvayı Kazanma": 1.2,
    "Penaltılarla Kazanılan Maç": 1,
    "Uzatma Dakikalarında Kazanılan Maç": 2,
}

# Özel durumları puanlama hesabına ekle
for takim, bilgiler in takimlar.items():
    for durum, ek_puan in ozel_puanlama.items():
        if durum in bilgiler:
            puan = bilgiler['puan']
            puan += bilgiler[durum] * ek_puan
            takimlar[takim]['puan'] = puan

# Ağ oluştur
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

# Düğümleri ekle
for takim, bilgiler in sirali_takimlar:
    puan = bilgiler['puan']
    node_title = f"{takim}: {puan:.2f} puan"  # Düğümün başlığına puanı ekleyin
    net.add_node(takim, label=takim, title=node_title)

# Kenarları ekle
for index, row in veriler_yil.iterrows():
    ev_sahibi = row['Ev Sahibi Takim']
    deplasman = row['Deplasman Takim']
    net.add_edge(ev_sahibi, deplasman)

# Fizik seçenekleri için düğmeleri ekleme
net.show_buttons(filter_=['physics'])

# HTML kodunu ekleyerek ağı gösterme
html_content = net.generate_html()
html_content = html_content.replace(
    '</head>',
    '''
    <style>
        #search-container {
            position: fixed;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 999;
        }
        #search {
            padding: 10px;
        font-size: 16px;
        width: 300px;
        border: 2px solid #ddd;
        border-radius: 5px;
    }
    </style>
    </head>
    '''
)

html_content = html_content.replace(
    '</body>',
    '''
    <div id="search-container">
        <input type="text" id="search" placeholder="Search...">
    </div>
    <script type="text/javascript">
        document.getElementById('search').addEventListener('input', function() {
            var term = this.value.toLowerCase();
            var nodes = network.body.data.nodes;
            nodes.update(nodes.get().map(function(node) {
                if (!node.originalColor) {
                    node.originalColor = node.color;
                    node.originalSize = node.size;
                    node.originalBorderWidth = node.borderWidth;
                }

                if (term && node.label.toLowerCase().includes(term)) {
                    node.color = '#ffff00';  // Aranan terimi içeren düğümleri sarı renkle vurgula
                    node.size = 30;  // Aranan terimi içeren düğümlerin boyutunu artır
                    node.borderWidth = 3;  // Kenarlık genişliği ekle
                    node.borderWidthSelected = 5;  // Seçildiğinde kenarlık genişliği artır
                } else {
                    node.color = node.originalColor;
                    node.size = node.originalSize;  // Diğer düğümleri normal boyuta getir
                    node.borderWidth = node.originalBorderWidth;  // Kenarlık genişliğini normal hale getir
                }
                return node;
            }));
        });

        // Node'ların orijinal renklerini sakla
        network.on('beforeDrawing', function() {
            network.body.data.nodes.get().forEach(function(node) {
                if (!node.originalColor) {
                    node.originalColor = node.color;
                    node.originalSize = node.size;
                    node.originalBorderWidth = node.borderWidth;
                }
            });
        });
    </script>
    </body>
    '''
)

# HTML içeriğini dosyaya yazma
html_file = 'fifa_basarim.html'
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

# Oluşturulan HTML dosyasını gösterme
webbrowser.open(html_file)
