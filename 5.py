import geopandas as gpd
import matplotlib.pyplot as plt
from py2neo import Graph
import pandas as pd
import matplotlib.colors as mcolors

# Neo4j bağlantısı kurun
graph = Graph("bolt://localhost:7687", auth=("neo4j", "23232323"))

# Şehirlerin elektrik tüketimi verilerini çekin
query = """
MATCH (c:City)
RETURN c.name AS name, c.ElectricityConsumption AS electricity_consumption
"""
results = graph.run(query).to_data_frame()

# Şehir adlarını büyük harfe çevirin (eşleşmeyi kolaylaştırmak için)
results['name'] = results['name'].str.upper()

# Türkiye'nin şehir sınırlarını içeren GeoJSON dosyasını yükleyin
turkey_map = gpd.read_file('C:/Users/Mutlu/Desktop/Ağ proje klasörü/1.geojson')

# GeoJSON dosyasındaki şehir adlarını büyük harfe çevirin
turkey_map['name'] = turkey_map['name'].str.upper()

# Verileri GeoDataFrame ile birleştirin
turkey_map = turkey_map.merge(results, how='left', left_on='name', right_on='name')

# Eksik elektrik tüketim verileri için varsayılan bir değer belirleyin (örneğin, 0)
turkey_map['electricity_consumption'] = turkey_map['electricity_consumption'].fillna(0)

# Maviden kırmızıya doğru bir renk skalası belirleyin
cmap = plt.cm.coolwarm  # veya matplotlib.colors.LinearSegmentedColormap kullanabilirsiniz
norm = plt.Normalize(vmin=turkey_map['electricity_consumption'].min(), vmax=turkey_map['electricity_consumption'].max())
turkey_map['color'] = turkey_map['electricity_consumption'].apply(lambda x: cmap(norm(x)))

# Haritayı çiz
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
turkey_map.plot(ax=ax, color=turkey_map['color'])

# Renk skalası çubuğunu ekleyin
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # renk skalasının ayarlanmasını sağlar
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label('Elektrik Tüketimi')

plt.title('Türkiye Şehir Haritası - Elektrik Tüketimi')
plt.show()
