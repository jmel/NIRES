#!/usr/bin/env python
# Take difference between two fits files

import sys
import ds9
import imDisplay as imD
import time

if len(sys.argv) == 3:
    title,prefix=imD.returnInst(sys.argv[1])
    fname=imD.nameResolve(sys.argv[2],prefix)
else :
    print 'Did not specify required arguments, Here are some examples: "dps 50" or "dp s 50", "dpv 50" or "dp v 50"  '
    exit();
        
try:
    dd = 0
    dd = ds9.ds9(title)
    dd.regSave(file=title)
    dd.open(fname,1) #the number is used to set the frame number in the tile mode which is enable
    dd.regOpen(file=title)
except:
    print "Could not display %s" % fname
