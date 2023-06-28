

import scorpy 
import numpy as np
import matplotlib.pyplot as plt



qtia =  [1, 0, 2]
qtib =  [1.5, np.radians(45), 3]
qtic =  [1.5, np.radians(360-45), 4]

xyza = [ 0.025, 0.025, 0.4 ]
xyzb = [ 0.1, 0, 0.4 ]
xyzc = [ 0, .1, 0.4 ]
xyzd = [ -0.025, 0.025, 0.4 ]



pk =  scorpy.PeakData('','/home/ec2-user/corr/data/geom/19MPz040.geom' )



xyzi = np.array([xyza, xyzb, xyzc, xyzd])
pk.calc_scat(xyzi, [2,3,5,7])

xyzi = np.array([xyza, xyzb])
pk.calc_scat(xyzi, [2,3])

xyzi = np.array([xyza, xyzb, xyzc])
pk.calc_scat(xyzi, [2,3,5])




corr = scorpy.CorrelationVol(50, 90, 1.5, 0, cos_sample=False)
corr.fill_from_peakdata(pk)
corr._plot_2D(corr.get_xy(), title='q1q2')
corr._plot_2D(corr.vol[13,:,:], title='qa')
corr._plot_2D(corr.vol[38,:,:], title='qbc')

# corr._plot_2D(corr.vol.sum(axis=0))


pk.plot_peaks()

plt.show()
