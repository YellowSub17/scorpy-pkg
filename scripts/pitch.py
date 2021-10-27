
import matplotlib.pyplot as plt
plt.close('all')
import numpy as np
import scorpy



pk_qmax = 2.5
cif_qmax = 60
corr_nq = 100
sphv_nq = 30
ntheta = 90
nphi = 180
nl = 45




# pk = scorpy.PeakData(f'{scorpy.DATADIR}/h5/1vds.h5', qmax=pk_qmax)
# plt.figure()
# plt.axis('equal')
# pk.geo.plot_panels()
# pk.plot_peaks(cmap='plasma')
# plt.title('Simulated 2D Peaks')
# plt.colorbar()
# plt.savefig('pitch-2dpeaks.png')
# corr1 = scorpy.CorrelationVol(corr_nq, ntheta, pk.qmax, cos_sample=False)
# corr1.fill_from_peakdata(pk)
# corr1.plot_q1q2(log=True, xlabel='$\\psi$[rad]', ylabel='$q$ [$\u212b^{-1}$]', title='QCOR $q_1 = q_2$ (2D data)')
# plt.savefig('pitch-2dcorr.png')



cif = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-sf.cif', qmax=cif_qmax)
# corr2 = scorpy.CorrelationVol(corr_nq, ntheta, cif.qmax, cos_sample=False)
# corr2.fill_from_cif(cif)


corr2 = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/fcc-qcor')
corr2.plot_q1q2(log=True, xlabel='$\\psi$[rad]', ylabel='$q$ [$\u212b^{-1}$]', title='QCOR $q_1 = q_2$ (3D data)')
plt.savefig('pitch-3dcorr.png')


blqq1 = scorpy.BlqqVol(corr2.nq, nl, corr2.qmax)
blqq1.fill_from_corr(corr2)





sphv = scorpy.SphericalVol(sphv_nq, ntheta, nphi, cif.qmax)
sphv.fill_from_cif(cif)
qq = np.unique(np.where(sphv.vol>0)[0])[-1]
sphv.plot_slice(0, qq, xlabel='$\\phi$[rad]', ylabel='$\\theta$ [rad]', title='Spherical Corrdinate Intensity')
plt.savefig('pitch-sphv.png')


iqlm = scorpy.IqlmHandler(sphv.nq, nl , sphv.qmax)
iqlm.fill_from_sphv(sphv)
iqlm.plot_q(qq, title='Spherical Harmonics')
plt.savefig('pitch-harmonics.png')

blqq2 = scorpy.BlqqVol(iqlm.nq, nl, iqlm.qmax)
blqq2.fill_from_iqlm(iqlm)

blqq2.plot_slice(2, 0,xlabel='$q_1$ [$\u212b^{-1}$]', ylabel='$q_2$ [$\u212b^{-1}$]', title='BLQQ (L=0)')
plt.savefig('pitch-blqq.png')



mask = sphv.copy()
mask.make_mask()



a = scorpy.AlgoHandler(blqq2, mask, lossy_iqlm=False, lossy_sphv=False)

a.sphv_iter.plot_slice(0, qq, xlabel='$\\phi$[rad]', ylabel='$\\theta$ [rad]', title='Initial Random Start')
plt.savefig('pitch-random.png')
a.ER()
a.sphv_add.plot_slice(0, qq, xlabel='$\\phi$[rad]', ylabel='$\\theta$ [rad]', title='First Iteration')
plt.savefig('pitch-iter1.png')
a.ER()
a.sphv_add.plot_slice(0, qq, xlabel='$\\phi$[rad]', ylabel='$\\theta$ [rad]', title='Second Iteration')
plt.savefig('pitch-iter2.png')

plt.show()




