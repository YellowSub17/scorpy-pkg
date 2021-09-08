
import numpy as np
np.random.seed(0)
import pyshtools as pysh
import matplotlib.pyplot as plt
plt.close('all')

import scorpy



nl = 50

harms = scorpy.utils.harmonic_list(nl)

nphi = nl*2*2
ntheta = nl*2
qmax= 1
nq = 150



iqlm = scorpy.IqlmHandler(nq, nl, qmax)
# for q_ind in range(nq):
    # iqlm.set_val(q_ind, harms[q_ind][0], harms[q_ind][1])
    # iqlm.set_val(q_ind, harms[q_ind][0]+1, harms[q_ind][1])



iqlm.vals = np.random.random(iqlm.vals.shape)






sphv1 = scorpy.SphericalVol(nq,ntheta, nphi, qmax)
sphv1.fill_from_iqlm(iqlm)



# get the harmonic order matrix
blqq = scorpy.BlqqVol(nq, nl, qmax)
blqq.fill_from_iqlm(iqlm, inc_odds=True)

# get eigenvalues and vectors
lams, us = blqq.get_eig()

# knlm -> iqlm prime calculation
knlm = iqlm.copy()
knlm.calc_knlm(us)
iqlmp = knlm.copy()
iqlmp.calc_iqlm_prime(us)



# replot harmonics on new spherical volume
sphv2 = scorpy.SphericalVol(nq,ntheta, nphi, qmax)
sphv2.fill_from_iqlm(iqlmp)




loc = np.where(iqlmp.vals !=0)
print('q shells with recovered harmonic intensity:')
print(f'{loc[0]}')


fig, axes = plt.subplots(1,2)
plt.suptitle(f'q shell {loc[0][0]}')
sphv1.plot_slice(0, loc[0][0], fig=fig, axes=axes[0])
sphv2.plot_slice(0, loc[0][0], fig=fig, axes=axes[1])


fig, axes = plt.subplots(1,2)
plt.suptitle(f'q shell {20}')
sphv1.plot_slice(0, 20, fig=fig, axes=axes[0])
sphv2.plot_slice(0, 20, fig=fig, axes=axes[1])


print(f'Harmonic in qshell {loc[0][0]}')
print(harms[loc[0][0]])

print(f'Harmonic in qshell {20}')
print(harms[20])


# for i in range(loc[0].size):
    # print('harmonic', harms[loc[0][i]])
    # print('iqlm val', iqlm.vals[loc[0][i], loc[1][i], loc[2][i], loc[3][i]])
    # print('iqlmp val', np.round(iqlmp.vals[loc[0][i], loc[1][i], loc[2][i], loc[3][i]]))
    # print()







plt.show()
