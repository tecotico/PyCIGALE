#!/usr/bin/env python

import os
import sys
import getopt
import binascii
import base64
import time

from collections import namedtuple
from struct import *

import numpy as np

from pyds9 import *
from astropy.io import fits

#------------------------------
HDRLEN = 256
displayImgDS9 = False
displayMovieDS9 = False
inputfile = ''
outputfile = 'tmp.fits'
AdHdr = namedtuple('adhdr', ['nbdim', 'id', 'lx', 'ly', 'lz', 'scale', 'ix0', 'iy0', 'zoom'])

#------------------------------

def usage():
    print 'ad3fits.py -i <inputfile> -o <outputfile>'
    
#------------------------------

def readHeader(hdrdata):
    nbdim = unpack('i', hdrdata[0:4])[0]
    id = unpack('8B', hdrdata[4:12])
    lx = unpack('i', hdrdata[12:16])[0]
    ly = unpack('i', hdrdata[16:20])[0]
    lz = unpack('i', hdrdata[20:24])[0]
    scale = unpack('f', hdrdata[24:28])[0]
    ix0 = unpack('i', hdrdata[28:32])[0]
    iy0 = unpack('i', hdrdata[32:36])[0]
    zoom = unpack('f', hdrdata[36:40])[0]
    comment = unpack('216B', hdrdata[40:])
    H = AdHdr(nbdim, id, lx, ly, lz, scale, ix0, iy0, zoom)
    return(H)

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

# lectura del archivo
f = open(inputfile, "rb")
tmpdata = f.read(fileinfo.st_size - HDRLEN)
tmphdr = f.read(HDRLEN)
f.close

# arreglo del encabezado
hdr = readHeader(tmphdr)

# arreglo de los datos
data = unpack(str(hdr.lx * hdr.ly * hdr.lz)+'f', tmpdata)
imgArr = np.asarray(data)
if (hdr.lz == 1):
    imgArr.shape = (hdr.lx, hdr.ly)
else:
    imgArr.shape = (hdr.lx, hdr.ly, hdr.lz)

# se abre un ds9
if displayImgDS9:
    d = DS9()
    if hdr.lz == 1: 
        d.set_np2arr(imgArr)
    elif hdr.lz > 1:
        d.set_np2arr(imgArr[:, :, 0])
    d.set('zoom to fit')

# se guarda en fits
hdu = fits.PrimaryHDU(imgArr)
hdu.writeto(outputfile, clobber=True)

# despliega la superficie
'''
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

xx, yy = np.mgrid[0:imgArr.shape[0], 0:imgArr.shape[1]]
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(xx, yy, imgArr, rstride=1, cstride=1, cmap=plt.cm.gray, linewidth=0)

# show it
plt.show()
'''
