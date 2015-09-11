#!/usr/bin/env python
# Take difference between two fits files

import sys
from astropy.io import fits


order_image = fits.open('corrected.fits')
order_data = order_image[0].data

print order_data[0]
print order_data.shape
