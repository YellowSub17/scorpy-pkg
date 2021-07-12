#!/usr/bin/env python3
'''
h5totxt.py

Convert a H5 generated from pattern_sim to an espk peaklist

Usage:
    h5totxt [infpath] [outfpath] [ncrystals]
'''



import sys
import scorpy
from scorpy.env import __DATADIR

import h5py
import matplotlib.pyplot as plt
import numpy as np



infpath = sys.argv[1]
outfpath = sys.argv[2]
ncrystals = sys.argv[3]



infname = f'{__DATADIR}/out.h5'
outfname = f'{__DATADIR}/out.txt'





h5f = h5py.File(infname, 'r')

data = h5f['entry_1/instrument_1/detector_1/data'][:]







f.close()

f = open(outfname, 'w')
f.write('# #frameNumber, peak_x_raw, peak_y_raw, totalIntensity\n')

for peak_x_raw, peak_y_raw in zip(*np.where(data>0)):
    f.write(f'{0} {peak_x_raw} {peak_y_raw} {data[peak_x_raw, peak_y_raw]}\n')

f.close()



geo = scorpy.ExpGeom(f'{__DATADIR}/geoms/agipd_2304_vj_opt_v3.geom')
# pk = scorpy.PeakData(outfname, geo, cxi_flag=False)

# plt.figure()
# ax = plt.axes()
# ax.set_facecolor('#000000')
# geo.plot_panels()
# pk.plot_peaks(cmap='summer')
# plt.colorbar()




pk = scorpy.PeakData(f'{scorpy.env.__DATADIR}/out.h5', geo)

plt.figure()
ax = plt.axes()
ax.set_facecolor('#000000')
geo.plot_panels()
pk.plot_peaks(cmap='summer')
plt.colorbar()



plt.show()


