#!/usr/bin/env python

import os
import sys
import getopt
import binascii
import base64

from collections import namedtuple
from struct import *

import numpy as np

from pyds9 import *
from astropy.io import fits

#------------------------------
HDRLEN = 256
displayImgDS9 = False
inputfile = ''
outputfile = 'tmp.fits'
AdHdr = namedtuple('adhdr', ['nbdim', 'id', 'lx', 'ly', 'lz', 'scale', 'ix0', 'iy0', 'zoom'])

#------------------------------

def usage():
    print 'ad2fits.py -i <inputfile> -o <outputfile>'
    
#------------------------------

try:
    options, args = getopt.getopt(sys.argv[1:], 'i:o:d', ['inputfile=', 'outputfile=', 'display'])
    if not options:
        usage()
        sys.exit()
except getopt.GetoptError:
    usage()
    sys.exit()

for opt, arg in options:
    if opt in ('-d', '--display'):
        displayImgDS9 = True
    elif opt in ('-i', '--inputfile'):
        inputfile = arg
    elif opt in ('-o', '--outputfile'):
        outputfile = arg
    else:
        usage()
        sys.exit()


fileinfo = os.stat(inputfile)
fileinfo.st_size

f = open(inputfile, "rb")
#data = f.read(fileinfo.st_size - HDRLEN)

#lectura del encabezado
f.seek(fileinfo.st_size - HDRLEN, 0)
nbdim = unpack('i', f.read(4))[0]
id = unpack('8B', f.read(8))
lx = unpack('i', f.read(4))[0]
ly = unpack('i', f.read(4))[0]
lz = unpack('i', f.read(4))[0]
scale = unpack('f', f.read(4))[0]
ix0 = unpack('i', f.read(4))[0]
iy0 = unpack('i', f.read(4))[0]
zoom = unpack('f', f.read(4))[0]


# lectura de los datos
f.seek(0, 0)
data = unpack(str(lx * ly * lz)+'f', f.read(lx * ly * lz * 4))

imgArr = np.asarray(data)
if (hdr.lz == 1):
    imgArr.shape = (hdr.lx, hdr.ly)
else:
    imgArr.shape = (hdr.lx, hdr.ly, hdr.lz)

# se abre un ds9
if displayImgDS9:
    d = DS9()
    d.set_np2arr(imgArr)

# se guarda en fits
hdu = fits.PrimaryHDU(imgArr)
hdu.writeto(outputfile, clobber=True)
