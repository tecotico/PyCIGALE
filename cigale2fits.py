#!/usr/bin/env python3

import ctypes
import os
import sys
import binascii
import base64
import time
import argparse

from collections import namedtuple
from struct import *

import numpy as np

from pyds9 import *
from astropy.io import fits

#------------------------------
HDRLEN = 256

#------------------------------

def usage():
    print('cigale2fits.py -i <inputfile> -o <outputfile>')
    
#------------------------------

def myunpack(f, it, nv):
    global _unpack
    array_type = ctypes.c_int * nv
    _unpack.unpack_new(ctypes.c_int(f), array_type(it), ctypes.c_int(nv))
    
#------------------------------

_unpack = ctypes.CDLL('./libcigaleLAMB.so')
_unpack.unpack_new.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int)

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--inputfile', dest='ifile')
parser.add_argument('-o', '--outputfile', dest='ofile')

p = parser.parse_args()

if p.ifile == None or p.ofile == None:
    usage()
    sys.exit(0) 

#------------------------------
#formato encabezado new de cigale
record_format = '3s5s5s5s238s'
record_size = calcsize(record_format)
print('record_size', record_size)
result_list = []

# lectura del archivo
f = open(p.ifile, "rb")
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
#print 'nv: ', str(nv)

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
print('shape', img.shape)

# se guarda en fits
hdu = fits.PrimaryHDU(img)
# python 2.7
#hdu.writeto(.ofile, clobber=True)
# 
hdu.writeto(p.ofile, overwrite=True)





