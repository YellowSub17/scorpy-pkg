
import numpy as np
import matplotlib.pyplot as plt
import scorpy
plt.close('all')


nq = 100
npsi = 300
nl = 120

qmax = 0.36992983463258367 / 3

corrs = []
corrs_titles = []

blqqs = []
blqqs_titles = []


cif = scorpy.CifData('../data/xtal/1al1-sf.cif', qmax)
# cif.bin_sph(nq, npsi, 2 * npsi)

sphv = scorpy.SphericalVol(nq, npsi, 2 * npsi, qmax)
sphv.fill_from_cif(cif)

qs = np.unique(np.where(sphv.vol > 0)[0])

l = 0


corr1 = scorpy.CorrelationVol(nq, npsi, qmax)
corr1.fill_from_cif(cif)
# corr1.force_sym()
corrs.append(corr1)
corrs_titles.append('Corr1: cif->corr')

blqq1 = scorpy.BlqqVol(nq, nl, qmax)
blqq1.fill_from_corr(corr1)
blqqs.append(blqq1)
blqqs_titles.append('Blqq1: cif->corr->blqq')


corr2 = scorpy.CorrelationVol(nq, npsi, qmax)
corr2.fill_from_blqq(blqq1)
corrs.append(corr2)
corrs_titles.append('Corr2: cif->corr->blqq->corr')


blqq2 = scorpy.BlqqVol(nq, nl, qmax)
blqq2.fill_from_sphv(sphv)
blqqs.append(blqq2)
blqqs_titles.append('Blqq2: sphv->blqq')

corr3 = scorpy.CorrelationVol(nq, npsi, qmax)
corr3.fill_from_blqq(blqq2)
corrs.append(corr3)
corrs_titles.append('Corr3: sphv->blqq->corr')


for corr, title in zip(corrs, corrs_titles):
    corr.plot_q1q2()
    plt.title(title + ' q1=q2')

for corr, title in zip(corrs, corrs_titles):
    corr.plot_slice(axis=2, index=40)
    plt.title(title + f' theta slice: {40}')


plt.show()
