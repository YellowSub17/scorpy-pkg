
import scorpy
import numpy as np

import matplotlib.pyplot as plt
import h5py
import os






qmax=1.8
wavelength = 1.333e-10
clen = 0.1697469375
res = 5000
nq = 100
npsi = 180

r = scorpy.utils.convert_q2r(qmax, clen, wavelength*1e10)

print(qmax, r)


# qmax = scorpy.utils.convert_r2q(r, clen, wavelength*1e10)


pk_mask = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/mask/radial_mask_iwr.h5',qmax=qmax, mask_flag=True)
im = pk_mask.make_im(r=r, fname=f'{scorpy.DATADIR}/cxi/mask/mask_im.dbin', bool_iten=True)

pk_mask.plot_peaks()

plt.figure()
plt.imshow(im)


mask_corr_config = open(f'{scorpy.DATADIR}dbins/cxi/padfcorr/padfcorr_mask_config.txt', 'w')
mask_corr_config.write(f'input = {scorpy.DATADIR}cxi/mask/mask_im.dbin\n')
mask_corr_config.write(f'outpath = {scorpy.DATADIR}dbins/cxi/padfcorr/\n')
mask_corr_config.write(f'wavelength = {wavelength}\n')
mask_corr_config.write(f'pixel_width = {1/res}\n')
mask_corr_config.write(f'detector_z = {clen}\n')
mask_corr_config.write(f'nq = {nq}\n')
mask_corr_config.write(f'nth = {npsi*2}\n') # padfcorr give theta from 0-360, so double ntheta so cut in half later 
mask_corr_config.write(f'tag = padfcorr_mask\n')
mask_corr_config.write(f'qmax = {qmax*1e9}\n')
mask_corr_config.close()

os.system(f'{scorpy.PADFCORRDIR}padfcorr {scorpy.DATADIR}dbins/cxi/padfcorr/padfcorr_mask_config.txt')

padfcorrvol = np.fromfile(f'{scorpy.DATADIR}dbins/cxi/padfcorr/padfcorr_mask_correlation.dbin')

padfcorrvol = padfcorrvol.reshape((nq, nq, 2*npsi))

corr = scorpy.CorrelationVol(nq, npsi, qmax, cos_sample=False)
corr.vol = padfcorrvol[:,:, :npsi]

corr.save(f'{scorpy.DATADIR}dbins/cxi/mask_qcor.dbin')



# corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/cxi/mask/mask_qcor.dbin')
corr.plot_q1q2(xlabel='$\\Delta\\Psi [rad]$', ylabel='$q$ [$\u212b^{-1}$]')
plt.show()










