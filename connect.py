import numpy as np
import sys
import matplotlib.pyplot as plt
from ref import write_image, read_image
from skimage import measure
from scipy import stats


##insert a binary image 
def connected_components(image):
	parts,num = measure.label(image, background=0, return_num = True)
	return parts, num


### maybe change this part to work in the event that a least cost image exists 
### and that you want to get connected components from the NDWI without
###having to run the entire code again... still needs a way to get the right 
###index value for for the river...mode would work but it is very slow


#if __name__ == '__main__':
#	lc = read_image('*_LC.tif')
#	NDWI = read_image('*_NDWI.tif')	
#	image_array = np.where(NDWI>0, 1, 0)
#	image_array0 = np.where(image_array+lc != 0, 1, 0)
#	foo = connected_components(image_array0)
#	return fo
