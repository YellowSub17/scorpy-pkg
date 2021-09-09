

import numpy as np
import scorpy
import matplotlib.pyplot as plt



nq = 100
ntheta = 180
nphi = 360

qmax = 100



cif = scorpy.CifData(f'{scorpy.env.__DATADIR}/cifs/fcc-sf.cif', qmax=qmax)


sphv = scorpy.SphericalVol(nq, ntheta, nphi, cif.qmax)
print('a')
sphv.fill_from_cif(cif)

iqlm = scorpy.IqlmHandler(nq, sphv.nl, cif.qmax)
print('b')
iqlm.fill_from_sphv(sphv)


blqq = scorpy.BlqqVol(nq, sphv.nl, cif.qmax)
print('c')
blqq.fill_from_iqlm(iqlm)


corr1 = scorpy.CorrelationVol(nq, ntheta, cif.qmax)
print('d')
corr1.fill_from_blqq(blqq)


corr2 = scorpy.CorrelationVol(nq, ntheta, cif.qmax)
print('e')
corr2.fill_from_cif(cif)



blqq1 =scorpy.BlqqVol(nq, sphv.nl, qmax)
print('f')
blqq1.fill_from_corr(corr2)

corr3 = scorpy.CorrelationVol(nq, ntheta, cif.qmax)

print('g')
corr3.fill_from_blqq(blqq1)





corr1.plot_q1q2()
corr2.plot_q1q2()
corr3.plot_q1q2()


corr1.save(f'{scorpy.env.__DATADIR}/dbins/fcc1_corr')
corr2.save(f'{scorpy.env.__DATADIR}/dbins/fcc2_corr')
corr3.save(f'{scorpy.env.__DATADIR}/dbins/fcc3_corr')




plt.show()




