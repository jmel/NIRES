#!/usr/bin/env python
# removing the noise

import sys
import ds9
import imDisplay as imD
import numpy as np
#from matplotlib import pyplot as plt
from astropy.io import fits
#title = ''

#print sys.argv[2]
#name=imD.nameResolve(sys.argv[2],'s*')

noise_image = fits.open('s151112_a000017.fits')

noise_data = noise_image[0].data
total = np.zeros(2048)
average = np.zeros(2048)
clear_data = np.zeros((1024,2048))
average1 = np.zeros(2048)
total1 = np.zeros(2048)

for i in range(2048):
    for j in range(16):
        total[i] = total[i] + noise_data[j][i]
        average[i]  = total[i]/16
        total1[i] = total1[i] + noise_data[1023 - j][i]
        average1[i] = total1[i]/16
    for k in range(1024): 
        if (k<512): 
                  clear_data[k][i] = noise_data[k][i] - average[i]
   
        else:
                  clear_data[k][i] = noise_data[k][i] - average1[i]

hdu = fits.PrimaryHDU(clear_data)
hdulist = fits.HDUList([hdu])
hdulist.writeto('clear-data.fits')
