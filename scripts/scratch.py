
import numpy as np
import pyshtools as pysh
import matplotlib.pyplot as plt

import scorpy







# geom = scorpy.ExpGeom('../data/geoms/agipd_2304_vj_opt_v3.geom')
# geom.plot_panels()
# pk = scorpy.PeakData(f'../data/espk/homebrew-peaks.txt', geom, cxi_flag=False)
# pk.plot_peaks()







# corr1 = scorpy.CorrelationVol(100,180, pk.qmax)
# corr1.fill_from_peakdata(pk, method='scat_sph', verbose=False)


# corr2 = scorpy.CorrelationVol(100,180, pk.qmax)
# corr2.fill_from_peakdata(pk, method='scat_pol', verbose=False)


# corr1.plot_q1q2()
# plt.title('3D spherical q1q2')
# corr2.plot_q1q2()
# plt.title('2D Polar q1q2')

# corr1.plot_sumax()
# plt.title('3D spherical sumax')
# corr2.plot_sumax()
# plt.title('2D Polar sumax')

# plt.show()




geom = scorpy.ExpGeom('../data/geoms/agipd_2304_vj_opt_v3.geom')
pk = scorpy.PeakData('../data/test/test-1.txt', geom, cxi_flag=False, qmax=3.5)

plt.figure()
geom.plot_panels()
pk.plot_peaks()
plt.title('seed 1')


corr = scorpy.CorrelationVol(path='../data/test/test-1_qcor')
corr.plot_q1q2()
plt.title('seed 1')


corr_sum = scorpy.CorrelationVol(100,180, 3.5)

for i in range(1, 65):
    print(i)
    corr1 = scorpy.CorrelationVol(path=f'../data/test/test-{i}_qcor')
    corr_sum.vol += corr1.vol

corr_sum.plot_q1q2()
plt.title('sum of seeds')

plt.figure()
plt.imshow(corr_sum.get_xy()[:, 5:-5], origin='lower', aspect='auto', 
           extent=[corr_sum.psipts[5], corr_sum.psipts[-5], 0, corr_sum.qmax])
plt.title('sum of seeds (cropped)')
plt.show()








