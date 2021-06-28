
import scorpy
from scorpy import __DATADIR
import matplotlib.pyplot as plt



nq = 100
ntheta = 180
nphi = 360
npsi = 180
nl = 81


# branch 1
cif = scorpy.CifData(path=f'{scorpy.__DATADIR}/xtal/fcc-sf.cif', qmax=20)
corr1 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr1.fill_from_cif(cif, cords='scat_sph')
print('corr1 done')

blqq2 = scorpy.BlqqVol(nq, nl,cif.qmax)
blqq2.fill_from_corr(corr1)
print('blqq2 done')

corr4 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr4.fill_from_blqq(blqq2)
print('corr4 done')

sphv = scorpy.SphericalVol(nq, ntheta, nphi, cif.qmax, normalization='4pi')
sphv.fill_from_cif(cif)
sphv_scat_sph = sphv.ls_pts()
print('sphv done')


# branch 2
corr2 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr2.correlate_scat_sph(sphv_scat_sph)
print('corr2 done')

blqq3 = scorpy.BlqqVol(nq, nl,cif.qmax)
blqq3.fill_from_corr(corr2)
print('blqq3 done')

corr5 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr5.fill_from_blqq(blqq3)
print('corr5 done')

# branch 3
blqq1 = scorpy.BlqqVol(nq, nl,cif.qmax)
blqq1.fill_from_sphv(sphv)
print('blqq1 done')

corr3 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr3.fill_from_blqq(blqq1)
print('corr3 done')

blqq4 = scorpy.BlqqVol(nq, nl,cif.qmax)
blqq4.fill_from_corr(corr3)
print('blqq4 done')

corr6 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr6.fill_from_blqq(blqq4)
print('corr6 done')

blqq5 = scorpy.BlqqVol(nq, nl,cif.qmax)
blqq5.fill_from_corr(corr6)
print('blqq5 done')



# for i, corr in enumerate([corr1, corr2, corr3, corr4, corr5, corr6]):
    # corr.plot_q1q2()
    # plt.title(f'corr{i+1}')


for i, blqq in enumerate([blqq1, blqq2, blqq3, blqq4, blqq5]):
    blqq.plot_q1q2()
    plt.title(f'blqq{i+1}')



plt.show()
