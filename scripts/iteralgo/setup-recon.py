#!/usr/bin/env python3

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')

# # # Parameters
nq= 256
npsi = 360*32
qmax = 9

nl = 180
lcrop = 45
rcond = 0.1


recon_tag = 'barite'
cif_fname = 'barite'



ntheta = nl*2
nphi = ntheta*2











# # # Generate Target
cif_targ = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/{cif_fname}/{cif_fname}-sf.cif', qmax=qmax, rotk=[1,1,1], rottheta=np.radians(30))
sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif_targ)





# # # # Generate Support 
cif_supp = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/{cif_fname}/{cif_fname}-sf.cif', qmax=qmax, rotk=[1,1,1], rottheta=np.radians(30))
sphv_supp = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_supp.fill_from_cif(cif_supp)
sphv_supp.make_mask()




# qloc = np.unique(sphv_supp.ls_pts(inds=1)[:,0])
# print(qloc)

plt.figure()
plt.plot(sphv_supp.vol.sum(axis=-1).sum(axis=-1))
plt.xlabel('Q index')
plt.ylabel('Bragg Multi.')




sphv_supp.plot_slice(0,242)

dxsupp = 2
for pti in sphv_supp.ls_pts(inds=True):
    xul = int(pti[0]-dxsupp), int(pti[0]+dxsupp+1)
    yul = int(pti[1]-dxsupp), int(pti[1]+dxsupp+1)
    zul = int(pti[2]-dxsupp), int(pti[2]+dxsupp+1)

    sphv_supp.vol[xul[0]:xul[1], yul[0]:yul[1], zul[0]:zul[1]] = 1


    if zul[1]>sphv_supp.nz:
        sphv_supp.vol[xul[0]:xul[1], yul[0]:yul[1], 0:zul[1]-sphv_supp.nz] = 1

    if zul[0]<0:
        sphv_supp.vol[xul[0]:xul[1], yul[0]:yul[1], zul[0]:] = 1
        sphv_supp.vol[xul[0]:xul[1], yul[0]:yul[1], 0:zul[1]] = 1



sphv_supp.plot_slice(0, 242)











# # Generate Data (from corr)
corr_data = scorpy.CorrelationVol(nq, npsi, qmax)
corr_data.fill_from_cif(cif_targ, verbose=2)

blqq_data_full = scorpy.BlqqVol(nq, nl, qmax)
blqq_data_full.fill_from_corr(corr_data, rcond=rcond, verbose=1)

blqq_data_crop = blqq_data_full.copy()
blqq_data_crop.vol[:,:,lcrop:] = 0



# corr_calc = scorpy.CorrelationVol(nq, npsi, qmax)
# corr_calc.fill_from_blqq(blqq_data, verbose=1)



# # Make directory to save vols
os.mkdir(f'{scorpy.DATADIR}/algo/{recon_tag}')

sphv_targ.save(f'{scorpy.DATADIR}/algo/{recon_tag}/sphv_{recon_tag}_targ.dbin')
cif_targ.save(f'{scorpy.DATADIR}/algo/{recon_tag}/{recon_tag}_targ-sf.cif')
sphv_supp.save(f'{scorpy.DATADIR}/algo/{recon_tag}/sphv_{recon_tag}_supp.dbin')
blqq_data_crop.save(f'{scorpy.DATADIR}/algo/{recon_tag}/blqq_{recon_tag}_data.dbin')

# blqq_data_full.save(f'{scorpy.DATADIR}/algo/{recon_tag}/blqq_full_{recon_tag}_data.dbin')
# corr_data.save(f'{scorpy.DATADIR}/algo/{tag}/qcor_{tag}_data.dbin')
# corr_calc.save(f'{scorpy.DATADIR}/algo/{tag}/qcor_{tag}_calc.dbin')







plt.show()






