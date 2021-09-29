

import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')






# Parameters
nq= 100
ntheta = 180
nphi = 360
nl = 90
qmax = 108
qq = 5
nn = -2
rcond = 1e-1

# SET UP DATA
cif = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-sf.cif', qmax = qmax)

# SET UP MASK
sphv_mask = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_mask.fill_from_cif(cif)
sphv_mask.make_mask()

# SET UP TARGET HARMONICS
sphv_targ = sphv_mask.copy()
iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
iqlm_targ.fill_from_sphv(sphv_targ)

# SET UP BLQQ
blqq_data = scorpy.BlqqVol(nq, nl, qmax)
blqq_data.fill_from_iqlm(iqlm_targ)


lams, us = blqq_data.get_eig()


plt.figure()
plt.title('Eigenvalues before')
plt.imshow(lams)
plt.ylabel('n')
plt.xlabel('l')

plt.figure()
plt.plot(lams[:,nn], label='before')


eigs_thresh = np.max(lams, axis=0)*rcond


for l_ind, eig_thresh in enumerate(eigs_thresh):
    # print(l_ind, eig_thresh)
    loc = np.where(lams[:,l_ind] < eig_thresh)
    lams[loc, l_ind] = 0

plt.plot(lams[:,nn], label='after')


plt.figure()
plt.title('Eigenvalues after')
plt.imshow(lams)
plt.ylabel('n')
plt.xlabel('l')




# knlm_full = iqlm_targ.copy()
# knlm_full.calc_knlm(us)

# iqlm_full = knlm_full.copy()
# iqlm_full.calc_iqlmp(us)





# iqlm_targ.plot_q(qq)
# iqlm_full.plot_q(qq)


plt.show()










