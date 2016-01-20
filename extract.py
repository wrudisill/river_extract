import numpy as np
import sys
import matplotlib.pyplot as plt
import os.path
from pylab import *
from functions import *


#### checks if an NDWI tif already exists in folder
#### if not, it creates one. image_array not scaled

# or other folder name 
folder = 'LC80520182013258LGN00' 

if os.path.exists(folder+'/'+folder+'_NDWI.tif'):
	image_array = read_image(folder+'/'+folder+'_NDWI.tif')	

else:
	image_array, cols, rows = water_mask(folder)
	write_image(image_array, cols, rows, folder+'/'+folder+'_NDWI')
	print 'created'+folder+'folder'+fo

##removes values below zero, scale between 0 and 10
image_array = np.where(image_array>0, image_array, 0)
image_array0 = ((image_array-amin(image_array))/(amax(image_array)-amin(image_array))*10)
###

##fill in gaps; gap pixels given 10 cost
fill = fill_gaps(image_array0)
image_array0 = image_array0 + fill



###collect points for least cost path
# points = collect_points(simple_case).indices()

points = collect_points(image_array0).indices()
points = np.array(points)
print points


###start and end points for the least_cost alogorithm
start = points[0:len(points)-1]
end = np.tile(points[len(points)-1],(len(points)-1,1))

# ####holds values for cost path function, total collects cost
im = np.zeros_like(image_array0)
total = 0

# im = np.zeros_like(simple_case)



# ### for calculating cost_array

background = np.where(image_array0==0, 10000, 0)
negative = np.where(image_array0>0, 10-image_array0, 0)


# #### does cost path calculation
for t in range(2):
	background = background - im 
	negative = negative + im 
	cost_array = np.where(negative !=0, negative, background)
# cost_array = simple_case 

	for i in range(len(points)-1):
		# path, cost = least_cost(cost_array, points[i], points[i+1])
		path, cost = least_cost(cost_array, start[i], end[i])
		im = np.where(im + path != 0, 1, 0)
		total = cost + total
		# print t


###create a tiff
rows,cols = image_array.shape
write_image(im,rows,cols,folder+'/'+folder+'_LC')
#####

# print total




