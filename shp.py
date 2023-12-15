import geopandas as gpd
import numpy as np
from functions import head_tail_breaks

shp_path = r'D:\HKUST(GZ)\Research\Beautimeter\GZ-Downtown\streets\streets.shp'
output_shp_path = r'D:\HKUST(GZ)\Research\Beautimeter\GZ-Downtown\streets\streets_ht.shp'
att = 'lr'

try:
    gdf = gpd.read_file(shp_path)
    if att not in gdf.columns:
        raise ValueError(f"Attribute '{att}' not found in the data.")

    attribute_values = gdf[att].values

    ht_index, cuts = head_tail_breaks(attribute_values, break_per=0.46)
    print("Cuts:", cuts)

    gdf['ht_class'] = 0
    for i, threshold in enumerate(cuts):
        gdf.loc[gdf[att] > threshold, 'ht_class'] = i + 1

    gdf.to_file(output_shp_path)
    print(f"New Shapefile saved to {output_shp_path}")

except Exception as e:
    print(f"Error: {e}")
