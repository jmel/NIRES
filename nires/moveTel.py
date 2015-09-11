#!/usr/bin/env python
# Determine the move of the telescope

import sys
import ds9

argc=len(sys.argv)

if argc < 3:
	sys.exit()

startNumber = sys.argv[1]
endNumber = sys.argv[2]	


DD=0
title="Imager"
DD=ds9.ds9(title)
DD.regSave(file=title)

try:
	f=open(title+'.reg','r')
except: 
    print title+'.reg : File not found'
    sys.exit()

try:
	searchString1='text={'+startNumber+'}'
	searchString2='text={'+endNumber+'}'
	xStart=0
	yStart=0
	xEnd=0
	yEnd=0
	for line in f:
		if searchString1 in line:
			elements=line.split(',')
			xStart=float(elements[0].split('(')[1])
			yStart=float(elements[1])
		if searchString2 in line:
			elements=line.split(',')
			xEnd=float(elements[0].split('(')[1])
			yEnd=float(elements[1])
		if xStart != 0 and xEnd != 0:
			break

	print 'Delta X = %.2f, Delta Y = %.2f' % (xStart-xEnd,yStart-yEnd)
except:
	print 'could not resolve the move'
	



