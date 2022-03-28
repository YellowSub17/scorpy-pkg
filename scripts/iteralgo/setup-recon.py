#!/usr/bin/env python3

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')

# # # Parameters
nq= 256
npsi = 360*60
qmax = 9

nl = 150
rcond = 0.1

loose_supp = True

ntheta = nl*2
nphi = ntheta*2







tag = 'agno3'
cif_fname = 'agno3-sf.cif'




# # # Generate Target
cif_targ = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/{cif_fname}', qmax=qmax, rotk=[1,1,1], rottheta=np.radians(30))

sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif_targ)

qloc = np.unique(np.where(sphv_targ.vol !=0)[0])


# # # Generate Support 
cif_supp = scorpy.CifData(f'{scorpy.DATADIR}/xtal/{cif_fname}', qmax = qmax, rotk=[1,1,1], rottheta=np.radians(30))
sphv_supp = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_supp.fill_from_cif(cif_supp)





dxsupp = 2
for pti in sphv_supp.ls_pts(inds=True):
    xul = int(pti[0]-dxsupp), int(pti[0]+dxsupp+1)
    yul = int(pti[1]-dxsupp), int(pti[1]+dxsupp+1)
    zul = int(pti[2]-dxsupp), int(pti[2]+dxsupp+1)

    sphv_supp.vol[xul[0]:xul[1], yul[0]:yul[1], zul[0]:zul[1]] = 1






# iqlm_supp = scorpy.IqlmHandler(nq, nl, qmax)
# iqlm_supp.fill_from_sphv(sphv_supp)

# sphv_supp.vol *=0
# sphv_supp.fill_from_iqlm(iqlm_supp)

# sphv_supp.plot_slice(0, 92)
# sphv_supp.plot_slice(0, -1)
# sphv_supp.vol[sphv_supp.vol<1] = 0
# sphv_supp.vol[sphv_supp.vol>=1] = 1

sphv_targ.plot_slice(0, 70)
sphv_targ.plot_slice(0, 150)


# plt.figure()
# plt.plot(sphv_supp.vol.sum(axis=-1).sum(axis=-1))

# plt.figure()
# plt.plot(sphv_supp.vol.mean(axis=-1).mean(axis=-1))
# plt.plot(sphv_supp.vol.std(axis=-1).std(axis=-1))




















# plt.figure()
# plt.plot(sphv_supp.vol.sum(axis=-1).sum(axis=-1))

# sphv_supp.plot_slice(0, 246)
# plt.show()








# # # Generate Data (from corr)
# corr_data = scorpy.CorrelationVol(nq, npsi, qmax)
# corr_data.fill_from_cif(cif_targ, verbose=2)

# blqq_data = scorpy.BlqqVol(nq, nl, qmax)
# blqq_data.fill_from_corr(corr_data, rcond=0.1, verbose=1)

# corr_calc = scorpy.CorrelationVol(nq, npsi, qmax)
# corr_calc.fill_from_blqq(blqq_data, verbose=1)



# # # # Make directory to save vols
# os.mkdir(f'{scorpy.DATADIR}/algo/{tag}')

# sphv_targ.save(f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
# cif_targ.save(f'{scorpy.DATADIR}/algo/{tag}/{tag}_targ-sf.cif')
sphv_supp.save(f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')
# blqq_data.save(f'{scorpy.DATADIR}/algo/{tag}/blqq_{tag}_data.dbin')

# corr_data.save(f'{scorpy.DATADIR}/algo/{tag}/qcor_{tag}_data.dbin')
# corr_calc.save(f'{scorpy.DATADIR}/algo/{tag}/qcor_{tag}_calc.dbin')




# qloc = np.unique(sphv_targ.ls_pts(inds=True)[:,0])
# print(qloc)

# qq = -5


# sphv_targ.plot_slice(0, qq)
# sphv_supp.plot_slice(0, qq)

# blqq_data.plot_q1q2()
# corr_data.plot_q1q2()
# corr_calc.plot_q1q2()

# # x = sphv_targ.copy()
# # x.make_mask()
# # x.vol +=sphv_supp.vol
# # x.plot_slice(0,qq)




plt.show()






