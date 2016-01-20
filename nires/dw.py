#!/usr/bin/env python
# Take difference between two fits files

import sys
import numpy as np
import readcol as rc
import pyfits as pf
import string
import ds9
import globals


unit = open('wavelength.reg','w')


unit.write('# Region file format: DS9 version 4.1\n')
unit.write('# Filename: wavelength.reg\n')
unit.write('global color=green dashlist=8 3 width=3 font="helvetica 14 bold" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
unit.write('physical\n')


try:
    yy,xx,lam=rc.readcol(globals.calibrationpath +'tspec_wavelength_file_iraf.dat',names=False,twod=False)
    
    r1=range(0,len(lam))
    
    jtest=True

    for i in r1:
        s='line(%d,%d,%d,%d) # line=0 0\n' % (xx[i],yy[i]+10,xx[i],yy[i])
        unit.write(s)
        s2='# text(%d,%d) text={%.2f}\n' % (xx[i],yy[i]+20,lam[i])
        unit.write(s2)
                                    
except:
    print "did not work"

unit.close()


try:
    DD=0
    DD=ds9.ds9("Spectrograph")
    DD.wavedisp()
except:
    print "Could not show wavelength" 
