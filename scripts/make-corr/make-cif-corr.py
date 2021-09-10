

import numpy as np
import scorpy
import matplotlib.pyplot as plt



nq = 100
ntheta = 180
nphi = 360

qmax = 40
cos_sample = True



cif = scorpy.CifData(f'{scorpy.env.__DATADIR}/cifs/fcc-sf.cif', qmax=qmax)

sphv = scorpy.SphericalVol(nq, ntheta, nphi, cif.qmax)
print('a')
sphv.fill_from_cif(cif)

iqlm = scorpy.IqlmHandler(nq, sphv.nl, cif.qmax)
print('b')
iqlm.fill_from_sphv(sphv)


blqq1 = scorpy.BlqqVol(nq, sphv.nl, cif.qmax)
print('c')
blqq1.fill_from_iqlm(iqlm)

# correlation function of the harmonic order function from spherical volume
corr1 = scorpy.CorrelationVol(nq, ntheta, cif.qmax, cos_sample=cos_sample)
print('d')
corr1.fill_from_blqq(blqq1)


# correlation directly from the cif
corr2 = scorpy.CorrelationVol(nq, ntheta, cif.qmax, cos_sample=cos_sample)
print('e')
corr2.fill_from_cif(cif)



blqq2 =scorpy.BlqqVol(nq, sphv.nl, qmax)
print('f')
blqq2.fill_from_corr(corr2)

# correlation from harmonic order directly from cif
corr3 = scorpy.CorrelationVol(nq, ntheta, cif.qmax, cos_sample=cos_sample)
print('g')
corr3.fill_from_blqq(blqq2)





corr1.plot_q1q2()
corr2.plot_q1q2()
corr3.plot_q1q2()


corr1.save(f'{scorpy.env.__DATADIR}/dbins/fcc1_corr')
corr2.save(f'{scorpy.env.__DATADIR}/dbins/fcc2_corr')
corr3.save(f'{scorpy.env.__DATADIR}/dbins/fcc3_corr')




plt.show()




