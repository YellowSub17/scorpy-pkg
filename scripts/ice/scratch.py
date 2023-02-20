import numpy as np
import scorpy
import os
import h5py


import utils
import matplotlib.pyplot as plt
plt.close('all')

### make



utils.write_geom(clen=0.18, photonenergy=9300, pixsize=2e-4, npix=1024)
geom = scorpy.ExpGeom(f'{scorpy.DATADIR}/ice/sim/detector.geom')
geom.plot_panels()

for q in [0.5, 1,1.5, 2, 2.25]:
    geom.plot_qring(q=q)


utils.gen_pattern(size=5, nphotons=1e26, pdb='hex-ice')

# with h5py.File(f'{scorpy.DATADIR}/ice/sim/x.h5', 'r') as h5file:

    # data = h5file['/entry_1/instrument_1/detector_1/data'][:]


# print(data.max())
# print(data.min())

# plt.figure()
# plt.imshow(np.log10(np.abs(data)+1))
# plt.colorbar()


print('\nmaking pk')
pk = scorpy.PeakData(f'{scorpy.DATADIR}/ice/sim/x.h5', geom=geom, qmax=2.25)


pk.plot_peaks()


plt.show()

