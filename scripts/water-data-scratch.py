
import matplotlib.pyplot as plt
plt.close('all')
import numpy as np
import h5py
import scorpy
import os


##type 1
fname = f'../data/h2o/cxi2510/output_r0144/type1/LCLS_2011_Feb28_r0144_162942_d41_cspad.h5'
fname = f'../data/h2o/cxi2510/output_r0144/type1/LCLS_2011_Feb28_r0144_162957_2322_cspad.h5'
fname = f'../data/h2o/cxi2510/output_r0144/type1/LCLS_2011_Feb28_r0144_163006_2feb_cspad.h5'


##type 2
# fname = f'../data/h2o/cxi2510/output_r0144/type2/LCLS_2011_Feb28_r0144_163311_1341c_cspad.h5'
# fname = f'../data/h2o/cxi2510/output_r0144/type2/LCLS_2011_Feb28_r0144_163302_1267b_cspad.h5'




h5f = h5py.File(fname,'r')
data = h5f['data/data'][:]
h5f.close()

plt.figure()
plt.imshow(data,)
plt.figure()
plt.imshow(np.log10(np.abs(data+1)))


xs = [
        850.42,
        1258,
        1269,
        876.2,
        475.7,
        460.2

        ]

ys = [
        387.54,
        587.3,
        1151.6,
        1352.1,
        1086.4,
        711.6,

        ]




# qt = scorpy.utils.utils.to_polar(data, 350, data.shape[0]/2, data.shape[1]/2)
qt = scorpy.utils.utils.to_polar(data, data.shape[0]/2, np.mean(xs), np.mean(ys))
plt.figure()
plt.imshow(qt)





imgs = [data]


corr = scorpy.CorrelationVol(nq=350, npsi=360, qmax=2, cos_sample=False)
corr.fill_from_detector_imgs(imgs, 350, data.shape[0]/2, data.shape[1]/2, verbose=99)

corr.vol[:, :, :1] *=0
corr.vol[:, :, -1:] *=0

corr.plot_sumax(2,log=True)


plt.show()







