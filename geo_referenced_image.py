import numpy as np
import rasterio
from osgeo import gdal

image_path = r"D:\HKUST(GZ)\Research\Beautimeter\GZ-Downtown\krigin\v.tif"
output_path = r"D:\HKUST(GZ)\Research\Beautimeter\GZ-Downtown\krigin\v_ht.tif"

def head_tail_breaks(array, break_per=0.4):
    i = 1

    rats, cuts = [], []
    rat_in_head, head_mean, ht_index = 0, 0, 1
    
    base = np.zeros(np.shape(array)).astype(np.int8)
    image = np.copy(array)
    array = np.ravel(array)
    idx = np.where(array == -1)
    array = np.delete(array, idx)
    
    while (rat_in_head <= break_per) and (len(array) >1) and np.mean(array) > 0:
        if i == 1:
            break_per = 0.5
            i+=1
        else: 
            break_per = 0.5
        mean = np.mean(array)
        # print(mean)
        cuts.append(mean)
        
        head_mean = array[array > mean]

        count_total = len(array)
        count_head_mean = len(head_mean)

        rat = count_head_mean / count_total
        rats.append(rat)

        if rat_in_head == 0:
            rat_in_head = rat
        else:
            rat_in_head = np.mean(rats)

        if rat_in_head < break_per:
            ht_index += 1
        array = head_mean

    cn_list = cuts[0:-1]
    print(cn_list)
    del array
    
    for i, m in enumerate(cn_list):
        
        if i==len(cn_list)-1:
            condition = (image >= m)

        else:
            condition = (image >= m) & (image < cn_list[i+1])
        himg = np.where(condition, i+1, 0)
        
        base[himg!=0]=0
        base = base + himg
    
    return ht_index, base


# 使用gdal读取文件
dataset = gdal.Open(image_path)
band = dataset.GetRasterBand(1)
data = band.ReadAsArray()
transform = dataset.GetGeoTransform()
nodata_value = band.GetNoDataValue()

data[data == nodata_value] = -1

ht, htimg = head_tail_breaks(data)

htimg += 1
htimg[data == -1] = -1

# 获取数组的行数和列数
rows, cols = htimg.shape

# 创建TIFF文件
driver = gdal.GetDriverByName("GTiff")
output_dataset = driver.Create(output_path, cols, rows, 1, gdal.GDT_Int32)

# 将数组写入TIFF文件
output_dataset.GetRasterBand(1).WriteArray(htimg)

# 设置输出文件的坐标系统和变换
output_dataset.SetGeoTransform(transform)
output_dataset.SetProjection(dataset.GetProjection())

# 关闭文件
output_dataset = None
dataset = None

print(f"TIFF文件已保存到 {output_path}")