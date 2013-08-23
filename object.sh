#! /bin/csh -f
#
# set the object name on both NIRES spectrograph and NIRES field viewer
#
# written by Jason Melbourne 2013-08-16
#

modify -s nids object=$1
modify -s nsds object=$1
 
