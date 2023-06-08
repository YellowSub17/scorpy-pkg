import scorpy
import numpy as np
import matplotlib.pyplot as plt



npz_fname =  f'/home/ec2-user/corr/data/frames/1vds-500nm-19MPz40-test-1.npz'
pk = scorpy.PeakData(npz_fname, '/home/ec2-user/corr/data/geom/19MPz40.geom')

pk.plot_peaks()
pk.plot_peakr(0.005)

inte = pk.integrate_peaks(0.005)
pk.calc_scat(inte[:,0:3], inte[:,-1])

pk.plot_peaks()
plt.show()












