#!/usr/bin/python -tt
#=======================================================================
#                        General Documentation

"""Single-function module.

   See function docstring for description.
"""

#-----------------------------------------------------------------------
#                       Additional Documentation
#
# RCS Revision Code:
#   $Id: findgen.py,v 1.1 2004/03/17 00:51:34 jlin Exp $
#
# Modification History:
# - 16 Mar 2004:  Original by Johnny Lin, Computation Institute,
#   University of Chicago.  Passed passably reasonable tests.
#
# Notes:
# - Written for Python 2.2.2.
# - Module docstrings can be tested using the doctest module.  To
#   test, execute "python findgen.py".
# - See import statements throughout for packages/modules required.
#
# Copyright (c) 2004 by Johnny Lin.  For licensing, distribution 
# conditions, contact information, and additional documentation see
# the URL http://www.johnny-lin.com/py_pkgs/gemath/doc/.
#=======================================================================




#----------------------- Overall Module Imports ------------------------

#- Set module information to package information, as applicable:

import gemath_version
__version__ = gemath_version.version
__author__  = gemath_version.author
__date__    = gemath_version.date
__credits__ = gemath_version.credits
del gemath_version




#--------------------------- General Function --------------------------

def findgen(shape):
    """Create a Float32 array of shape filled with 1-D indices.

    Output is a single-precision floating point Numeric array with
    shape given by argument shape, where the elements of the array
    are filled with the values of the 1-D indices that would be 
    given in a Numeric.ravel()ed version of the array.  This function 
    is similar in purpose to the IDL FINDGEN function.
    
    Positional Input Argument:
    * shape:   If is 1-D tuple of integers, argument specifies the 
      shape of the output array.  If argument shape is a scalar, the
      output array is a 1-D vector with argument shape number of
      elements.

    Examples:
    >>> from findgen import findgen
    >>> array = findgen(5)
    >>> ['%.1f' % array[i] for i in range(len(array))]
    ['0.0', '1.0', '2.0', '3.0', '4.0']
    >>> array.shape
    (5,)
    >>> array.typecode()
    'f'

    >>> array = findgen((3,4))
    >>> ['%.1f' % array[0,i] for i in range(4)]
    ['0.0', '1.0', '2.0', '3.0']
    >>> ['%.1f' % array[1,i] for i in range(4)]
    ['4.0', '5.0', '6.0', '7.0']
    >>> ['%.1f' % array[2,i] for i in range(4)]
    ['8.0', '9.0', '10.0', '11.0']
    >>> array.shape
    (3, 4)
    """
    import numpy as N

    if type(shape) != type(()):  shape_use = (shape,)
    else:  shape_use = shape

    tot_nelem = N.product(N.array(shape_use))
    tmp = N.arange(tot_nelem, typecode=N.Float32)
    
    return N.reshape(tmp, shape_use)




#-------------------------- Main:  Test Module -------------------------

#- Define additional examples for doctest to use:

__test__ = { 'Additional Examples':
    """
    >>> from findgen import findgen
    >>> array = findgen(5,4)
    Traceback (most recent call last):
        ...
    TypeError: findgen() takes exactly 1 argument (2 given)

    >>> import Numeric as N
    >>> array = findgen((3,4,2))
    >>> print N.sum(N.ravel(array) == N.arange(24))
    24
    """ }


#- Execute doctest if module is run from command line:

if __name__ == "__main__":
    """Test the module.

    Tests the examples in all the module documentation 
    strings, plus __test__.

    Note:  To help ensure that module testing of this file works, the
    parent directory to the current directory is added to sys.path.
    """
    import doctest, sys, os
    sys.path.append(os.pardir)
    doctest.testmod(sys.modules[__name__])




# ===== end file =====
