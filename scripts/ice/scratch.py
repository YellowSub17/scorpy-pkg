import numpy as np
import scorpy
import os
import h5py


import utils
import matplotlib.pyplot as plt
plt.close('all')

### make



utils.write_geom()
geom = scorpy.ExpGeom(f'{scorpy.DATADIR}/ice/sim/detector.geom')
geom.plot_panels()

for q in [0.5, 1,1.5, 2, 2.25]:
    geom.plot_qring(q=q)


# utils.gen_pattern(size=10, nphotons=1e22, pdb='hex-ice')

with h5py.File(f'{scorpy.DATADIR}/ice/sim/test-pattern.h5', 'r') as h5file:

    data = h5file['/entry_1/instrument_1/detector_1/data'][:]


print(data.max())
print(data.min())

plt.figure()
plt.imshow(data)


pk = scorpy.PeakData(f'{scorpy.DATADIR}/ice/sim/test-pattern.h5', geom=geom, qmax=2.25)


pk.plot_peaks()


plt.show()

