#!/usr/bin/python2.6
# Take difference between two fits files

import sys
import ds9

a = sys.argv[1]

try:
	fname = a
        DD=0
        DD=ds9.ds9("Autodisplay")
        DD.open(fname,1)
	DD.wavedisp()
except:
	print "Could not write %s" % fname
