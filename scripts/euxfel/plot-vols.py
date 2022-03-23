
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches





qmax = 1.45
wavelength = 1.333e-10








run = 113


corr1 = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/cxi/qcors/{run}/run{run}-qcor.dbin')

corr1.vol[:,:,0] = 0


corr1.plot_slice(2, 1, log=True)



corr2 = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/cxi/qcors/npeakmax150/{run}/run{run}-qcor.dbin')

corr2.vol[:,:,0] = 0


corr2.plot_slice(2, 1, log=True)



pk = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run{run}_peaks.txt')


# frames = pk.split_frames()

# for i, frame in enumerate(frames):
    # if frame.scat_pol.shape[0]>150:
        # print(i, frame.scat_pol.shape)


# frames[78].plot_peaks()





corr3 = scorpy.CorrelationVol(100,180, 1.45, cos_sample=False, inc_self_corr=True)

corr3.fill_from_peakdata(pk, verbose=1, npeakmax=150)




corr3.plot_slice(2, 1, log=True)










plt.show()





















plt.show()

