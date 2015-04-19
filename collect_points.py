
from matplotlib import pyplot as plt
import numpy as np


###input is a numpy array; plots as image, returns a list of the 
### clicked points 

## usage: foo = collect_points(numpy_array).indices()
##

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



