

import numpy as np
import scorpy
import os
import h5py

import glob
import sys

import matplotlib.pyplot as plt
plt.close('all')


# sizes = ['500nm', '1000nm']
sizes = ['125nm']
geom = '19MPz18'

for size in sizes:

    patterns_path = f'/media/pat/datadrive/ice/sim/patterns/{geom}/{size}/*{size}*.npz'
    print(patterns_path)
    patterns_glob = glob.glob(patterns_path)
    patterns_glob.sort()



    if int(sys.argv[1]) ==0:
        start = 0
        end = 10000
    elif int(sys.argv[1])==1:
        start = 10000
        end = 20000

    elif int(sys.argv[1])==2:
        start = 20000
        end = 30000

    elif int(sys.argv[1])==3:
        start = 30000
        end = 40000


    pk = scorpy.PeakData(datapath=patterns_glob[start:end],
                        geompath=f'/media/pat/datadrive/ice/sim/geoms/{geom}.geom')




    im = pk.make_im(1000, 0.127)

    np.save(f'/media/pat/datadrive/ice/sim/patterns/sums/hex-ice-{size}-{geom}-10k-{sys.argv[1]}', im)

    plt.figure()
    plt.imshow(im, origin='lower')

