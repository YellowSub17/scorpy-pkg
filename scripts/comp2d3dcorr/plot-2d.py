import numpy as np
import h5py

import scorpy

import matplotlib.pyplot as plt
plt.close('all')













geo = scorpy.ExpGeom(f'{scorpy.DATADIR}/geoms/single_square.geom')
pk = scorpy.PeakData(f'{scorpy.DATADIR}/patternsim/plot-test.h5', geo=geo, qmin=0.01 )

# pk = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run118_peaks.txt')


pk.plot_peaks()

qs = [0.01, 0.25, 0.5, 0.75, 1]#, 1.25, 1.5, 1.75, 2]
for q in qs:
    pk.geo.plot_qring(q=q)







plt.show()

