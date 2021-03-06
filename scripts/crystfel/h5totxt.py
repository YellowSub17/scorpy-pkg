#!/usr/bin/env python3
'''
h5totxt.py

Convert a H5 generated from pattern_sim to an espk peaklist

Usage:
    h5totxt [infpath] [outfpath] [ncrystals]

    infpath: {path}/{tag}
    outfpath: {path}/{tag}
    ncrystals: int
'''



import sys
import scorpy
from scorpy.env import __DATADIR

import h5py
import matplotlib.pyplot as plt
import numpy as np



infpath = sys.argv[1]
outfpath = sys.argv[2]

if len(sys.argv)==4:
    ncrystals = int(sys.argv[3])
else:
    ncrystals = None





outf = open(f'{__DATADIR}/{outfpath}.txt', 'w')
outf.write('# #frameNumber, peak_x_raw, peak_y_raw, totalIntensity\n')


if ncrystals is None:
    h5f = h5py.File(f'{__DATADIR}/{infpath}.h5', 'r')
    data = h5f['entry_1/instrument_1/detector_1/data'][:]
    h5f.close()

    for peak_x_raw, peak_y_raw in zip(*np.where(data>0)):
        outf.write(f'{0} {peak_x_raw} {peak_y_raw} {data[peak_x_raw, peak_y_raw]}\n')

    outf.close()


else:
    for n in range(1, ncrystals+1):
        print(n)
        h5f = h5py.File(f'{__DATADIR}/{infpath}-{n}.h5', 'r')
        data = h5f['entry_1/instrument_1/detector_1/data'][:]
        h5f.close()

        for peak_x_raw, peak_y_raw in zip(*np.where(data>0)):
            outf.write(f'{n} {peak_x_raw} {peak_y_raw} {data[peak_x_raw, peak_y_raw]}\n')

    outf.close()



