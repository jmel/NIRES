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
    
    files = sorted([ f for f in os.listdir(dir) if f.startswith(prefix[0]) and f.endswith(suffix) and len(f) < 22])
    
    # handle old version of filename
    if len(files) == 0 and prefix[0] == 'v':
        files = sorted([ f for f in os.listdir(dir) if f.startswith('i') and f.endswith(suffix) and len(f) < 22])

    return files[-1]

def nameResolve(indexString, prefix): #removed the default setting of s*

    # check if only want most recent file indcated by indexString='c'
    if indexString == 'lp':
        try:
            return getMostRecentFile('.', prefix, 'fits')
        except:
            return ''
    # Check for length of input string to determine if you need to construct the name

    if is_number(indexString):
        indexStringLen = len(indexString)
    
        if indexStringLen < 4:
            num = indexString
            for i in range(4 - indexStringLen):
                num = '0' + num
            name = prefix + num + '.fits'    
        else:
            name = prefix + indexString + '.fits'
          
        try:
           
            full_name = glob.glob(globals.datapath + name)[0] #made the path absolute, used the path constant from globals
            
        except: 
        	# handle old version of the images 
            if name[0] == 'v':
                try:
                    name = 'i' + name[1:]
                    full_name = glob.glob(globals.datapath + name)[0]
                except:
                    print 'Image number out of range' 
                    full_name = ''
            else:
                print 'Image number out of range' 
                full_name = ''
        
        return full_name

    return indexString

def returnInst(instString): #removed the default setting of s
    if instString == 'v':
        title = 'Viewer'
        prefix = 'v*'    
    elif instString == 's':
        title = 'Spectrograph'
        prefix = 's*'
    else :
        print 'Please specify v for Viewer or s for Spectrograph'
    return title,prefix
