#!/usr/bin/env python

import argparse
import numpy as np
from astropy.io import fits
import sys


#------------------------------
def usage():
    print 'fits2cigale.py -i <inputfile> -o <outputfile>'
    
#------------------------------
parser = argparse.ArgumentParser()

parser.add_argument('-i', '--ifile', dest='infits')
parser.add_argument('-o', '--ofile', dest='outcig')

p = parser.parse_args()

if not len(sys.argv) > 1:
    usage()
    sys.exit()

# p.infits <-- cubo fits input
# p.outcig <-- cubo cigale output

hdul = fits.open(p.infits)
tipoDefault = hdul[0].data.dtype
cols = hdul[0].header['NAXIS1']
rows = hdul[0].header['NAXIS2']
plns = hdul[0].header['NAXIS3']

#print tipoDefault
#print hdul[0].data.shape

output_file = open(p.outcig, 'wb')
commen = 'raw%5d%5d%5d         ' % (cols, rows, plns)
#         012         012345678
commen = commen + '\0' * 229
output_file.write(commen)
#output_file.write(hdul[0].data)
#output_file.write(hdul[0].data.astype(np.uint32))
output_file.write(np.uint32(hdul[0].data))
output_file.close()
