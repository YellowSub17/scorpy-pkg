
import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')










for size in ['1000nm', '500nm', '250nm', '125nm']:

    fig, axes = plt.subplots(1,3)

    corr3d = scorpy.CorrelationVol(path='/media/pat/datadrive/ice/sim/corr/hex-ice-qcor.npy')
    corra = scorpy.CorrelationVol(path=f'/media/pat/datadrive/ice/sim/corr/hex-ice-{size}-qmin75-19MPz18-a-qcor.dbin')
    corrb = scorpy.CorrelationVol(path=f'/media/pat/datadrive/ice/sim/corr/hex-ice-{size}-qmin75-19MPz18-b-qcor.dbin')



    corr3d.vol[:,:, :10] = 0
    corr3d.vol[:,:, -10:] = 0
    corra.vol[:,:, :10] = 0
    corrb.vol[:,:, :10] = 0




    corra.qpsi_correction()
    corrb.qpsi_correction()

    corr3d.convolve()


    corr3d.plot_q1q2(log=True, fig=fig, axes=axes[0], title='3d')
    corra.plot_q1q2(log=True,  fig=fig, axes=axes[1], title=f'{size} a')
    corrb.plot_q1q2(log=True,  fig=fig, axes=axes[2], title=f'{size} b')


    corra.vol = np.log10(np.abs(corra.vol)+1)
    corrb.vol = np.log10(np.abs(corra.vol)+1)


    print(f'{size=} {scorpy.utils.utils.cosinesim(corra.vol, corrb.vol)}')









plt.show()
