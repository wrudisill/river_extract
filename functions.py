import numpy as np
import sys
import matplotlib.pyplot as plt
import gdal 
from gdalconst import * 
from scipy.ndimage import filters, morphology, measurements
from skimage import measure
from skimage.graph import route_through_array

def water_mask(filename):
	ds5 = gdal.Open(str(filename) +'/'+ str(filename)+'_B5.TIF', GA_ReadOnly)
	ds3 = gdal.Open(str(filename) +'/'+ str(filename)+'_B3.TIF', GA_ReadOnly)
	cols = ds5.RasterXSize
	rows = ds5.RasterYSize
	band3 = ds3.GetRasterBand(1)
	band5 = ds5.GetRasterBand(1)
	b3= band3.ReadAsArray(0, 0, cols, rows).astype(np.float)
	b5= band5.ReadAsArray(0, 0, cols, rows).astype(np.float)
	im = np.zeros((rows,cols))
	foo = np.where((b3+b5==0), 0, (b3-b5)/(b3+b5+0.00000000001))
	return foo, cols, rows



class collect_points():
    omega = []
    def __init__(self,array):
        self.array = array
        #self.omega = array??
    def onclick(self,event):
        # print 'xdata=%f, ydata=%f'%(
        #     int(round(event.xdata)),   int(round(event.ydata)))
        self.omega.append((int(round(event.ydata)), int(round(event.xdata))))
    def indices(self):
        plot = plt.imshow(self.array, cmap = plt.cm.hot, interpolation = 'nearest', origin= 'upper')
        fig = plt.gcf()
        ax = plt.gca()
        zeta = fig.canvas.mpl_connect('button_press_event', self.onclick)
        plt.colorbar()
        plt.show()
        return self.omega


def least_cost(image, start, end):
	
	indices, cost = route_through_array(image, start, end)
	indices = np.array(indices).T
	path = np.zeros_like(image)
	path[indices[0], indices[1]] = 1
	return path, cost



def fill_gaps(image_array):

	shape = image_array.shape
	#returns tuple of row,col
	rows = shape[0]
	cols = shape[1]

	im = np.zeros((rows,cols))

	### arrays of filling elements
	f1 = np.array([[0,1,0],[0,0,0],[0,1,0]])
	f2 = np.array([[0,0,0],[1,0,1],[0,0,0]])
	f3 = np.array([[1,0,0],[0,0,0],[0,0,1]])
	f4 = np.array([[0,0,1],[0,0,0],[1,0,0]])
	fill_kern = [f1,f2,f3,f4]

	print 'filling gaps...'
	
	for r in range(4):
		#find gaps, fill
		zed = morphology.binary_hit_or_miss(np.where(image_array + im != 0,1,0), structure1=fill_kern[r]) 
		im = im + zed 
		print r
	return im 


####NDWI image_array###
def spatial_filter(skeleton,image_array,loops,iterations):
	# image_array = np.where(image_array > threshold, 1, 0)
	im = np.zeros_like(image_array)
	s = morphology.generate_binary_structure(2,2)
	for i in range(loops):
		print i
		grow = morphology.binary_dilation(skeleton+im, iterations = iterations, structure = s)
		im = np.where(grow !=0, image_array , 0)
	return im


##insert a binary image 
def connected_components(image):
	parts,num = measure.label(image, background=0, return_num = True)
	return parts, num




def write_image(data, out_name):
	rows,cols = data.shape
	format = "GTiff"
	driver = gdal.GetDriverByName(format)
	outDataset = driver.Create(str(out_name)+'.tif', cols, rows, 1, GDT_Float32)
	outBand = outDataset.GetRasterBand(1)
	outBand.WriteArray(data, 0, 0) ###data being written goes here
	outBand.SetNoDataValue(0)
	outBand.FlushCache()
	outBand.GetStatistics(0, 1)


## reads an entire TIF. 

def read_image(image):
	ds= gdal.Open(image, GA_ReadOnly)
	band = ds.GetRasterBand(1)
	cols = ds.RasterXSize
	rows = ds.RasterYSize
	data =  band.ReadAsArray(0, 0, cols, rows).astype(np.float)
	return data


