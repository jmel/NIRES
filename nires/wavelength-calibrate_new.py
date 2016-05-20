#!/usr/bin/env python
# Take difference between two fits files

import sys
import numpy as np
import readcol as rc
from astropy.io import fits
import globals

<<<<<<< HEAD:wavelength-calibrate_new.py
x,y,wav = rc.readcol('wavelength.txt',skipline=1,twod=False)
xh,yh,wavh = rc.readcol('wavelength-h.txt',skipline=1,twod=False)
xj,yj,wavj = rc.readcol('wavelength-j.txt',skipline=1,twod=False)
xj1,yj1,wavj1 = rc.readcol('wavelength-j1.txt',skipline=1,twod=False)

order_image = fits.open('order-bright1.fits')
order_data = order_image[0].data

#print order_data[810][1]
=======
x,y,wav = rc.readcol(globals.calpath+'wavelength.txt',skipline=1,twod=False)
xh,yh,wavh = rc.readcol(globals.calpath+'wavelength-h.txt',skipline=1,twod=False)
xj,yj,wavj = rc.readcol(globals.calpath+'wavelength-j.txt',skipline=1,twod=False)

order_image = fits.open(globals.datapath +'order-bright.fits')
order_data = order_image[0].data


>>>>>>> master:nires/wavelength-calibrate_new.py
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
<<<<<<< HEAD:wavelength-calibrate_new.py

coj1 = np.zeros((len(wavj1),16))

for k in range(len(wavj1)-1):
    c = 0
    for i in range(3):
        for j in range(3):
        
            coj1[k][c] = xj1[k]**(i-1) * yj1[k]**(j-1)
            c = c+1

coeffj1 = np.dot(np.linalg.pinv(coj1),wavj1); # the model


fits_o = open('k-order1.txt','w');
lambda1 = np.zeros((1024 ,2048))
count  = 0
# used to predict some value from the training set
for m in range(1 , 1024):
    if m >816 and m<1024:
       for n in range(2047):
=======
row = 1024
col = 2048 
fits_o = open('k-order1.txt','w');
lambda1 = np.zeros((row,col))
count  = 0
# used to predict some value from the training set
for m in range(0, row):
    if m >816 and m<row:
       for n in range(col-1):
>>>>>>> master:nires/wavelength-calibrate_new.py
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
<<<<<<< HEAD:wavelength-calibrate_new.py
              if m> 479 and m<649:
                 for n in range(2047):
                     num = 0
                     for l in  range(3):
                         for g in  range(3):
              
                             lambda1[m][n] = lambda1[m][n] + coeffj[num]*(n+1)**(l-1)*m**(g-1)
                             num = num + 1
                     lambda1[m][n] = lambda1[m][n]*order_data[m][n] 
              else:
                   if m > 280 and m< 479:  
                      for n in range(2047):
                          num = 0
                          for l in  range(3):
                              for g in  range(3):
              
                                  lambda1[m][n] = lambda1[m][n] + coeffj1[num]*(n+1)**(l-1)*m**(g-1)
                                  num = num + 1
                          lambda1[m][n] = lambda1[m][n]*order_data[m][n] 
                   else:
                       for n in range(2047):
                           num = 0
                           for l in  range(3):
                               for g in  range(3):
=======
              for n in range(col-1):
                  num = 0
                  for l in  range(3):
                      for g in  range(3):
>>>>>>> master:nires/wavelength-calibrate_new.py
              
                                   lambda1[m][n] = 1
                                   num = num + 1
                           lambda1[m][n] = lambda1[m][n]*order_data[m][n] 

        


hdu = fits.PrimaryHDU(lambda1)
hdulist = fits.HDUList([hdu])
<<<<<<< HEAD:wavelength-calibrate_new.py
hdulist.writeto('nires-wavelength.fits')
=======
hdulist.writeto(globals.datapath+'nires-order.fits')
>>>>>>> master:nires/wavelength-calibrate_new.py
