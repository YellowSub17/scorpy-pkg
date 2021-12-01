#!/usr/bin/env python3

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')





# Parameters

tag = 'fcc_rand_50pc0'
sub_tag = 'a'



blqq_data =scorpy.BlqqVol(path=f'{scorpy.DATADIR}/algo/{tag}/blqq_{tag}_data.dbin')
sphv_supp =scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')
sphv_init =scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_init.dbin')
sphv_targ =scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')


a = scorpy.AlgoHandler(blqq_data, sphv_supp, sphv_init=sphv_init,
                       lossy_sphv=True, lossy_iqlm=True, rcond=1e-15)


vals_targ = sphv_targ.vol[a.supp_loc]
plt.figure()
plt.plot(vals_targ)
plt.title('targ vals')

a.sphv_iter.plot_slice(0, 128, title='init')


for i in range(6):
    _,_,err=a.HIO()
    a.sphv_iter.plot_slice(0, 128, title=f'hio {i}')
    print(i, err)

vals_hio = a.sphv_iter.vol[a.supp_loc]
plt.figure()
plt.plot(vals_hio)
plt.title('HIO vals')

for i in range(4):
    _,_,err=a.ER()
    a.sphv_iter.plot_slice(0, 128, title=f'er {i}')
    print(i, err)


vals_er = a.sphv_iter.vol[a.supp_loc]
plt.figure()
plt.plot(vals_er)
plt.title('ER vals')




plt.show()










