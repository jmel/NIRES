#!/usr/bin/env python
# Take difference between two fits files

import sys
import ds9
import imDisplay as imD
import time 

if len(sys.argv) == 2:
	fname = sys.argv[1]	
	title="Autodisplay"
else:
	title,prefix=imD.returnInst(sys.argv[1])
	fname=imD.nameResolve(sys.argv[2],prefix)

try:
	DD=0
	DD=ds9.ds9(title)
	DD.regSave(file=title)

	time.sleep(3)
	DD.open(fname,1)
	DD.regOpen(file=title)
except:
	print "Could not display %s" % fname
