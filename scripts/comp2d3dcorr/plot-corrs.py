import numpy as np
import h5py

import scorpy

import matplotlib.pyplot as plt
import matplotlib.patches as patches
plt.close('all')



# corr3d = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/inten1/inten1-qmax0264-3d-qcor.dbin')
# corr2d =  scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/inten1/inten1-qmax0264-2d-qcor.dbin')


# corr2d_inte = corr2d.copy()
# corr2d_inte.vol *=0

# corr3d_inte = corr2d.copy()
# corr3d_inte.vol *=0

# inte_rq = 0.0100
# inte_rt = np.pi/25


# for point, inds in zip(corr3d.ls_pts(), corr3d.ls_pts(inds=True)):
    # s, loc = corr2d.integrate_region(point[0], point[1], point[2], inte_rq, inte_rq, inte_rt)
    # npixforthispeak = len(np.where(corr2d.vol[loc]>0)[0])
    # corr2d_inte.vol[int(inds[0]), int(inds[1]), int(inds[2])] = s

    # s, loc = corr3d.integrate_region(point[0], point[1], point[2], inte_rq, inte_rq, inte_rt)
    # npixforthispeak = len(np.where(corr3d.vol[loc]>0)[0])
    # corr3d_inte.vol[int(inds[0]), int(inds[1]), int(inds[2])] = s




# corr3d_inte.save(f'{scorpy.DATADIR}/dbins/inten1/inten1-qmax0264-3d-inte-qcor.dbin')
# corr2d_inte.save(f'{scorpy.DATADIR}/dbins/inten1/inten1-qmax0264-2d-inte-qcor.dbin')



# corr2d_inte = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/inten1/inten1-qmax0264-2d-inte-qcor.dbin')
# corr2d_inte.qpsi_correction()
# corr3d_inte = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/inten1/inten1-qmax0264-3d-inte-qcor.dbin')



# blqq2d = scorpy.BlqqVol(corr2d_inte.nq, 90, corr2d_inte.qmax)
# blqq2d.fill_from_corr(corr2d_inte,rcond=0.1)
# blqq3d = scorpy.BlqqVol(corr3d_inte.nq, 90, corr3d_inte.qmax)
# blqq3d.fill_from_corr(corr3d_inte, rcond=0.1)



# blqq2d.plot_q1q2()
# blqq3d.plot_q1q2()
# plt.show()











# for b in [0, 10, 50, 100, 200, 500, 1000, 2000]:
for b in [0, 10, 50, 70]:
    corr3d = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/intenr-qmax0264-3d-qcor.dbin')
    corr2d =  scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/intenr-qmax0264-2d-qcor.dbin-batch{b}.dbin')

    corr2d.plot_q1q2(log=True, title=f'2D log')

    inte_rq = 0.0100
    inte_rt = np.pi/25


    for pt in corr3d.ls_pts():
        if pt[0] ==pt[1]:
            rect = patches.Rectangle((pt[2] -inte_rt, pt[0]-inte_rq), inte_rt*2, inte_rq*2, 0,
                                     fill=False, ec=np.random.random((1,3)), alpha=1, lw=1)
            plt.gca().add_patch(rect)

    rect = patches.Rectangle((np.pi/2 -inte_rt, 0.2020-inte_rq), inte_rt*2, inte_rq*2, 0,
                             fill=False, ec='red', alpha=1, lw=1)
    plt.gca().add_patch(rect)



    corr2d_inte = corr2d.copy()
    corr2d_inte.vol *=0

    corr3d_inte = corr2d.copy()
    corr3d_inte.vol *=0


    for point, inds in zip(corr3d.ls_pts(), corr3d.ls_pts(inds=True)):
        s, loc = corr2d.integrate_region(point[0], point[1], point[2], inte_rq, inte_rq, inte_rt)
        npixforthispeak = len(np.where(corr2d.vol[loc]>0)[0])
        corr2d_inte.vol[int(inds[0]), int(inds[1]), int(inds[2])] = s

        s, loc = corr3d.integrate_region(point[0], point[1], point[2], inte_rq, inte_rq, inte_rt)
        npixforthispeak = len(np.where(corr3d.vol[loc]>0)[0])
        corr3d_inte.vol[int(inds[0]), int(inds[1]), int(inds[2])] = s



    corr2d_inte.save(f'{scorpy.DATADIR}/dbins/corr2d_inte_b{b}.dbin')
    corr3d_inte.save(f'{scorpy.DATADIR}/dbins/corr3d_inte.dbin')







    corr2d_inte = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/corr2d_inte_b{b}.dbin')
    corr3d_inte = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/corr3d_inte.dbin')
    corr2d_inte.qpsi_correction()





# ####### qslice plots
    fig, axes = plt.subplots(1,2)
    plt.suptitle(f'{b}')
    corr3d_inte.plot_q1q2(title='3d integrated q1q2', fig=fig, axes=axes[0])
    corr2d_inte.plot_q1q2(title='2d integrated q1q2', fig=fig, axes=axes[1])

    fig, axes = plt.subplots(1,2)
    plt.suptitle(f'{b}')
    corr3d_inte.plot_slice(0, 58, title='3d integrated q1=58', fig=fig, axes=axes[0])
    corr2d_inte.plot_slice(0, 58, title='2d integrated q1=58', fig=fig, axes=axes[1])


##### corr(q)
#     plt.figure()
    # plt.suptitle(f'{b}')
    # plt.plot(corr2d_inte.qpts, corr2d_inte.get_xy()[:, 90]/np.max(corr2d_inte.get_xy()[:,90]), label='2d')
    # plt.title('2d (q correction)')
    # plt.figure()
    # plt.suptitle(f'{b}')
    # plt.plot(corr3d_inte.qpts, corr3d_inte.get_xy()[:, 90]/np.max(corr3d_inte.get_xy()[:,90]), label='3d')
    # plt.title('3d')
    # plt.legend()


###### corr(psi)
    fig, axes = plt.subplots(4,1)
    plt.suptitle(f'{b}')
    axes[2].plot(corr3d_inte.psipts, corr3d_inte.vol[76, 76,:]/np.max(corr3d_inte.vol[76,76,:]), label='3d')
    axes[2].plot(corr2d_inte.psipts, corr2d_inte.vol[76, 76,:]/np.max(corr2d_inte.vol[76,76,:]), label='2d')
    axes[2].set_title('qq=76')
    axes[2].legend()
    axes[1].plot(corr3d_inte.psipts, corr3d_inte.vol[-17, -17,:]/np.max(corr3d_inte.vol[-17, -17,:]) , label='3d')
    axes[1].plot(corr2d_inte.psipts, corr2d_inte.vol[-17, -17,:]/np.max(corr2d_inte.vol[-17,-17,:]), label='2d')
    axes[1].set_title('qq=-17')
    axes[1].legend()
    axes[3].plot(corr3d_inte.psipts, corr3d_inte.vol[58, 58,:]/np.max(corr3d_inte.vol[58,58,:]), label='3d')
    axes[3].plot(corr2d_inte.psipts, corr2d_inte.vol[58, 58,:]/np.max(corr2d_inte.vol[58,58,:]), label='2d')
    axes[3].set_title('qq=58')
    axes[3].legend()
    axes[0].plot(corr3d_inte.psipts, corr3d_inte.vol[96, 96,:]/np.max(corr3d_inte.vol[96,96,:]), label='3d')
    axes[0].plot(corr2d_inte.psipts, corr2d_inte.vol[96, 96,:]/np.max(corr2d_inte.vol[96,96,:]), label='2d')
    axes[0].set_title('qq=96')
    axes[0].legend()



##### OFF Q1=Q2 SLICE
    # fig, axes = plt.subplots(1,1)
    # plt.suptitle(f'{b}')
    # axes.plot(corr3d_inte.psipts, corr3d_inte.vol[76, -17,:]/np.max(corr3d_inte.vol[76,-17,:]), label='3d')
    # axes.plot(corr2d_inte.psipts, corr2d_inte.vol[76, -17,:]/np.max(corr2d_inte.vol[76,-17,:]), label='2d')
    # axes.set_title('q1=76, q2=-17')
    # axes.legend()

    # fig, axes = plt.subplots(1,1)
    # plt.suptitle(f'{b}')
    # axes.plot(corr3d_inte.psipts, corr3d_inte.vol[58, -17,:]/np.max(corr3d_inte.vol[58,-17,:]), label='3d')
    # axes.plot(corr2d_inte.psipts, corr2d_inte.vol[58, -17,:]/np.max(corr2d_inte.vol[58,-17,:]), label='2d')
    # axes.set_title('q1=58, q2=-17')
    # axes.legend()


    loc = np.unique(np.where(corr3d_inte.vol >0)[0])
    print(loc)







plt.show()

