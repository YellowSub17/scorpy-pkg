#!/usr/bin/env python3

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')





# Parameters



cif1 = scorpy.CifData(f'{scorpy.DATADIR}/cifs/p1-rand0-sf.cif', qmax=3.8)
print(cif1.qmax)


sphv = scorpy.SphericalVol(200, 180, 360, qmax= cif1.qmax)

sphv.fill_from_cif(cif1)


qq = np.where(sphv.vol.sum(axis=-1).sum(axis=-1)>0)[0]



sphv.plot_slice(0, qq[-22*5])
sphv.plot_slice(0, qq[-20*5])
sphv.plot_slice(0, qq[-5])


sphv.plot_sumax(0)
plt.show()










