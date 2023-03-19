
import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')










for size, vminmax in zip(['1000nm', '500nm', '250nm', '125nm'], [(8,17), (10,12), (10,12), (10,11)]):

    fig, axes = plt.subplots(1,3)

    corr3d = scorpy.CorrelationVol(path='/media/pat/datadrive/ice/sim/corr/hex-ice-qcor.npy')
    corra = scorpy.CorrelationVol(path=f'/media/pat/datadrive/ice/sim/corr/hex-ice-{size}-19MPz18-a-qcor.npy')
    corrb = scorpy.CorrelationVol(path=f'/media/pat/datadrive/ice/sim/corr/hex-ice-{size}-19MPz18-b-qcor.npy')



    corr3d.vol[:,:, :10] = 0
    corr3d.vol[:,:, -10:] = 0
    corra.vol[:,:, :10] = 0
    corrb.vol[:,:, :10] = 0




    corra.qpsi_correction()
    corrb.qpsi_correction()

    corr3d.convolve()


    corr3d.plot_q1q2(log=True, fig=fig, axes=axes[0], title='3d')
    corra.plot_q1q2(log=True, vminmax=vminmax, fig=fig, axes=axes[1], title=f'{size} a')
    corrb.plot_q1q2(log=True, vminmax=vminmax, fig=fig, axes=axes[2], title=f'{size} b')
    plt.suptitle(f'{size}')




# q1, q2, q3 = corra.get_index(x=1.6), corra.get_index(x=1.72), corra.get_index(x=1.815),
# q4 = corra.get_index(x=2.34)
# q5, q6, q7 = corra.get_index(x=2.77), corra.get_index(x=2.9), corra.get_index(x=3.025),

# plt.figure()
# q = q3
# plt.plot(corra.vol[q, q,:]/np.max(corra.vol[q,q,:]))
# plt.plot(corr3d.vol[q, q,:]/np.max(corr3d.vol[q,q,:]))







plt.show()
