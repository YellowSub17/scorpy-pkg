


import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')








geom = scorpy.ExpGeom(f'{scorpy.DATADIR}/test-data/test.geom')

pk = scorpy.PeakData(f'{scorpy.DATADIR}/test-data/runx_peaks.txt', geom=geom, qmax=0.9)

# print(pk.scat_pol)

frames = pk.split_frames()

# print(frames[0].scat_pol)



corr = scorpy.CorrelationVol(200, 90, 0.9, cos_sample=False)

corr.fill_from_peakdata(pk, verbose=2)

corr.plot_q1q2()

corr.plot_sumax(0)




pk.plot_peaks()
geom.plot_qring(0.9)

for pt in corr.ls_pts():
    print(pt)


print(corr.qpts)

plt.show()




