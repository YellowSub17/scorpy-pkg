import numpy as np
import scorpy
from scorpy.env import __DATADIR
import matplotlib.pyplot as plt







geo = scorpy.ExpGeom(f'{__DATADIR}/geoms/agipd_2304_vj_opt_v3.geom')

cif = scorpy.CifData(f'{__DATADIR}/xtal/1vds_fj-sf.cif')


pk = scorpy.PeakData(f'{__DATADIR}/ensemble_peaks/n256/peaks_256_0.txt', geo, cxi_flag=False)


plt.figure()
plt.title('N=4, seed0')
geo.plot_panels()
pk.split_frames()[0].plot_peaks()
pk.split_frames()[1].plot_peaks()
pk.split_frames()[2].plot_peaks()
pk.split_frames()[3].plot_peaks()



plt.figure()
plt.title('N=4, seed1')
geo.plot_panels()
pk.split_frames()[5].plot_peaks()
pk.split_frames()[6].plot_peaks()
pk.split_frames()[7].plot_peaks()
pk.split_frames()[8].plot_peaks()




plt.figure()
plt.title('N=1024, seed0')
geo.plot_panels()
for frame in pk.split_frames():
    frame.plot_peaks()



plt.figure()
plt.title('N=1024, seed1')
geo.plot_panels()
for frame in pk.split_frames()[-1::-1]:
    frame.plot_peaks()



plt.show()





