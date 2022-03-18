#!/usr/bin/env python3

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')

# # # Parameters
nq= 150
npsi = 360*32
qmax = 6.3

nl = 90
rcond = 0.1

loose_supp = True

ntheta = nl*2
nphi = ntheta*2







tag = 'nicotineamide-dres1-loose-supp-bigpsi-crop-poles'
cif_fname = 'nicotineamide-sf.cif'




# # # Generate Target
cif_targ = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/{cif_fname}', qmax=qmax, crop_poles=True)

sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif_targ)

qloc = np.unique(np.where(sphv_targ.vol !=0)[0])


# # # Generate Support 
cif_supp = scorpy.CifData(f'{scorpy.DATADIR}/xtal/{cif_fname}', qmax = qmax, crop_poles=True)
sphv_supp = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_supp.fill_from_cif(cif_supp)
sphv_supp.make_mask()



sphv_supp.convolve()
loc = sphv_supp.vol > 0.2
sphv_supp.vol[loc] = 1
sphv_supp.vol[~loc] = 0









# # # Generate Data (from corr)
corr_data = scorpy.CorrelationVol(nq, npsi, qmax)
corr_data.fill_from_cif(cif_targ, verbose=2)

blqq_data = scorpy.BlqqVol(nq, nl, qmax)
blqq_data.fill_from_corr(corr_data, rcond=0.1)

corr_calc = scorpy.CorrelationVol(nq, npsi, qmax)
corr_calc.fill_from_blqq(blqq_data)


# # # # Generate Data (from harm)
# iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
# iqlm_targ.fill_from_sphv(sphv_targ)
# sphv_harmed = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
# sphv_harmed.fill_from_iqlm(iqlm_targ)
# blqq_data = scorpy.BlqqVol(nq, nl, qmax)
# blqq_data.fill_from_iqlm(iqlm_targ)
# blqq_data.vol[:,:,41:] *=0
# corr_calc = scorpy.CorrelationVol(nq, npsi, qmax)
# corr_calc.fill_from_blqq(blqq_data)





# # # # Make directory to save vols
os.mkdir(f'{scorpy.DATADIR}/algo/{tag}')

sphv_targ.save(f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
cif_targ.save(f'{scorpy.DATADIR}/algo/{tag}/{tag}_targ-sf.cif')
sphv_supp.save(f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')
blqq_data.save(f'{scorpy.DATADIR}/algo/{tag}/blqq_{tag}_data.dbin')
corr_calc.save(f'{scorpy.DATADIR}/algo/{tag}/qcor_{tag}_calc.dbin')
corr_data.save(f'{scorpy.DATADIR}/algo/{tag}/qcor_{tag}_data.dbin')




qloc = np.unique(sphv_targ.ls_pts(inds=True)[:,0])
print(qloc)

qq = -5


sphv_targ.plot_slice(0, qq)
sphv_supp.plot_slice(0, qq)

blqq_data.plot_q1q2()
corr_data.plot_q1q2()
corr_calc.plot_q1q2()

# x = sphv_targ.copy()
# x.make_mask()
# x.vol +=sphv_supp.vol
# x.plot_slice(0,qq)




plt.show()






