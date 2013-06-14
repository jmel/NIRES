#!/usr/bin/env python
# Take difference between two fits files

import sys, pyfits as pf
import ds9
import warnings

def rf(fn):
	try:
		a = pf.open(fn)[0].data
	except:
		print "Could not open %s" % fn
	
	return a


a = rf(sys.argv[1])
b = rf(sys.argv[2])

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
        DD=ds9.ds9("Autodisplay")
        DD.open(fname,1)
except:
	print "Could not write %s" % fname
