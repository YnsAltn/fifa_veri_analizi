import pandas as pd
from pyvis.network import Network

# Veri setini oku
df = pd.read_excel('veriler5.xlsx')

# Kazanan ve kaybeden takımları birleştir
takimlar = pd.concat([df['Kazanan Takim'], df['Kaybeden Takim']]).unique()

# Her tur için puanlama sistemi
puanlama_sistemi = {
    'Group 1': 10,
    'Group 2': 20,
    'Group 3': 30,
    'Group 4': 40,
    'Round of 16': 50,
    'Quarterfinals': 60,
    'Semifinals': 70,
    'Third place': 80,
    'Final': 100
}

# Her takım için kazandığı tur sayısına göre puan hesapla
takim_skorlari = {}
for takim in takimlar:
    takim_filtre = (df['Kazanan Takim'] == takim) | (df['Kaybeden Takim'] == takim)
    filtered_df = df[takim_filtre].copy()  # SettingWithCopyWarning uyarısını önlemek için kopya oluştur
    filtered_df.loc[:, 'Puanlama'] = filtered_df['Asama'].map(puanlama_sistemi)
    tur_atlama_sayisi = filtered_df.groupby('Yil').size()
    takim_skorlari[takim] = tur_atlama_sayisi * 10

# Tüm yıllar için takım puanlarını topla ve yıl sayısına böl
genel_skorlar = pd.DataFrame(takim_skorlari).mean(axis=1)

# Network grafiği oluştur
nt = Network()

# Düğümleri ekle
for node, score in genel_skorlar.items():
    if isinstance(node, str):  # Node bir string ise düğümü ekle
        nt.add_node(node.lower(), value=score)  # Tüm harfleri küçük harfe dönüştür

# Bağlantıları ekle
for index, row in df.iterrows():
    kazanan = row['Kazanan Takim'].strip().lower()
    kaybeden = row['Kaybeden Takim'].strip().lower()

    if kazanan not in nt.get_nodes():
        nt.add_node(kazanan)

    if kaybeden not in nt.get_nodes():
        nt.add_node(kaybeden)

    nt.add_edge(kazanan, kaybeden)

# Görselleştirmeyi HTML olarak kaydet
nt.show('network.html')
