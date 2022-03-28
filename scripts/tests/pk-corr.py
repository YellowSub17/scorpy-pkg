


import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')








geom = scorpy.ExpGeom(f'{scorpy.DATADIR}/test-data/test.geom')

pk = scorpy.PeakData(f'{scorpy.DATADIR}/test-data/runx_peaks.txt', geom=geom, qmax=0.9, qmin=0.001)
print(pk.scat_pol)


frames = pk.split_frames()




corr = scorpy.CorrelationVol(50, 90, 0.9, cos_sample=False)

corr.fill_from_peakdata(pk, verbose=2)

corr.plot_q1q2(title='q1q2')

corr.plot_sumax(0, title='sumax')






pk.plot_peaks()
geom.plot_qring(0.9)

plt.show()




