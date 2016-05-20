#!/usr/bin/env python
# clipped mean combine

import sys
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

### paths ###
path = '/media/nivedita/New Volume/nires_data/tiptilt/'
opath = './data/'

row = 1024
col = 1024

### range of images to be considered
n1 = 74
n2 = 114

n3 = 21
n4 = 61

con = 'v160512_00'
con1 = 'v160512_0'
con2 = 'v160512_000'

### area of slit 
a_r = 550 - 380 +1
a_c = 162-95+1

print range(n1,n2,4)
j =0
data = np.zeros((11,row,col))

for i in range(n1,n2,4):
    if i > 99:
       image = fits.open(path+con1 +str(i) +'.fits')
    else:
       image = fits.open(path+con +str(i) +'.fits')
    data[j][:][:] = image[0].data
    j = j+1

yaxis = np.zeros((j+1,a_r,a_c))
xaxis = np.zeros((j+1,a_r,a_c))

x_p = np.zeros(11)
y_p = np.zeros(11)

y=0
for k in range(j):
    x=0
    temp = 0
    count = 0
    tempx = 0
    countx = 0
    for r in range(380,550):
        x = x+1
        y = 0
        if r < 500:
           for c in range(95,162):
               y = y +1
               if data[k][r][c] > -300 :   
                  yaxis[k][x][y] = c 
                  xaxis[k][x][y] = r
                  temp = temp+ yaxis[k][x][y]
                  count = count + 1
                  tempx = tempx+ xaxis[k][x][y]
                  countx = countx + 1
    y_p[k] =temp/count
    x_p[k] =tempx/countx 
      
np.savetxt('img0_y.txt', yaxis[0][:][:], delimiter= ",",fmt = '%d')
np.savetxt('img0_x.txt', xaxis[0][:][:], delimiter= ",",fmt = '%d') 
 
#print y_p , x_p   
theta = [0,5,10,15,20,25,30,35,40,45]
plt.plot(theta,y_p[:-1])
plt.ylim([124,125])
plt.xlabel('Theta (deg)')
plt.ylabel('col pix')
plt.savefig(opath+'x_theta1'+'.png', format = 'png')
plt.figure(2)
plt.plot(theta,x_p[:-1])
plt.xlabel('Theta (deg)')
plt.ylabel('row pix')
plt.savefig(opath+'y_theta1'+'.png', format = 'png')
