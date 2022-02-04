import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')



nq= 400
ntheta = 180
nphi = 360
nl = 90
npsi = 360
qmax = 0.5





# # # Generate Target
cif_targ = scorpy.CifData(path=f'{scorpy.DATADIR}/cifs/p1-inten-r0-sf.cif', qmax = qmax)
sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif_targ)


# # # Generate Data
iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
iqlm_targ.fill_from_sphv(sphv_targ)
sphv_harmed = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_harmed.fill_from_iqlm(iqlm_targ)

blqq_lm = scorpy.BlqqVol(nq, nl, qmax)
blqq_lm.fill_from_iqlm(iqlm_targ)


# # # Generate Data
corr = scorpy.CorrelationVol(nq, npsi, qmax)
corr.fill_from_cif(cif_targ)

blqq_cr = scorpy.BlqqVol(nq, nl, qmax)
blqq_cr.fill_from_corr(corr, rcond=0.1)



fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
blqq_lm.plot_q1q2(fig=fig, axes=axes[0], title='blqq from harmonics', ylabel='q1=q2', xlabel='L')
blqq_cr.plot_q1q2(fig=fig, axes=axes[1], title='blqq from corr', ylabel='q1=q2', xlabel='L')


blqq_lm_crop = blqq_lm.crop(0,0,0, nq-1, nq-1, 20)
blqq_cr_crop = blqq_cr.crop(0,0,0, nq-1, nq-1, 20)

fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
blqq_lm_crop.plot_xy(fig=fig, axes=axes[0], title='blqq from harmonics (crop)', ylabel='q1=q2', xlabel='L')
blqq_cr_crop.plot_xy(fig=fig, axes=axes[1], title='blqq from corr (crop)', ylabel='q1=q2', xlabel='L')




sphv_qloc = np.unique(np.where(sphv_targ.vol !=0)[0])
# corr_qloc = np.unique(np.where(corr.vol !=0)[0])

# qq = sphv_qloc[0]

sphv_targ.plot_slice(0, sphv_qloc[0], title=f'sphv q={sphv_targ.xpts[sphv_qloc[0]]}, nq={sphv_qloc[0]}', xlabel='phi', ylabel='theta')
sphv_targ.plot_slice(0,sphv_qloc[1], title=f'sphv q={sphv_targ.xpts[sphv_qloc[1]]}, nq={sphv_qloc[1]}', xlabel='phi', ylabel='theta')

sphv_targ.plot_slice(0, 192, title=f'sphv q={sphv_targ.xpts[192]}, nq={192}', xlabel='phi', ylabel='theta')
sphv_targ.plot_slice(0, 195, title=f'sphv q={sphv_targ.xpts[195]}, nq={195}', xlabel='phi', ylabel='theta')
sphv_targ.plot_slice(0, 196, title=f'sphv q={sphv_targ.xpts[196]}, nq={196}', xlabel='phi', ylabel='theta')



# plt.figure()
# plt.plot(sphv_qloc, sphv_targ.xpts[sphv_qloc])












# fig, axes = plt.subplots(1,3, sharex=False, sharey=True)
# blqq_cr.plot_q1q2(fig=fig, axes=axes[0])
# blqq_lm.plot_q1q2(fig=fig, axes=axes[1])
# iqlm_targ.plot_l(4,fig=fig, axes=axes[2])


plt.show()





