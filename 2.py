import geopandas as gpd
import matplotlib.pyplot as plt
import random
from py2neo import Graph
import pandas as pd

# Neo4j bağlantısı kurun
graph = Graph("bolt://localhost:7687", auth=("neo4j", "23232323"))

# Şehirlerin elektrik tüketimi verilerini çekin
query = """
MATCH (c:City)
RETURN c.name AS name, c.ElectricityConsumption AS electricity_consumption
"""
results = graph.run(query).to_data_frame()

# Türkiye'nin şehir sınırlarını içeren GeoJSON dosyasını yükleyin
turkey_map = gpd.read_file('C:/Users/Mutlu/Desktop/Ağ proje klasörü/1.geojson')

# Verileri GeoDataFrame ile birleştirin
turkey_map = turkey_map.merge(results, left_on='name', right_on='name')

# Renk skalasını belirleyin (örneğin, elektrik tüketimine göre)
cmap = plt.cm.viridis  # veya başka bir renk skalası kullanabilirsiniz
norm = plt.Normalize(vmin=turkey_map['electricity_consumption'].min(), vmax=turkey_map['electricity_consumption'].max())
turkey_map['color'] = turkey_map['electricity_consumption'].apply(lambda x: cmap(norm(x)))

# Haritayı çiz
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
turkey_map.plot(ax=ax, color=turkey_map['color'])

plt.title('Türkiye Şehir Haritası - Elektrik Tüketimi')
plt.show()
