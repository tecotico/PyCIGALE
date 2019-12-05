#!/usr/bin/env python3

import ctypes
import os
import sys
import getopt
import binascii
import base64
import time

from collections import namedtuple
from struct import *

import numpy as np

#from pyds9 import *
from astropy.io import fits

#------------------------------
HDRLEN = 256

#------------------------------

def usage():
    print('readNew.py -i <inputfile> -o <outputfile>')
    
#------------------------------

def myunpack(f, it, nv):
    global _unpack
    array_type = ctypes.c_int * nv
    _unpack.unpack_new(ctypes.c_int(f), array_type(it), ctypes.c_int(nv))
    '''
    num_numbers = len(numbers)
    array_type = ctypes.c_int * num_numbers
    result = _sum.our_function(ctypes.c_int(num_numbers), array_type(*numbers))
    return int(result)
    '''
    
#------------------------------

_unpack = ctypes.CDLL('./libcigaleLAMB.so')
_unpack.unpack_new.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int)

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


record_format = '3s5s5s5s238s'
record_size = calcsize(record_format)
result_list = []

# lectura del archivo
f = open(inputfile, "rb")
record = f.read(record_size)

result_list.append(unpack(record_format, record))
tipo = result_list[0][0]
dimx = int(result_list[0][1])
dimy = int(result_list[0][2])
ncan = int(result_list[0][3])
print(tipo)
print(dimx)
print(dimy)
print(ncan)

nv = dimx * dimy * ncan
print('nv: ', str(nv))

#--------------------------------------------

it = (ctypes.c_int * nv)()
data = unpack(str(nv)+'i', it)
img = np.zeros(nv, dtype=np.int32, order='C')
c_int_p = ctypes.POINTER(ctypes.c_int)
img_p = img.ctypes.data_as(c_int_p)
pointer, read_only_flag = img.__array_interface__['data']

f.seek(0, 0)
f.seek(256, 0)
_unpack.unpack_new(f.fileno(), ctypes.cast(pointer, ctypes.POINTER(ctypes.c_int)), nv)

f.close

img.shape = (ncan, dimy, dimx)

# se guarda en fits
hdu = fits.PrimaryHDU(img)
#utopia
#hdu.writeto('cie2.fits', clobber=True)
#tortuga
hdu.writeto(outputfile, overwrite=True)





