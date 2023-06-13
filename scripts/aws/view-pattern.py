import scorpy
import numpy as np
import matplotlib.pyplot as plt


for qmax, geomz in zip([1.5,1.0, 0.7, 0.5], ['040', '060','090', '120']):

    npz_fname =  f'/home/ec2-user/corr/data/frames/193l-100nm-19MPz{geomz}-test-1.npz'
    pk = scorpy.PeakData(npz_fname, f'/home/ec2-user/corr/data/geom/19MPz{geomz}.geom')

    pk.plot_peaks()
    plt.title(f'{geomz} orig')
    pk.plot_peakr(0.0025)

    inte = pk.integrate_peaks(0.0025)
    pk.calc_scat(inte[:,0:3], inte[:,-1])

    pk.plot_peaks()
    plt.title(f'{geomz} inte')
    pk.plot_qring(0.4)
    pk.plot_qring(qmax)




plt.show()












