



import h5py
import scorpy
import numpy as np
import scipy as sp



for i in range(1, 3721):
    fname = f'{scorpy.DATADIR}/ice/sim/patterns/hex-ice-1um-{i}'

    with h5py.File(fname+'.h5', 'r') as h5file:
        d = h5file['/entry_1/instrument_1/detector_1/data'][:]

    coo = sp.sparse.coo_matrix(d)
    sp.sparse.save_npz(fname+'.coo', coo)


