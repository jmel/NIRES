import sys, pyfits as pf
import glob
import warnings
import os
import globals

def readImage(fn):
	try:
		a = pf.open(fn)[0].data
	except:
		print "Could not open %s" % fn
	
	return a

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def getMostRecentFile(dir, prefix='s', suffix='.fits'):
	files = sorted([ f for f in os.listdir(dir) if f.startswith(prefix) and f.endswith(suffix)])
	return files[-1]

def nameResolve(indexString,prefix): #removed the default setting of s*

	# check if only want most recent file indcated by indexString='c'
	if indexString == 'c':
		try:
			return getMostRecentFile('.',prefix,'fits')
		except:
			return ''
	# Check for length of input string to determine if you need to construct the name

	if is_number(indexString):
		indexStringLen=len(indexString)
	
		if indexStringLen < 4:
			num=indexString
			for i in range(4-indexStringLen):
				num='0'+num
			name=prefix+num+'.fits'	
		else:
			name=prefix+indexString+'.fits'
			

		try:
                        name=glob.glob(globals.datapath + name)[0] #made the path absolute, used the path constant from globals
			
		except: 
			print 'Image number out of range' 
			name=''

		return name

	return indexString

def returnInst(instString): #removed the default setting of s
	if instString == 'v':
		title='Viewer'
		prefix='i*'	
	elif instString == 's':
		title='Spectrograph'
		prefix='s*'
	return title,prefix
