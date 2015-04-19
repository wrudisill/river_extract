import numpy as np
import sys
import matplotlib.pyplot as plt
import os.path
from scipy.ndimage import filters, morphology, measurements




def fill_gaps(image_array):

	rows,cols = image_array.shape
	
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
