import scorpy
import matplotlib.pyplot as plt

import timeit






geo = scorpy.ExpGeom('../data/geoms/agipd_2304_vj_opt_v3.geom')
peakdata = scorpy.PeakData('../data/cxi/125/peaks.txt', geo)

cif = scorpy.CifData('../data/xtal/1al1-sf.cif')

qmax = cif.qmax/4


frames = peakdata.split_frames()



corr1 = scorpy.CorrelationVol(qmax=qmax)
corr2 = scorpy.CorrelationVol(qmax=qmax)

t1 = timeit.timeit(
"""
corr1.correlate_scat_rect(cif.scat_rect)
"""
                   , number=1, globals=globals())


# t2 = timeit.timeit(
# """

# corr2.correlate_scat_rect2(cif.scat_rect)
# """
                   # , number=1, globals=globals())



corr1.plot_sumax()
corr2.plot_sumax()
print(t1)
print(t2)

plt.show()




