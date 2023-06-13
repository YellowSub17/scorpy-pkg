import scorpy
import numpy as np
import matplotlib.pyplot as plt



npz_fname =  f'/home/ec2-user/corr/data/frames/193l-500nm-19MPz040-test-0.npz'
pk = scorpy.PeakData(npz_fname, '/home/ec2-user/corr/data/geom/19MPz040.geom')

plt.figure()
pk.plot_panels()
pk.plot_qring(0.4, ec='red')
pk.plot_qring(1.5)
plt.title('40')

pk = scorpy.PeakData(npz_fname, '/home/ec2-user/corr/data/geom/19MPz060.geom')
plt.figure()
pk.plot_panels()
pk.plot_qring(0.4, ec='red')
pk.plot_qring(1.0)
plt.title('60')

pk = scorpy.PeakData(npz_fname, '/home/ec2-user/corr/data/geom/19MPz090.geom')
plt.figure()
pk.plot_panels()
pk.plot_qring(0.4, ec='red')
pk.plot_qring(0.7)
plt.title('90')


pk = scorpy.PeakData(npz_fname, '/home/ec2-user/corr/data/geom/19MPz120.geom')
plt.figure()
pk.plot_panels()
pk.plot_qring(0.4, ec='red')
pk.plot_qring(0.5)
plt.title('120')





plt.show()












