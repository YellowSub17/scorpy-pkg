import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
plt.close('all')


np.random.seed(0)







# Parameters
nq= 200
ntheta = 180
nphi = 360
nl = 90

# ntheta = 20
# nphi = 40
# nl = 10
qmax = 108
qmax = 50

qq = 50

# SET UP MASK DATA
cif_mask = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-sf.cif', qmax = qmax)
sphv_mask = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_mask.fill_from_cif(cif_mask)
sphv_mask.make_mask()


# SET UP TARGET DATA
cif_targ = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-sf.cif', qmax = qmax)
sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif_targ)


iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
iqlm_targ.fill_from_sphv(sphv_targ)

# SET UP BLQQ
blqq_data = scorpy.BlqqVol(nq, nl, qmax)
blqq_data.fill_from_iqlm(iqlm_targ)

corr_data1 = scorpy.CorrelationVol(nq, ntheta, qmax)
corr_data1.fill_from_blqq(blqq_data)

corr_cif = scorpy.CorrelationVol(nq, ntheta, qmax)
corr_cif.fill_from_cif(cif_targ)

blqqx = scorpy.BlqqVol(nq, nl, qmax)
blqqx.fill_from_corr(corr_cif)

corr_data2 = scorpy.CorrelationVol(nq, ntheta, qmax)
corr_data2.fill_from_blqq(blqqx)



















# # SET UP ALGORITHM
# a = scorpy.AlgoHandler(blqq_data, sphv_mask, iter_obj='sphv',
                       # lossy_sphv=True, lossy_iqlm=True, rcond=1e-3)













