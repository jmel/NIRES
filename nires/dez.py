#!/usr/bin/env python
# Take difference between two fits files

import sys
import numpy
import readcol as rc
import pyfits as pf
import string
import ds9
import globals


z = sys.argv[1]

unit = open(globals.calibrationpath + 'z_emission.reg','w')
wsol = pf.open(globals.calibrationpath + 'tspec_wavesol.fits')[0].data
sz=wsol.shape

unit.write('# Region file format: DS9 version 4.1\n')
unit.write('# Filename: zregion.reg\n')
unit.write('global color=black dashlist=8 3 width=3 font="helvetica 14 bold" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
unit.write('physical\n')

try:
    id,pd,llist=rc.readcol(globals.calibrationpath + 'emissionLineList.dat',names=False,twod=False,fsep=",")
    names,(ord,xx,yy,lam)=rc.readcol(globals.calibrationpath + 'tspec_wavelength_file.dat',names=True,twod=False)

    z=float(z)
    lam=lam/(1.+z)
    id=id.tolist()
    lam=lam.tolist()
    print id
    print lam

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
                    s='line(%d,%d,%d,%d) # line=0 0\n' % (xx[j],yy[j]+90,xx[j],yy[j]+80)
                    unit.write(s)
                    s2='# text(%d,%d) text={%s}\n' % (xx[j],yy[j]+110,pd[i])
                    unit.write(s2)
                    jtest=False
            else:
                jtest=True



    '''r1=range(0,sz[0])
    r1.reverse()
    r2=range(0,sz[1])
    r2.reverse()

    for i in r1:
        for j in r2:
            c=0
            for ll in lam:
                if (wsol[i,j] > ll -0.0005) and (wsol[i,j] < ll +0.0005): 
                    print i,j,ll,wsol[i,j]
                    s='line(%d,%d,%d,%d) # line=0 0\n' % (j,i-80,j,i-60)
                    print s
                    unit.write(s)
                    s2='# text(%d,%d) text={%s}\n' % (j,i-90,id[c])
                    unit.write(s2)
                    lam.pop(c)
                    id.pop(c)
                c=c+1'''
except:
    print "did not work"

unit.close()
        

try:
    DD=0
    DD=ds9.ds9("Spectrograph")
    DD.emissiondisp()
except:
    print "could not display \n"
