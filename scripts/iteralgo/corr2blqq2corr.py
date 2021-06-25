
import scorpy
from scorpy import __DATADIR
import matplotlib.pyplot as plt



nq = 100
ntheta = 180
nphi = 360

npsi = 180
nl = 80


# branch 1
cif = scorpy.CifData(path=f'{scorpy.__DATADIR}/xtal/fcc-sf.cif', qmax=20)
corr1 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr1.fill_from_cif(cif, cords='scat_sph')

blqq2 = scorpy.BlqqVol(nq, nl,cif.qmax)
blqq2.fill_from_corr(corr1)

corr4 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr4.fill_from_blqq(blqq2)

sphv = scorpy.SphericalVol(nq, ntheta, nphi, cif.qmax)
sphv.fill_from_cif(cif)
sphv_scat_sph = sphv.ls_pts()


# branch 2
corr2 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr2.correlate_scat_sph(sphv_scat_sph)

blqq3 = scorpy.BlqqVol(nq, nl,cif.qmax)
blqq3.fill_from_corr(corr2)

corr5 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr5.fill_from_blqq(blqq3)

# branch 3
blqq1 = scorpy.BlqqVol(nq, nl,cif.qmax)
blqq1.fill_from_sphv(sphv)

corr3 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr3.fill_from_blqq(blqq1)

blqq4 = scorpy.BlqqVol(nq, nl,cif.qmax)
blqq4.fill_from_corr(corr3)



for corr in [corr1,corr2,corr3,corr4,corr5]:
    corr.plot_q1q2()

plt.show()
