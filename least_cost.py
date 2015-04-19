import gdal
from gdalconst import *
import numpy as np
import matplotlib.pyplot as plt
import sys
from skimage.graph import route_through_array

def least_cost(image, start, end):
	
	indices, cost = route_through_array(image, start, end)
	indices = np.array(indices).T
	path = np.zeros_like(image)
	path[indices[0], indices[1]] = 1
	return path, cost

if __name__ == '__main__':
	least_cost(sys.argv[1],sys.argv[2],sys.argv[3])





