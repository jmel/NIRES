#!/usr/bin/env python
# Take difference between two fits files

import sys
import numpy as np
import readcol as rc
import pyfits as pf
import string
import ds9
import globals

z = sys.argv[1]
print z
unit = open(globals.codepath +'calibrations/zregion.reg','w')
wsol = pf.open(globals.codepath +'calibrations/tspec_wavesol.fits')[0].data
sz=wsol.shape

unit.write('# Region file format: DS9 version 4.1\n')
unit.write('# Filename: zregion.reg\n')
unit.write('global color=green dashlist=8 3 width=3 font="helvetica 14 bold" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
unit.write('physical\n')

llist=np.arange(80)/80.
llist=llist.tolist()
llist.extend(np.arange(40)/40.*2.+1.)
print 'LList: ',llist,'\n'
try:
    names,(ord,xx,yy,lam)=rc.readcol(globals.codepath +'calibrations/tspec_wavelength_file.dat",names=True,twod=False)
    print ord
    print xx
    print 'lam: ',lam

    z=float(z)
    print 'z= ',z
    lam=lam/(1.+z)

    m=max(lam)
    
    llist2=[i for i in llist if i < m]
    print llist2

    r1=range(0,len(llist2))
    r2=range(0,len(lam))
    
    jtest=True

    for i in r1:
        jtest=True
        for j in r2:
            if (lam[j] > llist2[i] -0.0005) and (lam[j] < llist2[i] +0.0005):
                if jtest:
                    s='line(%d,%d,%d,%d) # color=black line=0 0\n' % (xx[j],yy[j]+90,xx[j],yy[j]+80)
                    unit.write(s)
                    s2='# text(%d,%d) color=black text={%.2f}\n' % (xx[j],yy[j]+110,llist2[i])
                    unit.write(s2)
                    jtest=False
            else:
                jtest=True
                
except:
    print "did not work"

unit.close()

try:
    DD=0
    DD=ds9.ds9("Spectrograph")
    DD.zdisp()
except:
    print "could not display \n"
        
