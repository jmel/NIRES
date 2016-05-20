#!/usr/bin/env python
# showing the orders by using the edge detection algorithm


import numpy as np
from astropy.io import fits
import imDisplay as imD
import sys
import globals


fname = imD.nameResolve(sys.argv[1], 's*')
continuum_image = fits.open(fname)
continuum_data = continuum_image[0].data


##own code for order determination

for i in range(1, 1024):
    for j in range(1, 2048):
        if i > 504:
           if j > 1810:
              if continuum_data[i][j] > 25:
                 continuum_data[i][j] = 1
              else:
                 continuum_data[i][j] = 0
           else:
               if continuum_data[i][j] > 45:
                  continuum_data[i][j] = 1
               else:
                  continuum_data[i][j] = 0
        else:
           if i<=504 and i>360:
              if j > 1610 and j<1745:
                 if continuum_data[i][j] > 12:
                    continuum_data[i][j] = 1
                 else:
                    continuum_data[i][j] = 0 
              else:
                  if j>=1745 and j < 1820:
                     if continuum_data[i][j] > 7:
                        continuum_data[i][j] = 1
                     else:
                        continuum_data[i][j] = 0  
                  else:
                      if j>=1820:
                         if continuum_data[i][j] > 5:
                            continuum_data[i][j] = 1
                         else:
                            continuum_data[i][j] = 0
                      else:
                         if continuum_data[i][j] > 18:
                            continuum_data[i][j] = 1
                         else:
                            continuum_data[i][j] = 0
           else:
               if j<1745:
                  if continuum_data[i][j] > 13:
                     continuum_data[i][j] = 1
                  else:
                     continuum_data[i][j] = 0
               else:
                  if j >=1745 and j<1820:
                     if continuum_data[i][j] > 7:
                        continuum_data[i][j] = 1
                     else:
                        continuum_data[i][j] = 0
                  else:
                     if j>=1820:
                        if continuum_data[i][j] > 5:
                           continuum_data[i][j] = 1
                        else:
                           continuum_data[i][j] = 0 
                    
hdu = fits.PrimaryHDU(continuum_data)
hdulist = fits.HDUList([hdu])
hdulist.writeto(globals.datapath+'order-bright.fits')
