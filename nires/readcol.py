"""
readcol.py by Adam Ginsburg (keflavich@gmail.com)

readcol is meant to emulate IDL's readcol.pro, but is more capable and
flexible.  It is not a particularly "pythonic" program since it is not modular.
For a modular ascii table reader, http://cxc.harvard.edu/contrib/asciitable/ is
probably better.  This single-function code is probably more intuitive to an
end-user, though.
"""
import string,re,sys
import numpy
try:
    from scipy.stats import mode
    hasmode = True
except ImportError:
    #print "scipy could not be imported.  Your table must have full rows."
    hasmode = False
except ValueError:
    #print "error"
    hasmode = False

def readcol(filename,skipline=0,skipafter=0,names=False,fsep=None,twod=True,
        fixedformat=None,asdict=False,comment='#',verbose=True,nullval=None,
        asStruct=False):
    """
    The default return is a two dimensional float array.  If you want a list of
    columns output instead of a 2D array, pass 'twod=False'.  In this case,
    each column's data type will be automatically detected.
    
    Example usage:
    CASE 1) a table has the format:
     X    Y    Z
    0.0  2.4  8.2
    1.0  3.4  5.6
    0.7  3.2  2.1
    ...
    names,(x,y,z)=readcol("myfile.tbl",names=True,twod=False)
    or
    x,y,z=readcol("myfile.tbl",skipline=1,twod=False)
    or 
    names,xx = readcol("myfile.tbl",names=True)
    or
    xxdict = readcol("myfile.tbl",asdict=True)
    or
    xxstruct = readcol("myfile.tbl",asStruct=True)

    CASE 2) no title is contained into the table, then there is
    no need to skipline:
    x,y,z=readcol("myfile.tbl")
    
    CASE 3) there is a names column and then more descriptive text:
     X      Y     Z
    (deg) (deg) (km/s) 
    0.0    2.4   8.2
    1.0    3.4.  5.6
    ...
    then use:
    names,x,y,z=readcol("myfile.tbl",names=True,skipline=1,twod=False)
    or
    x,y,z=readcol("myfile.tbl",skipline=2,twod=False)

    INPUTS:
        fsep - field separator, e.g. for comma separated value (csv) files
        skipline - number of lines to ignore at the start of the file
        names - read / don't read in the first line as a list of column names
                can specify an integer line number too, though it will be 
                the line number after skipping lines
        twod - two dimensional or one dimensional output
        nullval - if specified, all instances of this value will be replaced
           with a floating NaN
        asdict - zips names with data to create a dict with column headings 
            tied to column data.  If asdict=True, names will be set to True
        asStruct - same as asdict, but returns a structure instead of a dictionary
            (i.e. you call struct.key instead of struct['key'])
        fixedformat - if you have a fixed format file, this is a python list of 
            column lengths.  e.g. the first table above would be [3,5,5].  Note
            that if you specify the wrong fixed format, you will get junk; if your
            format total is greater than the line length, the last entries will all
            be blank but readcol will not report an error.

    If you get this error: "scipy could not be imported.  Your table must have
    full rows." it means readcol cannot automatically guess which columns
    contain data.  If you have scipy and columns of varying length, readcol will
    read in all of the rows with length=mode(row lengths).
    """
    f=open(filename,'r').readlines()
    
    null=[f.pop(0) for i in range(skipline)]

    if names or asdict or asStruct:
        # can specify name line 
        if type(names) == type(1):
            nameline = f.pop(names)
        else:
            nameline = f.pop(0)
        if nameline[0]==comment:
            nameline = nameline[1:]
        nms=nameline.split(fsep)

    null=[f.pop(0) for i in range(skipafter)]

    commentfilter = make_commentfilter(comment)
    
    if fixedformat:
        myreadff = lambda(x): readff(x,fixedformat)
        splitarr = map(myreadff,f)
        splitarr = filter(commentfilter,splitarr)
    else:
        fstrip = map(string.strip,f)
        fseps = [ fsep for i in range(len(f)) ]
        splitarr = map(string.split,fstrip,fseps)
        for i in xrange(splitarr.count([''])):
            splitarr.remove([''])

        splitarr = filter(commentfilter,splitarr)

        # check to make sure each line has the same number of columns to avoid 
        # "ValueError: setting an array element with a sequence."
        nperline = map(len,splitarr)
        if hasmode:
            ncols,nrows = mode(nperline)
            if nrows != len(splitarr):
                if verbose:
                    print "Removing %i rows that don't match most common length.  \
                     \n%i rows read into array." % (len(splitarr) - nrows,nrows)
                for i in xrange(len(splitarr)-1,-1,-1):  # need to go backwards
                    if nperline[i] != ncols:
                        splitarr.pop(i)

    try:
        x = numpy.asarray( splitarr , dtype='float')
    except ValueError:
        if verbose: 
            print "WARNING: reading as string array because %s array failed" % 'float'
        try:
            x = numpy.asarray( splitarr , dtype='S')
        except ValueError:
            if hasmode:
                raise Exception( "ValueError when converting data to array." + \
                        "  You have scipy.mode on your system, so this is " + \
                        "probably not an issue of differing row lengths." )
            else:
                raise Exception( "Conversion to array error.  You probably " + \
                        "have different row lengths and scipy.mode was not " + \
                        "imported." )

    if nullval is not None:
        x[x==nullval] = numpy.nan
        x = get_autotype(x)

    if asdict or asStruct:
        mydict = dict(zip(nms,x.T))
        for k,v in mydict.iteritems():
            mydict[k] = get_autotype(v)
        if asdict:
            return mydict
        elif asStruct:
            return Struct(mydict)
    elif names and twod:
        return nms,x
    elif names:
        # if not returning a twod array, try to return each vector as the spec. type
        return nms,[ get_autotype(x.T[i]) for i in xrange(x.shape[1]) ]
    else:
        if twod:
            return x
        else:
            return [ get_autotype(x.T[i]) for i in xrange(x.shape[1]) ]

def get_autotype(arr):
    """
    Attempts to return a numpy array converted to the most sensible dtype
    Value errors will be caught and simply return the original array
    Tries to make dtype int, then float, then no change
    """
    try:
        narr = arr.astype('float')
        if (narr < sys.maxint).all() and (narr % 1).sum() == 0:
            return narr.astype('int')
        else:
            return narr
    except ValueError:
        return arr

class Struct(object):
    """
    Simple struct intended to take a dictionary of column names -> columns
    and turn it into a struct by removing special characters
    """
    def __init__(self,namedict):
        R = re.compile('\W')  # find and remove all non-alphanumeric characters
        for k in namedict.keys():
            v = namedict.pop(k) 
            if k[0].isdigit():
                k = 'n'+k
            namedict[R.sub('',k)] = v  
        self.__dict__ = namedict

def readff(s,format):
    """
    Fixed-format reader
    Pass in a single line string (s) and a format list, 
    which needs to be a python list of string lengths 
    """

    F = numpy.array([0]+format).cumsum()
    bothF = zip(F[:-1],F[1:])
    strarr = [s[l:u] for l,u in bothF]

    return strarr

def make_commentfilter(comment):
    if comment is not None:
        def commentfilter(a):
            try: return comment.find(a[0][0])
            except: return -1
        return commentfilter
    else: # always return false 
        return lambda(x): -1


