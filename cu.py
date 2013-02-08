#!/usr/bin/python2.6
# Take difference between two fits files

import sys
import ds9

argc=len(sys.argv)

if argc==1:
	sys.exit()

print "Number Args = ", argc
color=["white","yellow","cyan","blue","magenta","green","orange","red","brown","black"]

cuNumber = sys.argv[1]	
print cuNumber 

DD=0
DD=ds9.ds9("Imager")

if cuNumber.lower() == 'all':
	DD.cuDel(group="all")
	if argc==2:
		for i in range(10):
			DD.cuDisp(200+i*50,600,15,group="group"+str(i),label=str(i),color=color[i])
	sys.exit()

if argc==3:
	command=sys.argv[2]
	if command.lower() == 'del':
		DD.cuDel(group="group"+cuNumber)
	elif command.lower()=='cent':
		DD.cuCent(group="group"+cuNumber)
	elif command.lower()=='info':
		DD.cuInfo(group="group"+cuNumber)
	sys.exit()


if argc ==2:
	cuX=200+int(cuNumber)*50
	cuY=600
if argc >= 4:	
	cuX=float(sys.argv[2])
	cuY=float(sys.argv[3])

DD.cuDel(group="group"+cuNumber)
DD.cuDisp(cuX,cuY,15,group="group"+cuNumber,color=color[int(cuNumber)],label=cuNumber)
