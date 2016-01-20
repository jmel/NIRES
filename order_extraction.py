#!/usr/bin/env python
# showing the orders by using the edge detection algorithm

import cv2
import numpy as np
#from matplotlib import pyplot as plt
from astropy.io import fits


continuum_image = fits.open('s151112_a000025.fits')
continuum_data = continuum_image[0].data
continuum_copy = np.uint8(continuum_data)
edges = cv2.Canny(continuum_copy,27,100)

##own code for order determination

for i in range(1, 1024):
    for j in range(1, 2048):
        if i > 385:
           if continuum_data[i][j] > 45:
              continuum_data[i][j] = 1
           else:
              continuum_data[i][j] = 0
        else:
           if continuum_data[i][j] > 14:
              continuum_data[i][j] = 1
           else:
              continuum_data[i][j] = 0

#hdu = fits.PrimaryHDU(edges)
#hdulist = fits.HDUList([hdu])
#hdulist.writeto('order-bright.fits')

hdu = fits.PrimaryHDU(continuum_data)
hdulist = fits.HDUList([hdu])
hdulist.writeto('order-bright1.fits')
