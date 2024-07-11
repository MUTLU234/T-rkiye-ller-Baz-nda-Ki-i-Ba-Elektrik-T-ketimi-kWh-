import geopandas as gpd
import matplotlib.pyplot as plt
from py2neo import Graph
import pandas as pd
import matplotlib.colors as mcolors

# Neo4j bağlantısı kurma kısmı
graph = Graph("bolt://localhost:7687", auth=("neo4j", "23232323"))

# Şehirlerin elektrik tüketimi verilerini neo4j den çekme kısmı.
query = """
MATCH (c:City)
RETURN c.name AS name, c.ElectricityConsumption AS electricity_consumption
"""
results = graph.run(query).to_data_frame()

# Şehir adlarını büyük harfe çevirin (eşleşmeyi kolaylaştırmak için ve küçük büyük harf duyarlılığının önüne geçmiş olduk hepsi aynı formatta olacak..!!!)
results['name'] = results['name'].str.upper()

# Türkiye'nin şehir sınırlarını içeren GeoJSON dosyasını yükleme kısmı(geojson dosyasını internetten bulabilirsiniz linkler kaynakçamda mevcut.)
turkey_map = gpd.read_file('C:/Users/Mutlu/Desktop/Ağ proje klasörü/1.geojson')

# GeoJSON dosyasındaki şehir adlarını büyük harfe çevirdim(çünkü geojson ve neo4j deki şehir isimleri eşleştirmek için büyük küçük harf duyarlılığını kaldırmak istedim.)
turkey_map['name'] = turkey_map['name'].str.upper()

# Verileri GeoDataFrame ile birleştirme kısmı( isimler aynı olanların veri eşleştirildi.)
turkey_map = turkey_map.merge(results, how='left', left_on='name', right_on='name')

# Eksik elektrik tüketim verileri için varsayılan bir değer belirleme (örneğin 0 çünkü eğer değer vermezsek ve veride eksik bir değer olursa kod hatalı çalışır ve optimize sonuç alınmaz.)
turkey_map['electricity_consumption'] = turkey_map['electricity_consumption'].fillna(0)

# Maviden kırmızıya doğru bir renk skalası belirleme kısmı.
cmap = plt.cm.winter  # veya matplotlib.colors.LinearSegmentedColormap kullanabilir.
norm = plt.Normalize(vmin=turkey_map['electricity_consumption'].min(), vmax=turkey_map['electricity_consumption'].max())
turkey_map['color'] = turkey_map['electricity_consumption'].apply(lambda x: cmap(norm(x)))

# Haritayı çizdirme kodum.
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
turkey_map.plot(ax=ax, color=turkey_map['color'])

# Her şehrin üzerine isimlerini yazdırma (baş harfi büyük olacak şekilde düzenledim haritada görünecek kısım bu olacak)
for idx, row in turkey_map.iterrows():
    city_name = row['name'].capitalize()  # Sadece baş harfi büyük yapma kısmı.
    plt.annotate(text=city_name, xy=(row['geometry'].centroid.x, row['geometry'].centroid.y), color='Black', fontsize=7, ha='center')

# Renk skalası çubuğunu ekledim, burdaki amaç kwh cinsinden renklerin hangi değere denk geldiğinin anlaşılmasıdır.
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # renk skalasının ayarlanmasını sağlar.
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label('Elektrik Tüketimi')

plt.title('Türkiye Haritası - Şehirler Bazında Bireysel Elektrik Tüketimi')
plt.show()
