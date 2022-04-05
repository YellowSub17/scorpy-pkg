


import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')








# geom = scorpy.ExpGeom(f'{scorpy.DATADIR}/test-data/test.geom')

pk = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run125_peaks.txt', qmax=1.45, qmin=0.001)


corr1 = scorpy.CorrelationVol(100, 180, 1.45, cos_sample=False)
corr1.fill_from_peakdata(pk, verbose=1, method='scat_pol')

# corr2 = scorpy.CorrelationVol(100, 180, 1.45, cos_sample=False)
# corr2.fill_from_peakdata(pk, verbose=1, method='scat_sph')




corr3 = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/cxi/qcors/125/run125-qcor.dbin')



corr1.plot_q1q2(log=True)
# corr2.plot_q1q2(log=True)
corr3.plot_q1q2(log=True)





# pk.plot_peaks()
# pk.geom.plot_qring(0.9)

plt.show()




