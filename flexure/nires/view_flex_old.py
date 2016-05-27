#!/usr/bin/env python
# clipped mean combine

import sys
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

### paths ### (changes based on system)
path = '/media/nivedita/New Volume2/nires_data/tiptilt/'
opath = './data/'

row = 1024
col = 1024

### range of images to be considered
n1 = 73
n2 = 110

n3 = 22
n4 = 61
l_i = (((n2-n1) + (n4-n3))/4) + 1
print l_i

con = 'v160512_00'
con1 = 'v160512_0'
con2 = 'v160512_000'

### area of slit 
r1 = 380
r2 = 550
c1 = 95
c2 = 135

a_r = r2 - r1 +1
a_c = c2 - c1+1

print range(n2,n1,-4)
print range(n3,n4,4)

j =0
data = np.zeros((20,row,col))

for i in range(n2,n1,-4):
    if i < 10:
       image = fits.open(path+con2 +str(i) +'.fits')
    elif i <100:
       image = fits.open(path+con +str(i) +'.fits')
    else:
       image = fits.open(path+con1 +str(i) +'.fits')
    data[j][:][:] = image[0].data
    j = j+1

for i in range(n3,n4,4):
    if i < 10:
       image = fits.open(path+con2 +str(i) +'.fits')
    elif i <100:
       image = fits.open(path+con +str(i) +'.fits')
    else:
       image = fits.open(path+con1 +str(i) +'.fits')
    data[j][:][:] = image[0].data
    j = j+1


yaxis = np.zeros((j,a_r,a_c))
xaxis = np.zeros((j,a_r,a_c))

x_p = np.zeros(j)
y_p = np.zeros(j)

y=0
for k in range(j):
    x=0
    temp1 = 0
    count = 0
    tempx1 = 0
    countx = 0
    for r in range(r1,r2):
        x = x+1
        y = 0
        temp = 0
        tempx = 0
        weight = 0
        if r < 510 or r>513:
           for c in range(c1,c2):
               y = y +1
               if data[k][r][c] > -700 and (data[k][r][c+3]>-300 or data[k][r][c-3]>-300 or data[k][r+3][c]>-300 or data[k][r-3][c]>-300) :   
                  yaxis[k][x][y] = c 
                  xaxis[k][x][y] = r
             #     temp = temp+ yaxis[k][x][y]*data[k][r][c]
                  tempx = tempx+ xaxis[k][x][y]*data[k][r][c]
                  weight = weight+data[k][r][c]
           print weight
           if abs(weight)>0:
       #       temp1 =temp1+ temp/weight
        #      count = count+1
              tempx1 =tempx1+ tempx/weight
              countx = countx+1
    #y_p[k] = temp1/count
    x_p[k] = tempx1/countx 
      
y=0
for k in range(j):
    x=0
    temp1 = 0
    count = 0
    tempx1 = 0
    countx = 0
    for c in range(c1,c2):
        x = x+1
        y = 0
        temp = 0
        tempx = 0
        weight = 0
        
        for r in range(r1,r2):
            if r < 510 or r>513:
               y = y +1
               if data[k][r][c] > -700 and (data[k][r][c+3]>-300 or data[k][r][c-3]>-300 or data[k][r+3][c]>-300 or data[k][r-3][c]>-300) :   
                  yaxis[k][y][x] = c 
                  xaxis[k][y][x] = r
                  temp = temp+ yaxis[k][y][x]*data[k][r][c]
                  #tempx = tempx+ xaxis[k][y][x]*data[k][r][c]
                  weight = weight+data[k][r][c]
        if abs(weight)>0:
              temp1 =temp1+ temp/weight
              count = count+1
              #tempx1 =tempx1+ tempx/weight
              #countx = countx+1
    y_p[k] = temp1/count
    #x_p[k] = tempx1/countx 



    #np.savetxt('img'+str(k)+'_y.txt', yaxis[k][:][:], delimiter= ",",fmt = '%d')
    #np.savetxt('img0'+str(k)+' _x.txt', xaxis[k][:][:], delimiter= ",",fmt = '%d') 



theta = [-45,-40,-35,-30,-25,-20,-15,-10,-5,0,0,5,10,15,20,25,30,35,40,45]
plt.plot(theta,y_p)
#plt.ylim([124,125])
plt.xlabel('Theta (deg)')
plt.ylabel('col pix')
plt.savefig(opath+'y_theta2'+'.png', format = 'png')
plt.figure(2)
plt.plot(theta,x_p)
plt.xlabel('Theta (deg)')
plt.ylabel('row pix')
plt.savefig(opath+'x_theta2'+'.png', format = 'png')
