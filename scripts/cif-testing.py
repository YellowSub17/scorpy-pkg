import scorpy
import matplotlib.pyplot as plt

import timeit






geo = scorpy.ExpGeom('../data/geoms/agipd_2304_vj_opt_v3.geom')
peakdata = scorpy.PeakData('../data/cxi/125/peaks.txt', geo)


frames = peakdata.split_frames()



corr1 = scorpy.CorrelationVol(qmax=1.4)
corr2 = scorpy.CorrelationVol(qmax=1.4)

t1 = timeit.timeit(
"""
for frame in frames:
    corr1.correlate_scat_pol(frame.scat_pol)
"""
                   , number=1, globals=globals())


t2 = timeit.timeit(
"""
for frame in frames:
    corr2.correlate_scat_pol2(frame.scat_pol)
"""
                   , number=1, globals=globals())



corr1.plot_sumax()
corr2.plot_sumax()
print(t1)
print(t2)

plt.show()




