import numpy as np
import scorpy
from scorpy.env import __DATADIR
import matplotlib.pyplot as plt
import time







geo = scorpy.ExpGeom(f'{__DATADIR}/geoms/agipd_2304_vj_opt_v3.geom')

cif = scorpy.CifData(f'{__DATADIR}/xtal/1vds_fj-sf.cif')

pk = scorpy.PeakData(f'{__DATADIR}/ensemble_peaks/n1024/peaks_1024_9.txt', geo, cxi_flag=False)


# plt.figure()
# plt.hist(cif.scat_sph[:,0], bins=100)
# plt.title('cif qmag hist')
# plt.xlabel('q')
# plt.ylabel('frequency')

# plt.figure()
# plt.hist(pk.scat_pol[:,0], bins=100)
# plt.title('peakdata qmag hist')
# plt.xlabel('q')
# plt.ylabel('frequency')



# corr1 = scorpy.CorrelationVol(100,180, qmax=qmax)
# corr2 = scorpy.CorrelationVol(100,180, qmax=qmax)

# print('Correlating cif')
# print(time.asctime())
# corr1.fill_from_cif(cif)

# print('Correlating pk')
# print(time.asctime())
# corr2.fill_from_peakdata(pk)

# corr1.save(f'{__DATADIR}/dbins/comp_epvscif_cif.dbin')
# corr2.save(f'{__DATADIR}/dbins/comp_epvscif_ep.dbin')

# corr1 = scorpy.CorrelationVol(path = f'{__DATADIR}/dbins/comp_epvscif_cif.dbin')
# corr2 = scorpy.CorrelationVol(path = f'{__DATADIR}/dbins/comp_epvscif_ep.dbin')

# corr1.plot_q1q2()
# corr2.plot_q1q2()

plt.show()






