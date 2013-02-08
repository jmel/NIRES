#!/usr/bin/env python
# Take difference between two fits files

import sys, pyfits as pf
import ds9
import warnings
import imDisplay as imD

def rf(fn):
	try:
		a = pf.open(fn)[0].data
	except:
		print "Could not open %s" % fn
	
	return a

def nameResolve(indexString,prefix='sp'):
	indexStringLen=len(indexString)
	if indexStringLen < 4:
		num=indexString
		for i in range(4-indexStringLen):
			num='0'+num
		name=prefix+num+'.fits'	
	#else:
	#	name=indexString
	print name
	return name

def returnInst(instString='s'):
	if instString == 'i':
		title='Imager'
		prefix='im'	
	elif instString == 's':
		title='Spectrograph'
		prefix='sp'
	return title,prefix

if len(sys.argv) == 4: 

	title,prefix=returnInst(sys.argv[1]) 

	a = rf(nameResolve(sys.argv[2],prefix))
	b = rf(nameResolve(sys.argv[3],prefix))
else:
	title='Autodisplay'
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
        DD=ds9.ds9(title)
        DD.open(fname,1)
except:
	print "Could not write %s" % fname
