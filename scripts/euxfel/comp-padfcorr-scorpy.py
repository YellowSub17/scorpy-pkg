
import scorpy
import numpy as np

import os
import matplotlib.pyplot as plt




wavelength = 1.333e-10
clen = 0.1697469375
res = 5000
nq = 100
npsi = 180



# x = 1.1235
# ind = scorpy.utils.index_x(x,0, x, 100)

# print(ind)


# run = 118
# frame_i = 0



# pk = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run{run}_peaks.txt')
# pk = pk.split_frames()[frame_i]
# pk.plot_peaks()


# qmax = pk.qmax
# r = scorpy.utils.convert_q2r(qmax, clen, wavelength*1e10)


# sc_corr = scorpy.CorrelationVol(nq, npsi, qmax, cos_sample=False, inc_self_corr=True)
# print(pk.qmax, sc_corr.qmax)
# sc_corr.fill_from_peakdata(pk)



# # pk = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run{run}_peaks.txt')
# # qmax = pk.qmax
# # r = scorpy.utils.convert_q2r(qmax, clen, wavelength*1e10)
# im = pk.make_im(r=r, fname=f'/tmp/tmp_frame_im.dbin')
# plt.figure()
# plt.imshow(im)

# corr_config = open(f'/tmp/padfcorr_tmp_config.txt', 'w')
# corr_config.write(f'input = /tmp/tmp_frame_im.dbin\n')
# corr_config.write(f'outpath = /tmp\n')
# corr_config.write(f'wavelength = {wavelength}\n')
# corr_config.write(f'pixel_width = {1/res}\n')
# corr_config.write(f'detector_z = {clen}\n')
# corr_config.write(f'nq = {nq}\n')
# corr_config.write(f'nth = {npsi*2}\n')
# corr_config.write(f'tag = padfcorr_tmp_frame\n')
# corr_config.write(f'qmax = {qmax*1e9}\n')
# corr_config.close()

# print('Padfcorr')
# os.system(f'{scorpy.PADFCORRDIR}padfcorr /tmp/padfcorr_tmp_config.txt')

# tmppadfcorrvol = np.fromfile(f'/tmp/padfcorr_tmp_frame_correlation.dbin')
# tmppadfcorrvol = tmppadfcorrvol.reshape((nq, nq, 2*npsi))


# pc_corr = scorpy.CorrelationVol(nq, npsi, qmax, cos_sample=False)
# pc_corr.vol = tmppadfcorrvol[:,:, :npsi]



# pc_corr.plot_sumax(0, log=True)
# sc_corr.plot_sumax(0, log=True)

# pc_corr.plot_q1q2( log=True)
# sc_corr.plot_q1q2( log=True)




pc_corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/cxi/run118_padfcorr_qcor.dbin')
sc_corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/cxi/run118_qcor.dbin')

pc_corr.plot_q1q2(log=True, title='Run 118 - PADFCORR - log10', xlabel='$\\Delta \\Psi$', ylabel='$q_1=q_2$')
sc_corr.plot_q1q2(log=True, title='Run 118 - SCORPY - log10', xlabel='$\\Delta \\Psi$', ylabel='$q_1=q_2$')
# pc_corr.plot_q1q2()
# sc_corr.plot_q1q2()

# pc_corr.plot_sumax(0, log=True)
# sc_corr.plot_sumax(0, log=True)

# pc_corr.plot_sumax(0)
# sc_corr.plot_sumax(0)





















plt.show()



