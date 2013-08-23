#!/usr/bin/env python



import numpy
import os
import shlex
import subprocess
import time
import logging as lg

class ds9:
	title = None
	'''
	The ds9 class provides wrappers around the unix commands xpaget
	and xpaset. The class is smart enough to automatically detect
	a running ds9 and attach automatically displayed images to it
	'''
	def __init__(self, title):
		''' ds9 construction init checks to see if a ds9 called title
		is currently running. If not, a new ds9 instance is created with
		that title'''
		self.title = title
		print 'yep'
		cmd = shlex.split("/usr/local/bin/xpaget %s" % self.title)
		retcode = subprocess.call(cmd)
		if retcode == 1:
			subprocess.Popen(["ds9", "-title", self.title])
			time.sleep(5)
			if self.title == "Spectrograph":
				self.xpaset("width 1250")
				self.xpaset("height 400")
				self.xpaset("scale zscale")
				self.xpaset("colorbar NO")
				self.xpaset("zoom 0.58 0.58")
			if self.title == "Viewer":
				self.xpaset("width 560")
				self.xpaset("height 512")
				self.xpaset("scale zscale")
				self.xpaset("colorbar NO")
				self.xpaset("zoom 0.5 0.5")
				#self.xpaset("rotate 270")
				

	def xpaget(self, cmd):
		'''xpaget is a convenience function around unix xpaget'''
		cmd = shlex.split("/usr/local/bin/xpaget %s %s" % (self.title, cmd))
		retcode = subprocess.call(cmd)

	def xpapipe(self, cmd, pipein):
		''' xpapipe is a convenience wrapper around echo pipein | xpaset ...'''
		
		cmd = shlex.split('/usr/local/bin/xpaset %s %s' % (self.title, cmd))
		p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		p.stdin.write(pipein)
		p.stdin.flush()
		# print p.communicate()


	def xpaset(self, cmd):
		'''xpaget is a convenience function around unix xpaset'''
		xpacmd = "/usr/local/bin/xpaset -p %s %s" % (self.title, cmd)
		lg.debug(xpacmd)

		cmd = shlex.split(xpacmd)
		retcode = subprocess.call(cmd)
		lg.debug("retcode = %s" % retcode) 


	def frameno(self, frame):
		'''frameno sets the ds9 frame number to [frame]'''
		self.xpaset("frame %i" %frame)

	def open(self, fname, frame):
		'''open opens a fits file [fname] into frame [frame]'''
		self.frameno(frame)
		print 'hm'
		self.xpaset("file %s" % fname)
		if self.title=="Spectrograph":
			self.xpaset("pan 000 190")	
			self.xpaset("orient xy")
		if self.title=="Viewer":
			self.xpaset("pan 000 000")	

	def wavedisp(self):
		self.xpaset("regions /Users/jmel/nires/calibrations/tspec_wavelength.reg")

	def emissiondisp(self):
		self.xpaset("regions delete all")
		self.xpaset("regions /Users/jmel/nires/calibrations/tspec_wavelength.reg")		
		self.xpaset("regions /Users/jmel/nires/calibrations/z_emission.reg")

	def zdisp(self):
		self.xpaset("regions delete all")
		self.xpaset("regions /Users/jmel/nires/calibrations/tspec_wavelength.reg")
		self.xpaset("regions /Users/jmel/nires/calibrations/zregion.reg")

	def cuDisp(self,x,y,size=15,group="foo1",label='1',color="white"):
		font="helvetica 16 normal"
		s="regions command '{box %d %d %d %d # color=%s tag=%s width=2 font=\"%s\" text=\"%s\"}'" \
			% (x,y,size,size,color,group,font,label)
		self.xpaset(s)

	def cuLabel(self,x,y,label="1",group="group1",color="white"):
		font="helvetica 16 normal"
		s="regions command '{text %d %d # color=%s tag=%s width=2 font=\"%s\" text=\"%s\" }'" % (x,y,color,group,font,label)
		self.xpaset(s)

	def cuDel(self,group):
		if group=='all':
			s="regions delete all" 
		else:
			s="regions group %s delete" % (group)
		self.xpaset(s)

	def cuCent(self,group):
		s="regions group %s select" % (group)
		self.xpaset(s)
		s="regions centroid radius 5 iterations 5"
		self.xpaset(s)
		s="regions selectnone"
		self.xpaset(s)

	def cuInfo(self,group):
		s="regions group %s select" % (group)
		self.xpaset(s)
		self.xpaset('regions getinfo')

	def regSave(self,file='ds9'):
		self.xpaset('regions save '+file+'.reg')

	def regOpen(self,file='ds9'):
		self.xpaset('regions load '+file+'.reg')

	def lindisp(self,dmin,dmax):
		self.xpaset('scale linear')
		s='scale limits %d %d' % (dmin,dmax)
		self.xpaset(s)


			    
		#xpacmd = 'echo "box %i %i %i %i" | xpaset %s regions' % (x,y,size,size,self.title)
		#cmd = shlex.shlex(xpacmd)
		#cmd.quotes = '"'
		#cmd2=list(cmd)
		#print cmd2
		# retcode = subprocess.call(cmd2)
