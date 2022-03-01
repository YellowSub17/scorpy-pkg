import numpy as np
import h5py

import scorpy

import matplotlib.pyplot as plt
plt.close('all')




fnames = [
    'inten1-qmax0264-2d-ssph-batch-noint-noselfcorr-qcor',
    'inten1-qmax0264-2d-ssph-batch-noint-selfcorr-qcor',
    'inten1-qmax0264-2d-ssph-batch-int-noselfcorr-qcor',
    'inten1-qmax0264-2d-ssph-batch-int-selfcorr-qcor',]






# corr2d_noint_self = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/inten1-qmax0264-2d-ssph-batch-noint-selfcorr-qcor.dbin')
# corr2d_noint_noself = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/inten1-qmax0264-2d-ssph-batch-noint-noselfcorr-qcor.dbin')
# corr2d_int_self = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/inten1-qmax0264-2d-ssph-batch-int-selfcorr-qcor.dbin')
# corr2d_int_noself = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/inten1-qmax0264-2d-ssph-batch-int-noselfcorr-qcor.dbin')
# corr3d = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/inten1-qmax0264-3d-sph-qcor.dbin')





fig, axes = plt.subplots(2,2, sharex=True, sharey=True)
plt.suptitle('2D')
for i, fname in enumerate(fnames):


    corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/{fname}.dbin')

    corr.vol[:,:,:20] = 0
    corr.vol[:,:,-20:] = 0

    corr.plot_q1q2(title=f'{fname[30:]}', fig=fig, axes=axes.flatten()[i])




corr3d = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/inten1-qmax0264-3d-sph-qcor.dbin')
corr3d.plot_q1q2(title=f'3D')



plt.show()

