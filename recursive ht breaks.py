import numpy as np
import rasterio
from osgeo import gdal

image_path = "D:\\Data\\JS&MS\h1\\inside.tif"
output_path = r"D:\Data\JS&MS\h1\inside_htr.tif"

def head_tail_breaks(array, break_per=0.42):
    
    rats, cuts = [], []
    rat_in_head, head_mean, ht_index = 0, 0, 1
    
    array = np.ravel(array)
    idx = np.where(array == -1)
    array = np.delete(array, idx)
    arr = np.copy(array)
    
    while (rat_in_head <= break_per) and (len(array) >1) and np.mean(array) > 0:

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
    if len(cn_list)>2:
        r = arr[arr<cn_list[0]]
    else:
        r = -1
    return ht_index, cn_list, r


with rasterio.open(image_path) as src:

    data = src.read()[0,:,:].astype(np.int32)
    transform = src.transform
    nodata_value = src.nodatavals[0]
    
data[data == nodata_value] = -1

i=1 
c = []
ht = 3
while ht>2:
    if i==1:
        ht, cn_list, r = head_tail_breaks(data)
    else:
        ht, cn_list, r = head_tail_breaks(r)
    i+=1
    c.extend(cn_list)
c = np.sort(np.unique(c))

base = np.zeros(np.shape(data)).astype(np.int8)


for i, m in enumerate(c):
    
    if i==len(c)-1:
        condition = (data >= m)

    else:
        condition = (data >= m) & (data < c[i+1])
    himg = np.where(condition, i+1, 0)
    
    base[himg!=0]=0
    base = base + himg


base[data == -1] = -1

# print(ht)
# 获取数组的行数和列数
rows, cols = base.shape

# 创建TIFF文件
driver = gdal.GetDriverByName("GTiff")
dataset = driver.Create(output_path, cols, rows, 1, gdal.GDT_Int32)

# 将数组写入TIFF文件
dataset.GetRasterBand(1).WriteArray(base)

# 关闭文件
dataset = None

print(f"TIFF文件已保存到 {output_path}")