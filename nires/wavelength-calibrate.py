#!/usr/bin/env python
# Take difference between two fits files

import sys
import numpy as np
import readcol as rc
from astropy.io import fits
import globals

x,y,wav = rc.readcol(globals.calpath+'wavelength.txt',skipline=1,twod=False)
xh,yh,wavh = rc.readcol(globals.calpath+'wavelength-h.txt',skipline=1,twod=False)
xj,yj,wavj = rc.readcol(globals.calpath+'wavelength-j.txt',skipline=1,twod=False)

order_image = fits.open(globals.datapath +'order-bright.fits')
order_data = order_image[0].data


co = np.zeros((len(wav),16))
for k in range(len(wav)-1):
    c = 0
    for i in range(3):
        for j in range(3):
        
            co[k][c] = x[k]**(i-1) * y[k]**(j-1)
            c = c+1

coeff = np.dot(np.linalg.pinv(co),wav); # the model

coh = np.zeros((len(wavh),16))

for k in range(len(wavh)-1):
    c = 0
    for i in range(3):
        for j in range(3):
        
            coh[k][c] = xh[k]**(i-1) * yh[k]**(j-1)
            c = c+1

coeffh = np.dot(np.linalg.pinv(coh),wavh); # the model

coj = np.zeros((len(wavj),16))

for k in range(len(wavj)-1):
    c = 0
    for i in range(3):
        for j in range(3):
        
            coj[k][c] = xj[k]**(i-1) * yj[k]**(j-1)
            c = c+1

coeffj = np.dot(np.linalg.pinv(coj),wavj); # the model
row = 1024
col = 2048 

lambda1 = np.zeros((row,col))
count  = 0
# used to predict some value from the training set
for m in range(0, row):
    if m >816 and m<row:
       for n in range(col-1):
           num = 0
           for l in  range(3):
               for g in  range(3):
              
                   lambda1[m][n] = lambda1[m][n] + coeff[num]*(n+1)**(l-1)*m**(g-1)
                   num = num + 1
           lambda1[m][n] = lambda1[m][n]*order_data[m][n]    
    else:
	 if m < 816 and m > 649:
            for n in range(col-1):
                num = 0
                for l in  range(3):
                    for g in  range(3):
                        lambda1[m][n] = lambda1[m][n] + coeffh[num]*(n+1)**(l-1)*m**(g-1)
                        num = num + 1
                lambda1[m][n] = lambda1[m][n]*order_data[m][n] 
        
         else:
             if m<649 and m>466:
                for n in range(col-1):
                    num = 0
                    for l in  range(3):
                        for g in  range(3):
              
                            lambda1[m][n] = lambda1[m][n] + coeffj[num]*(n+1)**(l-1)*m**(g-1)
                            num = num + 1
                    lambda1[m][n] = lambda1[m][n]*order_data[m][n] 
             else:
                 for n in range(col-1):
                     num = 0
                     lambda1[m][n] = lambda1[m][n] + 1
                     num = num + 1
                     lambda1[m][n] = lambda1[m][n]*order_data[m][n] 
        


hdu = fits.PrimaryHDU(lambda1)
hdulist = fits.HDUList([hdu])
hdulist.writeto(globals.datapath+'nires-order.fits')
