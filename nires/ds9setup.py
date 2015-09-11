#!/usr/bin/env python
# Take difference between two fits files

import sys
import ds9
import imDisplay as imD

title, prefix = imD.returnInst(sys.argv[1])

try:
	dd = 0
	dd = ds9.ds9(title)
	dd.regSave(file=title)
except:
	print "Could not open ds9 for %s" % title

