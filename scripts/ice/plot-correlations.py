
import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')







log=False
# power=0.125
power=1



# log=True
# power = 1

qpsi=True

selfcorrbuff=2



corr3d = scorpy.CorrelationVol(path='/media/pat/datadrive/ice/sim/corr/hex-ice-qcor.npy')
corr3d.vol = corr3d.vol**(power)

if qpsi:
    corr3d.qpsi_correction()
if log:
    corr3d.vol = np.log10(np.abs(corr3d.vol)+1)
corr3d.plot_q1q2(title='3d', xlabel='$\\Delta\\Psi$ [rad]', ylabel='q [A-1]')



print(f'{power=}, {log=}')
for size in ['1000nm']:
    print('')

    # fig, axes = plt.subplots(1,2)
    plt.suptitle(f'{size} {log=} {power=}')

    corra = scorpy.CorrelationVol(path=f'/media/pat/datadrive/ice/sim/corr/sums/stds/hex-ice-{size}-qmin15-std-99900-0-a-qcor.dbin')
    corrb = scorpy.CorrelationVol(path=f'/media/pat/datadrive/ice/sim/corr/sums/stds/hex-ice-{size}-qmin15-std-99900-0-b-qcor.dbin')

    corra.vol[:,:, :selfcorrbuff] = 0
    corrb.vol[:,:, :selfcorrbuff] = 0

    if qpsi:
        corra.qpsi_correction()
        corrb.qpsi_correction()


    corra.vol = corra.vol**(power)
    corrb.vol = corrb.vol**(power)

    if log:
        corra.vol = np.log10(np.abs(corra.vol)+1)
        corrb.vol = np.log10(np.abs(corrb.vol)+1)




    # corra.plot_q1q2(fig=fig, axes=axes[0],)
    # corrb.plot_q1q2(fig=fig, axes=axes[1],)

    corra.plot_q1q2()
    corrb.plot_q1q2()



    plt.tight_layout()








plt.show()
