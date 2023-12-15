import numpy as np
from osgeo import gdal

from functions import head_tail_breaks

image_path = "path/to/lr.tif"
output_path = "path/to/lr_ht.tif"

# Open the dataset
try:
    with gdal.Open(image_path) as dataset:
        if dataset is None:
            raise IOError(f"Failed to open image file: {image_path}")

        band = dataset.GetRasterBand(1)
        data = band.ReadAsArray()
        transform = dataset.GetGeoTransform()
        nodata_value = band.GetNoDataValue()

        # Handle NoData values
        if nodata_value is not None:
            data[data == nodata_value] = -1

        # Apply head-tail breaks classification
        ht_index, cuts = head_tail_breaks(data)
        print("Ht-index:%s, Cuts:%s" % (ht_index, cuts))

        htimg = np.full(data.shape, -1, dtype=int)
        for i, threshold in enumerate(cuts):
            htimg[data > threshold] = i + 1

        # Save the result as a new GeoTIFF file
        rows, cols = htimg.shape
        with gdal.GetDriverByName("GTiff").Create(
            output_path, cols, rows, 1, gdal.GDT_Int32
        ) as output_dataset:
            output_dataset.GetRasterBand(1).WriteArray(htimg)
            output_dataset.SetGeoTransform(transform)
            output_dataset.SetProjection(dataset.GetProjection())
            print(f"TIFF file saved to {output_path}")

except Exception as e:
    print(f"An error occurred: {e}")
