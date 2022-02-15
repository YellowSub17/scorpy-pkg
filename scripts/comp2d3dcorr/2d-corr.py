import numpy as np
import h5py

import scorpy

import matplotlib.pyplot as plt
plt.close('all')















geo = scorpy.ExpGeom(f'{scorpy.DATADIR}/geoms/single_square.geom')
corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/1vds-2d-total-qcor.dbin')

for i in range(1, 1001):
    pk = scorpy.PeakData(f'/tmp/1vds-{i}.h5', geo=geo, qmax=1, qmin=0.01)


    print(i, end='\r')

    corr.fill_from_peakdata(pk, verbose=0)




corr.save(f'{scorpy.DATADIR}/dbins/1vds-2d-total-qcor.dbin')









plt.show()

