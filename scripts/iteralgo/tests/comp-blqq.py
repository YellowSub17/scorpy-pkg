import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')



nq= 50

qmax = 0.5

ntheta = 180
nphi = 360
nl = 90
npsi = 360*16



# ntheta = 90
# nphi = 180
# nl = 45
# npsi = 360*32




# ntheta = 720
# nphi = 1440
# nl = 360
# npsi = 360*32

#

# ntheta = 200
# nphi = 400
# nl = 100




# # Generate Target
cif_targ = scorpy.CifData(path=f'{scorpy.DATADIR}/cifs/p1-inten-r0-sf.cif', qmax = qmax, crop_poles=True)

cif_targ.unit_inten()


print(cif_targ.scat_sph[10:20,:])
cif_targ.sin_theta_correction()
print(cif_targ.scat_sph[10:20,:])


sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif_targ)

qloc = np.unique(np.where(sphv_targ.vol !=0)[0])


# # # Generate Data
iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax, inc_odds=False)
iqlm_targ.fill_from_sphv(sphv_targ)

blqq_lm = scorpy.BlqqVol(nq, nl, qmax, inc_odds=False)
blqq_lm.fill_from_iqlm(iqlm_targ)

blqq_lm.vol *= ntheta*nphi


# # # Generate Data
corr = scorpy.CorrelationVol(nq, npsi, qmax)
corr.fill_from_cif(cif_targ)

blqq_cr = scorpy.BlqqVol(nq, nl, qmax, inc_odds=False)
blqq_cr.fill_from_corr(corr, rcond=0.1)

# blqq_cr = blqq_lm.copy()
# std = blqq_cr.vol[blqq_cr.vol!=0].std()/5
# err = (std + std) *np.random.random(blqq_cr.vol.shape) - std
# blqq_cr.vol += err





blqq_lm.vol[:, :, 41:] *=0
blqq_cr.vol[:, :, 41:] *=0




blqq_div = scorpy.BlqqVol(nq, nl, qmax)
loc0 = np.where(blqq_lm.vol !=0)

# blqq_div.vol[loc0] = blqq_cr.vol[loc0] / blqq_lm.vol[loc0]

blqq_div.vol = blqq_cr.vol - blqq_lm.vol


fig, axes = plt.subplots(1,3, sharex=True, sharey=True)
blqq_lm.plot_q1q2(fig=fig, axes=axes[0], title='blqq from harmonics', ylabel='q1=q2', xlabel='L')
blqq_cr.plot_q1q2(fig=fig, axes=axes[1], title='blqq from corr', ylabel='q1=q2', xlabel='L')
blqq_div.plot_q1q2(fig=fig, axes=axes[2], title='blqq div', ylabel='q1=q2', xlabel='L')





plt.figure()
# plt.plot(blqq_div.get_xy()[:, 40])
y = blqq_div.get_xy()[qloc[10],:]
plt.plot(y/y[0])

y = blqq_div.get_xy()[qloc[0],:]
plt.plot(y/y[0])

# y = blqq_div.get_xy()[qloc[-8],:]
# plt.plot(y/y[0])

# y = blqq_div.get_xy()[qloc[-21],:]
# plt.plot(y/y[0])



sphv_targ.plot_slice(0, qloc[0])
sphv_targ.plot_slice(0, qloc[10])


plt.figure()

x = sphv_targ.qpts

y = sphv_targ.vol.sum(axis=-1).sum(axis=-1)
plt.plot(x,y)




# y1 = blqq_lm.get_xy().sum(axis=-1)
# y2 = blqq_cr.get_xy().sum(axis=-1)

# y1 = blqq_lm.get_xy()[:, 4]
# y2 = blqq_cr.get_xy()[:, 4]

# y1 = blqq_lm.vol[qloc[0],:, 4]
# y2 = blqq_cr.vol[qloc[0],:, 4]


# fig, axes = plt.subplots(1,2, sharex=True)
# axes[0].plot(y1)
# axes[0].plot(y2)

# y3 = np.ones( y1.shape)
# y3[y2!=0] = (y1[y2!=0]/y2[y2!=0])

# axes[1].plot(y3)



# lams_lm, us_lm = blqq_lm.get_eig(herm=True)
# lams_cr, us_cr = blqq_cr.get_eig(herm=True)



# plt.figure()
# plt.imshow(lams_lm)
# plt.title('eigenvalues from harmonics')
# plt.colorbar()


# plt.figure()
# plt.imshow(lams_cr)
# plt.title('eigenvalues from correlation')
# plt.colorbar()


# plt.figure()
# plt.plot(lams_lm[:, 10])
# plt.plot(lams_cr[:, 10])







# #  Generate Target
# cif_targ = scorpy.CifData(path=f'{scorpy.DATADIR}/cifs/p1-inten-r0-sf.cif', qmax = qmax, crop_poles=False)
# # cif_targ.multi_inten(10000)

# sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
# sphv_targ.fill_from_cif(cif_targ)

# # # Generate Data
# iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax, inc_odds=False)
# iqlm_targ.fill_from_sphv(sphv_targ)

# blqq_lm1 = scorpy.BlqqVol(nq, nl, qmax, inc_odds=False)
# blqq_lm1.fill_from_iqlm(iqlm_targ)
# blqq_lm1.vol *= ntheta*nphi


# # Generate Target
# cif_targ = scorpy.CifData(path=f'{scorpy.DATADIR}/cifs/p1-inten-r0-sf.cif', qmax = qmax, crop_poles=False)
# cif_targ.unit_inten()
# # cif_targ.multi_inten(10000)

# sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
# sphv_targ.fill_from_cif(cif_targ)

# # # Generate Data
# iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax, inc_odds=False)
# iqlm_targ.fill_from_sphv(sphv_targ)

# blqq_lm2 = scorpy.BlqqVol(nq, nl, qmax, inc_odds=False)
# blqq_lm2.fill_from_iqlm(iqlm_targ)
# blqq_lm2.vol *= ntheta*nphi


# blqq_lm1.vol[:, :, 41:] *=0
# blqq_lm2.vol[:, :, 41:] *=0


# fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
# blqq_lm1.plot_q1q2(title='unit intensity', fig=fig, axes=axes[0])
# blqq_lm2.plot_q1q2(title='random intensity', fig=fig, axes=axes[1])


















plt.show()





