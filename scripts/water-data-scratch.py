
import matplotlib.pyplot as plt
plt.close('all')
import numpy as np
import h5py
import scorpy
import os


##type 1
fname = f'../data/h2o/cxi2510/output_r0144/type1/LCLS_2011_Feb28_r0144_162942_d41_cspad.h5'
# fname = f'../data/h2o/cxi2510/output_r0144/type1/LCLS_2011_Feb28_r0144_162957_2322_cspad.h5'
fname = f'../data/h2o/cxi2510/output_r0144/type1/LCLS_2011_Feb28_r0144_163006_2feb_cspad.h5'


##type 3
fname = f'../data/h2o/cxi2510/output_r0144/type3/LCLS_2011_Feb28_r0144_163049_6ba9_cspad.h5'
# fname = f'../data/h2o/cxi2510/output_r0144/type3/LCLS_2011_Feb28_r0144_163146_bc8b_cspad.h5'



h5f = h5py.File(fname,'r')
data = h5f['data/data'][:]
h5f.close()



# loc = np.where(data>1000)
# loc2 = np.where(data<=1000)
# data[loc] = 10
# data[loc2] =0

plt.figure()
# plt.imshow(np.log10(data +1))
plt.imshow(data)
plt.title('data (type 3)')




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




# qt = scorpy.utils.utils.to_polar(data, 600, np.mean(xs), np.mean(ys))
# qt = scorpy.utils.utils.to_polar(data, 600, 871.9, 884.8)
# qt = scorpy.utils.utils.to_polar(data, 600, data.shape[0]/2, data.shape[1]/2)
qt = scorpy.utils.utils.to_polar(data, 600, 884.8, 871.9)




# qt[440:500,33:40] = 1
# qt[440:500,90:96] = 1
# qt[440:500,145:152] = 1
# qt[440:500,204:214] = 1
# qt[440:500,265:273] = 1
# qt[440:500,318:324] = 1

plt.figure()
plt.imshow(qt, origin='lower')
plt.title('data unwrapped')
plt.xlabel('theta (0-360 degrees)')
plt.ylabel('radial pixels')

# plt.figure()
# plt.imshow(np.log10(np.abs(qt+1)))
# plt.title('log data unwrap')








imgs = [data]


corr = scorpy.CorrelationVol(nq=600, npsi=360, qmax=600, cos_sample=False)
corr.fill_from_detector_imgs(imgs, np.mean(xs), np.mean(ys) , verbose=99)


# corr.qpsi_correction()

corr.vol[:, :, :1] *=0
corr.vol[:, :, -1:] *=0

# corr.plot_sumax(0,log=True, title='sum ax')
corr.plot_q1q2(vminmax=(1e-9, 5e-1), title='q1q2 (minus t mean)', subtmean=True)


plt.figure()
plt.plot(corr.get_xy()[168, :])
plt.title('q1q2 lineplot (q=168)')
plt.xlabel('psi (0-180 degrees)')
plt.ylabel('correlation intensity')




plt.show()







