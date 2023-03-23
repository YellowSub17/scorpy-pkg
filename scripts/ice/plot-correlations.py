
import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')







log=True
# power=0.125
power=1



# log=True
# power = 1

qpsi=True

selfcorrbuff=2



corr3d = scorpy.CorrelationVol(path='/media/pat/datadrive/ice/sim/corr/hex-ice-qcor.npy')
corr3d.vol = corr3d.vol**(power)
if log:
    corr3d.vol = np.log10(np.abs(corr3d.vol)+1)
corr3d.plot_q1q2(title='3d')



print(f'{power=}, {log=}')
for size in ['1000nm', '500nm', '250nm', '125nm']:
    print('')

    fig, axes = plt.subplots(2,2)
    plt.suptitle(f'{size} {log=} {power=}')

    corra = scorpy.CorrelationVol(path=f'/media/pat/datadrive/ice/sim/corr/hex-ice-{size}-qmin75-19MPz18-a-qcor.dbin')
    corrb = scorpy.CorrelationVol(path=f'/media/pat/datadrive/ice/sim/corr/hex-ice-{size}-qmin75-19MPz18-b-qcor.dbin')

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




    corra.plot_q1q2(fig=fig, axes=axes[0,0],  ylabel='20k')
    corrb.plot_q1q2(fig=fig, axes=axes[0,1], )


    


    print(f'20k {size=} x=y {scorpy.utils.utils.cosinesim(corra.get_xy(), corrb.get_xy())}')
    print(f'20k {size=} vol {scorpy.utils.utils.cosinesim(corra.vol, corrb.vol)}')




    corra = scorpy.CorrelationVol(path=f'/media/pat/datadrive/ice/sim/corr/19MPz18/{size}-qmin75/hex-ice-{size}-qmin75-19MPz18-2-a-qcor.npy')
    corrb = scorpy.CorrelationVol(path=f'/media/pat/datadrive/ice/sim/corr/19MPz18/{size}-qmin75/hex-ice-{size}-qmin75-19MPz18-2-b-qcor.npy')

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




    corra.plot_q1q2(fig=fig, axes=axes[1,0],  ylabel='125', xlabel='a')
    corrb.plot_q1q2(fig=fig, axes=axes[1,1],  xlabel='b')


    print(f'125 {size=} x=y {scorpy.utils.utils.cosinesim(corra.get_xy(), corrb.get_xy())}')
    print(f'125 {size=} vol {scorpy.utils.utils.cosinesim(corra.vol, corrb.vol)}')

    plt.tight_layout()








plt.show()
