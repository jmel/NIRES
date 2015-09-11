#!/usr/bin/env python
# Take difference between two fits files

import sys, pyfits as pf
import ds9
import warnings
import imDisplay as imD

if len(sys.argv) == 4: 

	title,prefix=imD.returnInst(sys.argv[1]) 

	a = imD.readImage(imD.nameResolve(sys.argv[2],prefix))
	b = imD.readImage(imD.nameResolve(sys.argv[3],prefix))
else:
	title='Autodisplay'
	a = imD.readImage(sys.argv[1])
	b = imD.readImage(sys.argv[2])



def fn(fn):
	return fn.split(".")[0]

try:
	hdu = pf.PrimaryHDU(a-b)
	hdulist = pf.HDUList([hdu])
except:
	print "Could not create FITS HDU"

try:
	fname = "d%sm%s.fits" % (fn(sys.argv[1]), fn(sys.argv[2]))
	with warnings.catch_warnings():
		warnings.simplefilter('ignore')
		hdulist.writeto(fname, clobber=True)
	print "ds9 %s " % fname
        DD=0
        DD=ds9.ds9(title)
    	DD.regSave(file=title)
        DD.open(fname,1)
        DD.regOpen(file=title)
except:
	print "Could not write %s" % fname
