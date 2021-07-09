#!/usr/bin/env python3
'''
hdf5_2_espk.py

Convert a H5 generated from pattern_sim to an espk peaklist
'''

import sys
import scorpy
from scorpy.env import __DATADIR

import h5py
import matplotlib.pyplot as plt
import numpy as np

# infname = sys.argv[1]
# outfname = sys.argv[2]

infname = f'{__DATADIR}/out.h5'
outfname = f'{__DATADIR}/out.txt'




print(infname)

f = h5py.File(infname, 'r')

data = f['entry_1/instrument_1/detector_1/data'][:]

if np.all(data==0):
    print('crash')
    sys.exit()






f.close()

f = open(outfname, 'w')
f.write('# #frameNumber, peak_x_raw, peak_y_raw, totalIntensity\n')

for peak_x_raw, peak_y_raw in zip(*np.where(data>0)):
    f.write(f'{0} {peak_x_raw} {peak_y_raw} {data[peak_x_raw, peak_y_raw]}\n')

f.close()



geo = scorpy.ExpGeom(f'{__DATADIR}/geoms/agipd_2304_vj_opt_v3.geom')
pk = scorpy.PeakData(outfname, geo, cxi_flag=False)

plt.figure()
ax = plt.axes()
ax.set_facecolor('#000000')
geo.plot_panels()
pk.plot_peaks(cmap='summer')
plt.colorbar()

plt.show()








