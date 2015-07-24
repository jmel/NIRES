
#  Written on 18 July 2011 by RFT to measure MOSFIRE flexure
#  Edited 21 February 2014 to get flexure in triplespec

import pyfits as pf
import numpy as np
import pylab as pl
import csv
import matplotlib.pyplot as plt
from scipy.optimize import leastsq


deg_to_radians = np.pi / 180.0

# Define starting point of flexure ellipse parameters 
p0 = [0.161, 9.60, 66.5, 5.33,6.89,0.626] # HK CSU zen fit (3/23/12)

def flexure_correction3(angs, params):
	'''Returns flexure correction in pixels for a given Elevation, PA, and 
	vector of flexure ellipse parameters.'''

	El = angs[1] * deg_to_radians
	PA = angs[0] * deg_to_radians

	k = params[0] # ratio of minor to major axes of flexure ellipse
	ph = params[1] * deg_to_radians # phase of ellipse
	th = params[2] * deg_to_radians # rotation of major axis w.r.t. y axis
	amp = params[3] * np.sin(El - 90 * deg_to_radians) # semi-major axis length
	Yc = params[4] * (1 - np.cos(El - 90 * deg_to_radians)) # center of ellipse in Y
	Xc = params[5] * (1 - np.cos(El - 90 * deg_to_radians)) # center of ellipse in X
	#Yc = params[4] * np.sin(El - 90 * deg_to_radians) # center of ellipse in Y
	#Xc = params[5] * np.sin(El - 90 * deg_to_radians) # center of ellipse in X
	af = 1

	Fy0 = Yc + amp * np.cos(PA + th) * np.cos(ph) + \
	    amp * k * np.sin(PA + th) * np.sin(ph)
	Fx0 = Xc + amp * np.cos(PA + th) * np.sin(ph) - \
	    af * amp * k * np.sin(PA + th) * np.cos(ph)

	return [Fx0, Fy0]

def res(p, data, t, wt=None):
	'''Returns residuals to flexure model for fitting.'''

	mod = []
	for ii in range(len(t)):
		mod.append(flexure_correction3(t[ii], p))
	mod = -np.array(mod) # - because Fx is correction (x + Fx = 0)
	err = (data - mod).flatten()
	wterr = err * (wt.flatten())

	return wterr

def read_flexure_data():
	''' read in flexure data from files''' 

	pas = [] # position angles
	els = [] # elevations
	xs = [] # x-centroids
	ys = [] # y-centroids

	data_dir = '/Users/jmel/nires/triplespecFlexure/'
	with open(data_dir + 'zenith30.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		help, reader
		header = reader.next()
		for row in reader:
			help, row
			els.append(float(row[0]))
			pas.append(float(row[1]))
			xs.append(float(row[2]))
			ys.append(float(row[3]))

	with open(data_dir + 'zenith60.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		header = reader.next()
		for row in reader:
			els.append(float(row[0]))
			pas.append(float(row[1]))
			xs.append(float(row[2]))
			ys.append(float(row[3]))	
	el30i = [i for i, j in enumerate(els) if j == 30]
	el60i = [i for i, j in enumerate(els) if j == 60]
	xs = np.array(xs) - np.median(xs)
	# xs[el30i] = xs[el30i] - np.median(xs[el30i])
	# xs[el60i] = xs[el60i] - 0.3

	ys = np.array(ys) - np.median(ys)
	# ys[el30i] = ys[el30i] - np.median(ys[el30i])
	# ys[el60i] = ys[el60i] + 0.3

	pas = np.array(pas) 
	els = np.array(els) 

	return xs, ys, pas, els


def fit_ellipse(xs=None, ys=None, pas=None, els=None):
	''' Fit ellipse parameters to data, using fiducial parameters as starting point'''

	if (xs == None):
		xs, ys, pas, els = read_flexure_data()

	print 'XS:', xs
	print 'YS:', ys
	print 'PA:', pas
	print 'EL:', els

	xd = xs 
	xe = xs * 0. + 0.05 
	
	yd = ys
	ye = ys * 0. + 0.05


	data = np.transpose(np.array([xd,yd])) # centroid means
	err =  np.transpose(np.array([xe,ye])) # centroid stddev
	angs = [[pas[ii],els[ii]] for ii in range(len(pas))] # angles 

	fit = leastsq(res, p0, args=(data,angs,err**(-2)), full_output=1)

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
	
	return p1, perr

def plot_flexure_corrections():
	
	p1, perr = fit_ellipse()
	xs, ys, pas, els = read_flexure_data()
	
	xcor = []
	ycor = []

	for pa, el in zip(pas,els):
		[x1, y1] = flexure_correction3([pa,el], p1)
		xcor.append(x1)
		ycor.append(y1)

	fig = plt.figure()
	plt.scatter(pas, ys, c='red')
	plt.scatter(pas, ys + ycor , c='blue')
	plt.ylim([-0.8,0.8])
	plt.xlim([200,600])
	plt.xlabel('ring angle')
	plt.ylabel('y offset [pix]')
	plt.plot([200,600], [0,0], 'b--')
	fig.suptitle('Flexure Correction', fontsize=20)
	fig.savefig('/Users/jmel/nires/plots/tspec_flexure_y2.pdf')

	fig = plt.figure()
	plt.scatter(pas, xs, c='red')
	plt.scatter(pas, xs + xcor, c='blue')
	plt.ylim([-0.8,0.8])
	plt.xlim([200,600])
	plt.xlabel('ring angle')
	plt.ylabel('x offset [pix]')
	plt.plot([200,600], [0,0], 'b--')
	fig.suptitle('Flexure Correction', fontsize=20)
	fig.savefig('/Users/jmel/nires/plots/tspec_flexure_x2.pdf')

