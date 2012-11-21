
#  Written on 18 July 2011 by RFT to measure MOSFIRE flexure
#  Edited 2 October 2012 to improve readability

import pyfits as pf
#import scipy.signal as sig
import numpy as np
import pylab as pl
#from scipy import interpolate as int
#from scipy.special import erf
from scipy.optimize import leastsq


ROOT="/Users/Ryan/Documents/Physics/Caltech/Steidel/MOSFIRE/FCS/data/"

dg=np.pi/180.0

DEBUG_CENT = True # if True, writes out images of slits
do_fit = True
do_grid = True

filter_set=""
grating_set="HK" # HK | YJ | mirror

color_set='b'

if grating_set=="HK":
	color_set='r'
elif grating_set=="YJ":
	color_set='g'

def cm(box):
	'''Computes light-weighted center of slit box'''
	total = box.sum()
	y = np.arange(box.shape[0])
	x = np.arange(box.shape[1])
	xnum = (x*box.sum(0)).sum()
	xcm = xnum/total
	ynum = (y * box.sum(1)).sum()
	ycm = ynum/total

	return [xcm, ycm]


def measure_centroids(img,tag="",grating="mirror"):
	'''Computes mean and average '''
	if (tag) : tag="_"+tag
	if grating=="mirror":
		bl = [1021,90]
		ur = [1056,155]
		dx = 88.5
		dy = 0

	elif grating=="HK":
		bl = [372,63.5]
		ur = [407,133.5]
		dx = 88.5
		dy = -4

	elif grating=="YJ":
		bl = [755,72]
		ur = [785,142]
		dx = 88.5
		dy = -4		

	if DEBUG_CENT:
		pl.figure(1)
		pl.clf()
		pl.subplot(4,5,1)
		cnt = 1

	cms = []

	skipid = [10,11] # Indices of boxes to skip because of bad fits
	if DEBUG_CENT: fbox=open("boxes.reg","w")
	for i in range(22):
		# this defines slit boxes, which are assumed to be linearly
		# or quadratically distributed
		sub = img[bl[1]:ur[1], bl[0]:ur[0]]
		# next line defines box for .reg file for DS9
		box = ((ur[0]+bl[0])/2.0,(ur[1]+bl[1])/2.0,ur[0]-bl[0],ur[1]-bl[1])
		if grating != "mirror":
			dy += i*1.0/20.0
		bl[0] += dy
		bl[1] += dx
		ur[0] += dy
		ur[1] += dx
		try: 
			skipid.index(i)
			continue
		except: pass
		if DEBUG_CENT: fbox.write("box(%6.1f,%6.1f,%2i,%2i,0)\n" % box)
		cms.append(cm(sub))
		
		if DEBUG_CENT:
			# plots slit box image if DEBUG_CENT = True
			pl.subplot(4,5,cnt)
			cnt += 1
			pl.imshow(sub)

	if DEBUG_CENT:
		pl.savefig('fcs_'+grating+'_1'+tag+'.pdf')
		fbox.close()
		pl.close(1)

       	return np.array(cms)

def flexure_correction3(angs,params, filter=""):
	'''Returns flexure correction in pixels for a given Elevation, PA, and 
	vector of flexure ellipse parameters.'''
	El=angs[1]*dg
	PA=angs[0]*dg

	k=params[0] # ratio of minor to major axes of flexure ellipse
	ph=params[1]*dg # phase of ellipse
	th=params[2]*dg # rotation of major axis w.r.t. y axis
	amp=params[3]*np.sin(El-90*dg) # semi-major axis length
	Yc=params[4]*(1-np.cos(El-90*dg)) # center of ellipse in Y
	Xc=params[5]*(1-np.cos(El-90*dg)) # center of ellipse in Y
	af = 1

	Fy0=Yc+amp*np.cos(PA+th)*np.cos(ph)+ \
	    amp*k*np.sin(PA+th)*np.sin(ph)
	Fx0=Xc+amp*np.cos(PA+th)*np.sin(ph)- \
	    af*amp*k*np.sin(PA+th)*np.cos(ph)

	return [Fx0,Fy0]

def res(p,data,t,wt=None):
	'''Returns residuals to flexure model for fitting.'''
	mod = []
	for ii in range(len(t)):
		mod.append(flexure_correction3(t[ii],p,filter=filter_set))
	mod = -np.array(mod) # - because Fx is correction (x + Fx = 0)
	err = (data - mod).flatten()
	wterr = err*(wt.flatten())
	return wterr

# Define fiducial image for each grating mode
if grating_set=="HK":
	fitsb = pf.open(ROOT+"m120406_0066.fits")[0]
elif grating_set=="YJ":
	fitsb = pf.open(ROOT+"m120406_0068.fits")[0]
elif grating_set=="mirror":
	fitsb = pf.open(ROOT+"m120406_0077.fits")[0]

foo=DEBUG_CENT # This is to ensure slit images are written for fiducial image
DEBUG_CENT=True
b = fitsb.data
fid = measure_centroids(b,grating=grating_set)
DEBUG_CENT=foo

# Define flexure ellipse parameters for each grating mode
if grating_set=="mirror":
	p0 = [0.206, 24.3, 54.8, 4.80, 8.24, 2.08] # Mirror CSU fit (3/21/11)
elif grating_set=="HK":
	p0 = [0.161, 9.60, 66.5, 5.33,6.89,0.626] # HK CSU zen fit (3/23/12)
elif grating_set=="YJ":
	p0 = [0.185, 11.3, 66.6, 5.28, 7.18, 0.68] # YJ CSU fit (3/21/11)

cnt = 1

# Define input images to analyze for each mode
if grating_set=="mirror":
	skiplist=[]
	imgs = range(235,273,3) # Mirror no FCS 5 April 2012 (First Light)
elif grating_set=="HK":
	skiplist=[334,335,336]
	imgs = range(329,354) # HK no FCS 5 April 2012, el=45 (First Light)
elif grating_set=="YJ":
	imgs = range(120,158) # YJ no FCS 5 April 2012 (First Light)

print "grating = ",grating_set
print "id objname  pa  zen    --> Xc  Yc"
pas = []
els = []
xs = []
ys = []

sweep=0

f=open("flex_spec_log.dat","w")

for img in imgs:
	try:
		skiplist.index(img)
		continue
	except: pass

	# Open image
	try:
		fitsb = pf.open(ROOT+"m120406_%4.4i.fits" % img)[0]
		b = fitsb.data
	except:
		print "File "+"m120406_%4.4i.fits not found" % img
		continue

	if fitsb.header["aborted"] == True:
		continue

	# Measure slit positions
	cms = measure_centroids(b,"%4.4i" % img,grating=grating_set)

	# Compare to fiducial image
	delts = cms - fid

	cms = [np.mean(delts[:,0]), np.mean(delts[:,1])]
	sds = [np.std(delts[:,0]), np.std(delts[:,1])]

	objname = fitsb.header["object"]

	elevation='elevation'
	phase='phase'

	# This reads from the FITS header OBJECT keyword
	# Keyword was written as Python dictionary:
	# {'elevation':<elevation angle>,'phase':<phase angle>}
	fd=eval(fitsb.header["framdesc"])

	El=fd["elevation"]
	try:
		El=float(El)
	except:
		pass
	els.append(El)
	try:
		pai=fd["phase"]
	except:
		pai=float(fd["phase"])
	pas.append(pai)

	# This defines a new "sweep" if direction of rotation has changed
	# since last image... useful for looking for hysteresis 
	if len(pas)>2 and ((pas[-1]>pas[-2] and pas[-2]<pas[-3]) or \
				    (pas[-1]<pas[-2] and pas[-2]>pas[-3])):
		sweep += 1

	# Calculate expected flexure and corrected image position
	# given fiducial model
	flex=flexure_correction3([pai,El],p0,filter=filter_set)
	cor = [cms[0]+flex[0],cms[1]+flex[1]]

	print "%i %s %3.2f %i --> %2.1f %2.1f %2.1f %2.1f %2.1f %2.1f %2.1f %2.1f" % (img,  objname, pai, El, cms[0], cms[1], sds[0], sds[1], flex[0], flex[1], cor[0], cor[1])

	f.write("%i %3.2f %3.1f %2.1f %2.1f %2.1f %2.1f" % (img, pai, El, cms[0], cms[1], sds[0], sds[1]))

	xs.append([cms[0], sds[0], cor[0], sweep])
	ys.append([cms[1], sds[1], cor[1], sweep])

f.close()

xs = np.array(xs)
ys = np.array(ys)
pas = np.array(pas)
els = np.array(els)

xd = xs[:,0]
xe = xs[:,1]
xc = xs[:,2]
yd = ys[:,0]
ye = ys[:,1]
yc = ys[:,2]
sw = xs[:,3]

# Fit ellipse parameters to data, using fiducial parameters as starting point
if do_fit == True:
	data = np.transpose(np.array([xd,yd]))
	err =  np.transpose(np.array([xe,ye]))
	angs = [[pas[ii],els[ii]] for ii in range(len(pas))]
	fit = leastsq(res,p0,args=(data,angs,err**(-2)),full_output=1)
	p1 = fit[0]
	cov_x = fit[1]
	perr = range(len(p1))
	print "Best fit params: %5.3f %3.1f %3.1f %4.2f %4.2f %4.2f" % tuple(p1)
	try:
		for ii in range(len(perr)):
			perr[ii] = np.sqrt(cov_x[ii,ii])
		print "Parameter errors: %5.3f %3.1f %3.1f %4.2f %4.2f %4.2f" % tuple(perr)
	except:
		pass
	print "Original params: %5.3f %3.1f %3.1f %4.2f %4.2f %4.2f" % tuple(p0)
	print "Difference: %5.3f %3.1f %3.1f %4.2f %4.2f %4.2f" % tuple(p1-p0)
	
	for i in range(len(pas)):
		flex = flexure_correction3([pas[i],els[i]],p1)
		xc[i] = xd[i]+flex[0]
		yc[i] = yd[i]+flex[1]
else: p1=p0

# Plot residuals of flexure model vs. PA
pl.figure(2)
pl.clf()

# Create vector of flexure model predictions for comparison
Fx=[]
Fy=[]
anglist=np.arange(-180,181,1)
for ang in anglist:
	flex=flexure_correction3([ang,45],p1,filter=filter_set)
	Fx.append(-flex[0])
	Fy.append(-flex[1])

pl.plot(anglist,Fx,c='k')
pl.plot(anglist,Fy,c='r')

pau=np.unique(pas)
colx=['b','g','r']
coly=['y','purple','orange']
#for i in range(len(pau)):
#	idx=pas==pau[i]
#	pl.errorbar(els[idx], xd[idx], xe[idx],c=colx[i])
#	pl.errorbar(els[idx], yd[idx], ye[idx],c=coly[i])
#	pl.text(-100+100*i,-0.5,"El = %3i" % pau[i],horizontalalignment='center',
#		verticalalignment='center',color=colx[i])

#pl.errorbar(els, xd, xe,c=colx[0])
#pl.errorbar(els, yd, ye,c=coly[0])
pl.errorbar(pas, xd, xe,c=colx[0])
pl.errorbar(pas, yd, ye,c=coly[0])
#pl.text(0,2.75,"X",horizontalalignment='center',
#	 verticalalignment='center',color='k')
#pl.text(0,0.75,"Y",horizontalalignment='center',
#	 verticalalignment='center',color='k')
#pl.title("Residual Flexure at Z=-60 degrees (Mirror")
pl.xlabel("PA (degrees)")
pl.ylabel("Residual Flexure (pixels)")
#pl.axis([-200,200,-1,3])

pl.savefig('fcs_spec_'+grating_set+'_2.pdf')
#pl.close(2)


# Plot residuals in X vs. Y
pl.figure(3)
pl.clf()
xlim=[-0.6,0.6]
ylim=[-0.6,0.6]
if do_grid:
	gspace=0.1
	gxlist=np.arange(xlim[0],xlim[1]+gspace,gspace)
	gylist=np.arange(ylim[0],ylim[1]+gspace,gspace)
	for gx in gxlist:
		pl.plot([gx,gx],ylim,'0.7')
	for gy in gylist:
		pl.plot(xlim,[gy,gy],'0.7')

#sigx=np.std(xd)
#sigy=np.std(yd)
sigx=np.std(xc)
sigy=np.std(yc)
slitsigx=np.mean(xe)
slitsigy=np.mean(ye)
pl.errorbar(xc,yc,ye,xe,"*")
#for i in range(len(Zu)):
#	idx=els==Zu[i]
#	pl.errorbar(xd[idx], yd[idx], ye[idx], xe[idx],col[i]+'*')
#	pl.text(-0.25+0.25*i,-0.5,"Z = %3i" % Zu[i],horizontalalignment='center',
#		verticalalignment='center',color=col[i])

#pl.errorbar(xd,yd,ye,xe,"*")
pl.text(0,0.5,
	"sig_x: %3.2f (%3.2f); sig_y: %3.2f (%3.2f)" % (sigx, slitsigx, \
		 sigy, slitsigy),
	horizontalalignment='center',
	verticalalignment='center')
pl.axis([-0.6,0.6,-0.6,0.6])
pl.title("Residual Flexure ("+grating_set+")")
pl.xlabel("Spectral direction (pix)")
pl.ylabel("Spatial direction (pix)")
#pl.axis([-0.4,0.4,-0.15,0.15])
pl.savefig('fcs_spec_'+grating_set+'_3.pdf')
#pl.close(3)


# Plot flexure in X vs. Y
pl.figure(4)
pl.clf()
xlim=[-2,3]
ylim=[-8,8]
if do_grid:
	gspace=0.5
	gxlist=np.arange(xlim[0],xlim[1]+gspace,gspace)
	gylist=np.arange(ylim[0],ylim[1]+gspace,gspace)
	for gx in gxlist:
		pl.plot([gx,gx],ylim,'0.7')
	for gy in gylist:
		pl.plot(xlim,[gy,gy],'0.7')

sigx=np.std(xd)
sigy=np.std(yd)
#sigx=np.std(xc)
#sigy=np.std(yc)
slitsigx=np.mean(xe)
slitsigy=np.mean(ye)
#pl.errorbar(xc,yc,ye,xe,"*")
pl.errorbar(xd,yd,ye,xe,"*")
pl.plot(Fx,Fy,c='k')
pl.text((xlim[0]+xlim[1])/2.0,ylim[1]-gspace/2.0,
	"sig_x: %3.2f (%3.2f); sig_y: %3.2f (%3.2f)" % (sigx, slitsigx, \
		 sigy, slitsigy),
	horizontalalignment='center',
	verticalalignment='center')

pl.axis([xlim[0],xlim[1],ylim[0],ylim[1]])
pl.title("Residual Flexure ("+grating_set+")")
pl.xlabel("Spectral direction (pix)")
pl.ylabel("Spatial direction (pix)")
#pl.axis('scaled')
#pl.axis([-0.4,0.4,-0.15,0.15])
pl.savefig('fcs_spec_'+grating_set+'_4.pdf')
#pl.close(4)
