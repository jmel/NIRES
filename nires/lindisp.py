#!/usr/bin/env python
#change the display

import sys
import ds9
import imDisplay as imD

try:
	title,prefix=imD.returnInst(sys.argv[1])
except:
	print ""
	print "ERROR: please provide the instrument"
	print "s - spectrograph"
	print "v - viewer"
	print "e.g. > lindisp v 0 1000"	
	print ""

try:
	DD=0
	DD=ds9.ds9(title)
	DD.lindisp(float(sys.argv[2]),float(sys.argv[3]))
except:
	print "Could not change display"
	print