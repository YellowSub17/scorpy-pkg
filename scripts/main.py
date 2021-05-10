
import numpy as np
import matplotlib.pyplot as plt
import scorpy
plt.close('all')


nq = 100
npsi = 360
nl = 95

qmax = 0.36992983463258367 / 3

corrs = []
corrs_titles = []

blqqs = []
blqqs_titles = []


cif = scorpy.CifData('../data/xtal/1al1-sf.cif', qmax)
cif.bin_sph(nq, npsi, 2 * npsi)

sphv = scorpy.SphericalVol(nq, npsi, qmax)
sphv.fill_from_cif(cif)

qs = np.unique(np.where(sphv.vol > 0)[0])

l = 0


corr1 = scorpy.CorrelationVol(nq, npsi, qmax)
corr1.fill_from_cif(cif)
# corr1.theta_multi()
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
    plt.title(title + f' q1q2')

for corr, title in zip(corrs, corrs_titles):
    corr.plot_slice(axis=2, index=40)
    plt.title(title + f' theta slice: {40}')


# q1 = qs[2]
# q2 = qs[5]
# plt.figure()
# plt.title(f'corrs: {q1}, {q2}')
# for corr, title in zip(corrs, corrs_titles):
    # print(np.max(corr.vol[q1,q2,:]))
    # plt.plot(corr.vol[q1,q2,:]/np.max(corr.vol[q1,q2,:]), label=title)
# plt.legend()


# q1 = qs[1]
# q2 = qs[1]
# plt.figure()
# plt.title(f'corrs: {q1}, {q2}')
# for corr, title in zip(corrs, corrs_titles):
    # print(np.max(corr.vol[q1,q2,:]))
    # plt.plot(corr.vol[q1,q2,:]/np.max(corr.vol[q1,q2,:]), label=title)
# plt.legend()


# for corr in corrs:
    # corr._nz -=20
    # corr._vol = corr.vol[...,10:-10]
    # corr.plot_slice(axis=0, index=q)


# # corr1.plot_line(axis=0, in1=q, in2=q)
# # plt.title('Corr - Original')

# corr2.plot_line(axis=0, in1=q, in2=q, new_fig=False)
# plt.title('Corr - corr->blqq->corr')

# corr3.plot_line(axis=0, in1=q, in2=q)
# plt.title('Corr - sphv->blqq->corr')

# q = qs[3]

# # corr1.plot_line(axis=0, in1=q, in2=q)
# # plt.title('Corr - Original')

# corr2.plot_line(axis=0, in1=q, in2=q)
# plt.title('Corr - corr->blqq->corr')

# corr3.plot_line(axis=0, in1=q, in2=q)
# plt.title('Corr - sphv->blqq->corr')


# blqq1.plot_slice(2,l)
# plt.title('Blqq - corr->blqq')

# blqq2.plot_slice(2,l)
# plt.title('Blqq - sphv->blqq')


# q= qs[0]
# plt.figure()
# plt.plot(blqq1.vol[:,q,l])
# plt.title(f'Blqq - corr->blqq - {q},{l}')

# plt.figure()
# plt.plot(blqq2.vol[:,q,l])
# plt.title(f'Blqq - sphv->blqq - {q},{l}')

# rel = scorpy.utils.mydiv(blqq1.vol, blqq2.vol)
# plt.figure()
# plt.plot(rel[:,q,l])

# plt.title(f'Blqq - Rel - {q},{l}')


# q= qs[2]
# plt.figure()
# plt.plot(blqq1.vol[:,q,l])
# plt.title(f'Blqq - corr->blqq - {q},{l}')

# plt.figure()
# plt.plot(blqq2.vol[:,q,l])
# plt.title(f'Blqq - sphv->blqq - {q},{l}')


# rel = scorpy.utils.mydiv(blqq1.vol, blqq2.vol)
# plt.figure()
# plt.plot(rel[:,q,l])

# plt.title(f'Blqq - Rel - {q},{l}')


# lam1, us1 =  blqq1.get_eig(herm=True)

# plt.figure()
# plt.title('eigen')
# plt.plot(lam1[:,l]/np.max(lam1[:,l]))


# lam2, us2 =  blqq2.get_eig(herm=True)
# plt.plot(lam2[:,l]/np.max(lam2[:,l]))


plt.show()
