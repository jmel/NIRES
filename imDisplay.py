import sys, pyfits as pf
import glob
import warnings

def readImage(fn):
	try:
		a = pf.open(fn)[0].data
	except:
		print "Could not open %s" % fn
	
	return a

def nameResolve(indexString,prefix='s*'):
	indexStringLen=len(indexString)
	if indexStringLen < 4:
		num=indexString
		for i in range(4-indexStringLen):
			num='0'+num
		name=prefix+num+'.fits'	
	else:
		name=prefix+indexString+'.fits'
	try:
		name=glob.glob(name)[0]
	except: 
		print 'Image number out of range' 
		name=''

	return name

def returnInst(instString='s'):
	if instString == 'v':
		title='Viewer'
		prefix='i*'	
	elif instString == 's':
		title='Spectrograph'
		prefix='s*'
	return title,prefix
