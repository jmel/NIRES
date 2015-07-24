#!/usr/bin/env python
# Take difference between two fits files

import sys
import ds9
import imDisplay as imD
import time 

if len(sys.argv) == 2:
	fname = sys.argv[1]	
	title = "Autodisplay"
else:
	title, prefix = imD.returnInst(sys.argv[1])
	fname = imD.nameResolve(sys.argv[2], prefix)

try:
	dd = 0
	dd = ds9.ds9(title)
	dd.regSave(file=title)
	dd.open(fname,1)
	dd.regOpen(file=title)
except:
	print "Could not display %s" % fname
