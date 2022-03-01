

import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')




# pk_cxi = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run118_peaks.txt')
# pk_cxi.plot_peaks()

# frames = pk_cxi.split_frames()
# frames[0].plot_peaks()


# # corr = scorpy.CorrelationVol(qmax= pk_cxi.qmax)
# # corr.fill_from_peakdata(pk_cxi, verbose=2)

# # corr.plot_sumax(2)
# # corr.plot_q1q2()


# geompath = f'{scorpy.DATADIR}/geoms/plot-test.geom'
# geo = scorpy.ExpGeom(f'{geompath}')
# pk_h5 = scorpy.PeakData(f'{scorpy.DATADIR}/patternsim/plot-test.h5', geo=geo)


# pk_h5.plot_peaks()
# pk_h5_int = pk_h5.integrate_peaks(0.005)
# pk_h5_int.plot_peaks()


geompath = f'{scorpy.DATADIR}/geoms/batch.geom'
geo = scorpy.ExpGeom(f'{geompath}')

qmax = 1
qmin = 0.01

frame = 1
pk = scorpy.PeakData(f'/tmp/corrbatch-{frame}.h5', geo=geo, qmax=qmax, qmin=qmin)
print(pk.df)
print(pk.scat_pol)
pk.plot_peaks()
pk.geo.plot_qring(qmax)
pk.geo.plot_qring(qmin)
pk_int = pk.integrate_peaks(0.005)

pk_int.plot_peaks()



plt.show()





