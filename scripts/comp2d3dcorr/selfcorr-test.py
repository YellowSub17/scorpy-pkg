
import numpy as np
import scorpy
import matplotlib.pyplot as plt
plt.close('all')






# method = 'scat_sph'

# cif = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/inten1-qmax1-sf.cif', qmax=0.264)

# corr1 = scorpy.CorrelationVol(100, 180, 0.264, cos_sample=False, inc_self_corr=True)
# corr1.fill_from_cif(cif, method=method)
# corr2 = scorpy.CorrelationVol(100, 180, 0.264, cos_sample=False, inc_self_corr=False)
# corr2.fill_from_cif(cif, method=method)

# corr1.plot_q1q2()
# corr2.plot_q1q2()

method= 'scat_pol'

geom = scorpy.ExpGeom(f'{scorpy.DATADIR}/geoms/plot-test.geom')
pk = scorpy.PeakData(f'{scorpy.DATADIR}/patternsim/plot-test.h5', geo=geom)
pk.plot_peaks()



corr1 = scorpy.CorrelationVol(100, 180, 1.48, cos_sample=False, inc_self_corr=True)
corr1.fill_from_peakdata(pk, method=method)

corr2 = scorpy.CorrelationVol(100, 180, 1.48, cos_sample=False, inc_self_corr=False)
corr2.fill_from_peakdata(pk, method=method)


corr1.plot_q1q2()
corr2.plot_q1q2()




plt.show()
