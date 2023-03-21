import numpy as np
import scorpy
import os
import h5py

import glob

import matplotlib.pyplot as plt
plt.close('all')


geom= '19MPz18'
size = '1000nm'


def get_fname(x):
    return f'/media/pat/datadrive/ice/sim/corr/{geom}/{size}-qmin75/hex-ice-{size}-qmin75-{geom}-{x}-a-qcor.npy'


aglob = glob.glob(f'/media/pat/datadrive/ice/sim/corr/{geom}/{size}-qmin75/hex-ice-{size}-qmin75-{geom}-*-a-qcor.npy')
for i in range(1, 161):
    if get_fname(i) in  aglob:
        print(i, True)
    else:

        print(i,False)









plt.show()
