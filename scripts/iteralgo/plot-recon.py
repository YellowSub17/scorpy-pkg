#!/usr/bin/env python3

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')








tag = 'nicotineamide-dres1-loose-supp-bigpsi-crop-poles'




sphv_targ = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
cif_targ = scorpy.CifData(path=f'{scorpy.DATADIR}/algo/{tag}/{tag}_targ-sf.cif')
sphv_supp = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')
blqq_data = scorpy.BlqqVol(path=f'{scorpy.DATADIR}/algo/{tag}/blqq_{tag}_data.dbin')
# corr_calc = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/algo/{tag}/qcor_{tag}_calc.dbin')
# corr_data = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/algo/{tag}/qcor_{tag}_data.dbin')





qloc = np.unique(sphv_targ.ls_pts(inds=True)[:,0])
print(qloc)

qq = 100



# corr_data.plot_q1q2()
blqq_data.plot_q1q2()
# corr_calc.plot_q1q2()

sphv_targ.plot_slice(0, qq)

sphv_supp.plot_slice(0, qq)




x = sphv_targ.copy()
loc = np.where(x.vol>0)
x.vol[loc] = 1

x.vol += sphv_supp.vol

x.plot_slice(0,qq)



plt.show()









