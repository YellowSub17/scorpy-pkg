import numpy as np
import h5py

import scorpy

import matplotlib.pyplot as plt
plt.close('all')







# geo = scorpy.ExpGeom(f'{scorpy.DATADIR}/geoms/single_square.geom')
# # pk = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run118_peaks.txt')
# # pk = scorpy.PeakData(f'{scorpy.DATADIR}/patternsim/plot-test.h5', geo=geo, qmax=1)

# pk = scorpy.PeakData(f'{scorpy.DATADIR}/patternsim/five-peaks.h5', geo=geo, qmax=1, qmin=0.01)
# pk.plot_peaks()


# corr1 = scorpy.CorrelationVol(nq=5, npsi=180, qmax=pk.qmax, cos_sample=False, inc_self_corr=False)
# for q in corr1.qpts[::2]:
    # pk.geo.plot_qring(q, ec='red')

# for q in corr1.qpts[1::2]:
    # pk.geo.plot_qring(q, ec='blue')

# for q in corr1.qpts[1:]:
    # pk.geo.plot_qring(q-corr1.dq/2, ec='black', ls='-')

# pk.geo.plot_qring(pk.qmax, ec='black', ls='-')
# pk.geo.plot_qring(0.01, ec='black', ls='-')



# corr1.fill_from_peakdata(pk, verbose=99)
# corr1.plot_q1q2(title='q1q2', xlabel='$\\Delta\\Psi$', ylabel='q1q2')
# print(corr1.qpts)







geo = scorpy.ExpGeom(f'{scorpy.DATADIR}/geoms/single_square.geom')
pk = scorpy.PeakData(f'{scorpy.DATADIR}/patternsim/plot-test.h5', geo=geo, qmin=0.01 )



pk.plot_peaks()

qs = [0.01, 0.25, 0.5, 0.75, 1]
for q in qs:
    pk.geo.plot_qring(q=q)















# corr2d = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/1vds-2d.dbin')
# corr2d.plot_q1q2(log=True)


# corr2d.vol[:,:,0:2]=0
# corr2d.plot_q1q2()


# corr3d = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/1vds-3d-qcor.dbin')
# corr3d.plot_q1q2(log=True)


# corr3d.vol[:,:,0:2]=0
# corr3d.plot_q1q2()







# q1 = corr2d.vol.sum(axis=-1).sum(axis=-1)
# q2 = corr3d.vol.sum(axis=-1).sum(axis=-1)

# q1 = corr2d.get_xy().sum(axis=-1)
# q2 = corr3d.get_xy().sum(axis=-1)

# plt.figure()
# plt.plot(np.log10(q1+1))
# plt.plot(np.log10(q2+1))









plt.show()

