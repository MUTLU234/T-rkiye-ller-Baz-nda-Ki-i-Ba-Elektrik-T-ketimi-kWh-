import geopandas as gpd
import matplotlib.pyplot as plt
import random

# Türkiye'nin şehir sınırlarını içeren GeoJSON dosyasını yükleyin
turkey_map = gpd.read_file('C:/Users/Mutlu/Desktop/Ağ proje klasörü/1.geojson')

# Her şehir için rastgele bir renk oluştur
turkey_map['color'] = turkey_map.apply(lambda x: (random.random(), random.random(), random.random()), axis=1)

# Haritayı çiz
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
turkey_map.plot(ax=ax, color=turkey_map['color'])

plt.title('Türkiye Şehir Haritası')
plt.show()
