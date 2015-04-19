import gdal
from gdalconst import *
import numpy as np
import sys

##writes a numpy array to a tif; not referenced. 

def write_image(data, out_name):
	rows,cols = data.shape
	format = "GTiff"
	driver = gdal.GetDriverByName(format)
	outDataset = driver.Create(str(out_name)+'.tif', rows, cols, 1, GDT_Float32)
	outBand = outDataset.GetRasterBand(1)
	outBand.WriteArray(data, 0, 0) ###data being written goes here
	outBand.SetNoDataValue(0)
	outBand.FlushCache()
	outBand.GetStatistics(0, 1)


## reads an entire TIF, puts it into a numpy array. could easily change to read in certain pixels
## defined by offset from top left corner. see docs. 

def read_image(image):
	ds= gdal.Open(image, GA_ReadOnly)
	band = ds.GetRasterBand(1)
	cols = ds.RasterXSize
	rows = ds.RasterYSize
	data =  band.ReadAsArray(0, 0, cols, rows).astype(np.float)
	return data









# stats = outBand.GetStatistics(0, 1)
	# # georef, set proj
	# outDataset.SetGeoTransform(ds.GetGeoTransform())
	# outDataset.SetProjection(ds.GetProjection())
	# # build pyramids
	# gdal.SetConfigOption('HFA_USE_RRD', 'YES')
	# outDataset.BuildOverviews(overviewlist=[2,4,8,16,32,64,128])
