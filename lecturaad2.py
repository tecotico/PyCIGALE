#!/usr/bin/env python

from struct import *
import binascii
import base64

import sys

f = open("mask4.ad2", "rb")

# 1048576 = 512 * 512 * 4
data = f.read(512 * 512 * 4)
nbytes = 512*512
datos = unpack(str(nbytes)+'f', data)
# parece que tambien funciona
#import array
#U = array.array('H')
#U.fromstring(data)

# ad_trailer
print 'ad_trailer'
print '----------'
# la siguiente linea funciona bien en mi maquina con windows
#nbdim = unpack('l', f.read(4))[0]
# cambio 24/ago/2016
# para linux 64 bits hubo que cambiar el tipo de l a i
# incluyendo las demas lineas
nbdim = unpack('i', f.read(4))[0]
print nbdim
id = unpack('8B', f.read(8))
print id
lx = unpack('i', f.read(4))[0]
print lx
ly = unpack('i', f.read(4))[0]
print ly
lz = unpack('i', f.read(4))[0]
print lz
scale = unpack('f', f.read(4))[0]
print scale
ix0 = unpack('i', f.read(4))[0]
print ix0
iy0 = unpack('i', f.read(4))[0]
print iy0
zoom = unpack('f', f.read(4))[0]
print zoom

# ad2_trailer
print '\nad2_trailer'
print '----------'
modevis = unpack('i', f.read(4))[0]
print modevis
thrshld = unpack('f', f.read(4))[0]
print thrshld
step = unpack('f', f.read(4))[0]
print step
nbiso = unpack('i', f.read(4))[0]
print nbiso
pal = unpack('i', f.read(4))[0]
print pal
cdelt1 = unpack('d', f.read(8))[0]
print cdelt1
cdelt2 = unpack('d', f.read(8))[0]
print cdelt2
crval1 = unpack('d', f.read(8))[0]
print crval1
crval2 = unpack('d', f.read(8))[0]
print crval2
crpix1 = unpack('f', f.read(4))[0]
print crpix1
crpix2 = unpack('f', f.read(4))[0]
print crpix2
crota2 = unpack('f', f.read(4))[0]
print crota2
equinox = unpack('f', f.read(4))[0]
print equinox
x_mirror = unpack('B', f.read(1))[0]
print x_mirror
y_mirror = unpack('B', f.read(1))[0]
print y_mirror
was_compressed = unpack('B', f.read(1))[0]
print was_compressed
none2 = unpack('B', f.read(1))[0]
print none2
none = unpack('4i', f.read(16))
print none
comment = unpack('128B', f.read(128))
print comment

for i in range(10):
  print datos[i]
  
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#from matplotlib.pyplot import plot, draw, show
plt.ion()
plt.plot(datos[200])
plt.show()

print(type(datos), len(datos))

import numpy as np

a = np.asarray(datos)
print(a.shape)
a.shape = (512, 512)
print(type(a))
print(a.shape)

from astropy.io import fits

hdu = fits.PrimaryHDU(a)
hdu.writeto('mask4.fits')

from pyraf import iraf 

iraf.tv()
iraf.tv.display('mask4.fits',1)

plt.imshow(a, cmap='gray')
plt.colorbar()

