#!/usr/bin/env python
# Delete the wavelength shown in ds9

import sys
import ds9

try:
    DD=0
    DD=ds9.ds9("Spectrograph")
    DD.wavDel()
except:
    print "Could not delete the wavelength" 
