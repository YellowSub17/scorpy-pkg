#!/usr/bin/env python3

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')




np.random.seed(1)

# Parameters
nq= 200
ntheta = 180
nphi = 360
nl = 90

qmax = 89




blqq_data =scorpy.BlqqVol(path=f'{scorpy.DATADIR}/algo/nq100test/blqq_nq100test_data.dbin')
sphv_supp =scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/nq100test/sphv_nq100test_supp.dbin')
a = scorpy.AlgoHandler(blqq_data, sphv_supp, lossy_sphv=True, lossy_iqlm=True, rcond=1e-15)

t1 = time.time()
a.ER()
t2 = time.time()
print(t2-t1)

blqq_data =scorpy.BlqqVol(path=f'{scorpy.DATADIR}/algo/nq200test/blqq_nq200test_data.dbin')
sphv_supp =scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/nq200test/sphv_nq200test_supp.dbin')
a = scorpy.AlgoHandler(blqq_data, sphv_supp, lossy_sphv=True, lossy_iqlm=True, rcond=1e-15)

t1 = time.time()
a.ER()
t2 = time.time()
print(t2-t1)






