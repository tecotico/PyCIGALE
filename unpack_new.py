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

#------------------------------

def usage():
    print 'unpack_new.py -i <inputfile> -o <outputfile>'
    
#------------------------------

def readHeader(hdrdata):
    nbdim = unpack('3s', hdrdata[0:3])[0]
    '''
    id = unpack('8B', hdrdata[4:12])
    lx = unpack('i', hdrdata[12:16])[0]
    ly = unpack('i', hdrdata[16:20])[0]
    lz = unpack('i', hdrdata[20:24])[0]
    scale = unpack('f', hdrdata[24:28])[0]
    ix0 = unpack('i', hdrdata[28:32])[0]
    iy0 = unpack('i', hdrdata[32:36])[0]
    zoom = unpack('f', hdrdata[36:40])[0]
    comment = unpack('216B', hdrdata[40:])
    '''
    H = AdHdr(nbdim)
    return(H)
    
#------------------------------

try:
    options, args = getopt.getopt(sys.argv[1:], 'i:o:d', ['inputfile=', 'outputfile='])
    if not options:
        usage()
        sys.exit()
except getopt.GetoptError:
    usage()
    sys.exit()

for opt, arg in options:
    if opt in ('-i', '--inputfile'):
        inputfile = arg
    elif opt in ('-o', '--outputfile'):
        outputfile = arg
    else:
        usage()
        sys.exit()


fileinfo = os.stat(inputfile)

# lectura del archivo
f = open(inputfile, "rb")
record_format = '3s5s5s5s'
record_size = calcsize(record_format)
result_list = []
record = f.read(calcsize(record_format))
#tmphdr = f.read(HDRLEN)
#tmpdata = f.read(fileinfo.st_size - HDRLEN)
f.close
result_list.append(unpack(record_format, record))
# arreglo del encabezado
#tipo = unpack('3s', tmphdr[0:3])[0]
#print tipo
#dimx = int(tmphdr[3:7].encode('hex'), 16)
#print(dimx)
tipo = result_list[0][0]
dimx = int(result_list[0][1])
dimy = int(result_list[0][2])
ncan = int(result_list[0][3])
print tipo
print dimx
print dimy
print ncan




