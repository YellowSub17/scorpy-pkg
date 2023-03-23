



import h5py
import scorpy
import numpy as np
import scipy as sp
import os
import sys



chunk = sys.argv[1]
npatterns = int(sys.argv[2])
xtal_size = sys.argv[3]
geom = sys.argv[4]

prefix = f'hex-ice-{xtal_size}nm-{geom}-{chunk}'
path = f'{scorpy.DATADIR}/ice/sim/patterns/{geom}/{xtal_size}nm'


pk = scorpy.PeakData(datapath='nonelol',
                    geompath=f'/media/pat/datadrive/ice/sim/geoms/{geom}.geom')


for i in range(1, npatterns+1):
    fname = f'{path}/{prefix}-{i}'

    with h5py.File(fname+'.h5', 'r') as h5file:
        d = h5file[pk.geom_params['data']][:]

    coo = sp.sparse.coo_matrix(d)
    sp.sparse.save_npz(fname, coo)




