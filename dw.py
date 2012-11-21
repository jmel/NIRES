#!/usr/bin/python2.6
# Take difference between two fits files

import sys
import ds9

try:
        DD=0
        DD=ds9.ds9("Autodisplay")
	DD.wavedisp()
except:
	print "Could not show wavelength" 
