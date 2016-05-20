#!/usr/bin/env python
# removing the noise

import sys
import ds9
import imDisplay as imD
import numpy as np
from astropy.io import fits
import globals

##image dimensions
row = 1024
col = 2048

### No.of lines to be average over
n = 16


name=imD.nameResolve(sys.argv[1],'s*')
noise_image = fits.open(name)


noise_data = noise_image[0].data
total = np.zeros(col)
average = np.zeros(col)
clear_data = np.zeros((row,col))
average1 = np.zeros(col)
total1 = np.zeros(col)

for i in range(col):
    for j in range(n):
        total[i] = total[i] + noise_data[j][i]
        average[i]  = total[i]/n
        total1[i] = total1[i] + noise_data[(row-1) - j][i]
        average1[i] = total1[i]/n
    for k in range(row): 
        if (k<row/2): 
                  clear_data[k][i] = noise_data[k][i] - average[i]
   
        else:
                  clear_data[k][i] = noise_data[k][i] - average1[i]

hdu = fits.PrimaryHDU(clear_data)
hdulist = fits.HDUList([hdu])
name = name[:-5]
hdulist.writeto(name+'clear-data.fits')
