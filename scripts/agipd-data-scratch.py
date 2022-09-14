


import scorpy

import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

import h5py

from extra_geom import AGIPD_1MGeometry
# from extra_data import open_run, stack_detector_data
import extra_data



geomfilename = scorpy.DATADIR / 'agipd/agipd_vds.geom'
geom = AGIPD_1MGeometry.from_crystfel_geom(geomfilename)
# geom.inspect()


h5filename = scorpy.DATADIR / 'agipd/RAW-R0079-AGIPD00-S00023.h5'


run = extra_data.H5File(h5filename, inc_suspect_trains=True)

sel = run.select('*AGIPD1M-1/DET/*', 'image.data')

train_id, data = sel.train_from_index(0)

# for train_id, train_data in sel.trains(require_all=True):
    # # print(f'found train id: {train_id} {train_data}')
    # break



modules_data = extra_data.stack_detector_data(data, 'image.data')

# data = modules_data[0]


res, center = geom.position_modules(modules_data)


im = res[0,0,:,:]

im[300:400, 700:800] = 0.75*np.max(im)
# im[400:500, 300:400] = 0.75*np.max(im)
im[900:1000, 300:400] = 0.75*np.max(im)

# im[300:400, 900:1000] = 0.75*np.max(im)




plt.figure()
plt.imshow(im, origin='lower')


im_unwrap = scorpy.utils.utils.to_polar(im, 500, center[0], center[1])

plt.figure()
plt.imshow(im_unwrap, origin='lower')



corr = scorpy.CorrelationVol(500, 360, 500, cos_sample=False)

corr.correlate_convolve(im_unwrap)
corr.qpsi_correction()

corr.vol[:, :, :50] = 0
corr.vol[:, :, -50:] = 0

corr.plot_q1q2()

corr.plot_slice(2, 180)

corr.plot_sumax(0)


plt.show()










# plt.show()
