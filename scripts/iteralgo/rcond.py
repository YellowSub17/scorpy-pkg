
import scorpy
from scorpy import __DATADIR
import matplotlib.pyplot as plt


nq = 100
ntheta = 180
nphi = 360
npsi = 180
nl = 90

rcond = 1e-15
rcond_str = 15

# branch 1
cif = scorpy.CifData(path=f'{scorpy.__DATADIR}/xtal/fcc-sf.cif', qmax=20)
corr1 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr1.fill_from_cif(cif, method='scat_sph')
print('corr1 done')

blqq2 = scorpy.BlqqVol(nq, nl,cif.qmax)
blqq2.fill_from_corr(corr1, inc_odds=True, rcond=rcond)
print('blqq2 done')

corr4 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr4.fill_from_blqq(blqq2, inc_odds=True)
print('corr4 done')

sphv = scorpy.SphericalVol(nq, ntheta, nphi, cif.qmax)
sphv.fill_from_cif(cif)
sphv_scat_sph = sphv.ls_pts()
print('sphv done')


# branch 2
corr2 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr2.correlate_scat_sph(sphv_scat_sph)
print('corr2 done')

blqq3 = scorpy.BlqqVol(nq, nl,cif.qmax)
blqq3.fill_from_corr(corr2, inc_odds=True, rcond=rcond)
print('blqq3 done')

corr5 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr5.fill_from_blqq(blqq3, inc_odds=True)
print('corr5 done')

# branch 3

iqlm = scorpy.IqlmHandler(nq, nl, cif.qmax)
iqlm.fill_from_sphv(sphv)

blqq1 = scorpy.BlqqVol(nq, nl,cif.qmax)
blqq1.fill_from_iqlm(iqlm, inc_odds=True)
print('blqq1 done')

corr3 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr3.fill_from_blqq(blqq1, inc_odds=True)
print('corr3 done')

blqq4 = scorpy.BlqqVol(nq, nl,cif.qmax)
blqq4.fill_from_corr(corr3, inc_odds=True, rcond=rcond)
print('blqq4 done')

corr6 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr6.fill_from_blqq(blqq4, inc_odds=True)
print('corr6 done')

blqq5 = scorpy.BlqqVol(nq, nl,cif.qmax)
blqq5.fill_from_corr(corr6, inc_odds=True, rcond=rcond)
print('blqq5 done')



for i, corr in enumerate([corr1, corr2, corr3, corr4, corr5, corr6]):
    corr.plot_q1q2()
    plt.title(f'corr{i+1}')
    plt.axis([-1,1,10, 18])
    plt.savefig(f'/home/pat/Documents/cloudstor/phd/latex/scorpy-script-reports/figs/iteralgo-corr{i+1}rcond{rcond_str}.png')



for i, blqq in enumerate([blqq1, blqq2, blqq3, blqq4, blqq5]):
    blqq.plot_q1q2()
    plt.title(f'blqq{i+1} q1=q2')
    plt.axis([0,80,10, 18])
    plt.savefig(f'/home/pat/Documents/cloudstor/phd/latex/scorpy-script-reports/figs/iteralgo-blqq{i+1}rcond{rcond_str}.png')

plt.show()
