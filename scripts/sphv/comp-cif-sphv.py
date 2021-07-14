
import scorpy
import matplotlib.pyplot as plt
import numpy as np
import time




nq = 100
ntheta = 180
nphi = ntheta*2

npsi = 180


cif = scorpy.CifData(path=f'{scorpy.__DATADIR}/xtal/fcc-sf.cif', qmax=20)
corr1 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr1.fill_from_cif(cif, cords='scat_sph')



corr1.plot_q1q2(title='cif')
corr1.plot_sumax(title='cif')


sphv = scorpy.SphericalVol(nq, ntheta, nphi, cif.qmax)
sphv.fill_from_cif(cif)
sphv_scat_sph = sphv.ls_pts()

corr2 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr2.correlate_scat_sph(sphv_scat_sph)

corr2.plot_q1q2(title='sphv')
corr2.plot_sumax(title='sphv')


plt.show()






