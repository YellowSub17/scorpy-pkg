import numpy as np
import scorpy
import matplotlib.pyplot as plt






runs = [i for i in range(11, 25)] + [i for i in range(40, 61)]

# corr_total = scorpy.CorrelationVol(nq=150, npsi=180, qmax=1.5, qmin=0.4, cos_sample=False)

# for run in runs:
    # datapath = f'/home/ec2-user/corr/data/p11'
    # runpath = f'{datapath}/crystfel_calc/{run}/pk8_thr5_snr5'
    # corr_run = scorpy.CorrelationVol(path=f'{datapath}/qcor/p11_run{run}_total_qcor.dbin')
    # corr_total.vol += corr_run.vol

# corr_total.vol[:,:,0] = 0
# corr_total.plot_q1q2(vminmax=(0, corr_total.vol.mean()), xlabel='$\\psi$', ylabel='$q_1=q_2$', title='All runs')

# # plt.figure()
# # # plt.plot(corr_total.qpts, corr_total.get_xy()[:,0])
# # plt.figure()
# # plt.plot(corr_total.psipts, corr_total.get_xy()[9,:])



# corr_3d = scorpy.CorrelationVol(path='/home/ec2-user/corr/data/qcor/193l_3d_qcor.dbin')

# corr_3d.vol[:,:,0] = 0
# corr_3d.plot_q1q2(xlabel='$\\psi$', ylabel='$q_1=q_2$', title='qcor3d' )

# # plt.figure()
# # plt.plot(corr_3d.psipts, corr_3d.get_xy()[-7,:])
# # plt.figure()
# # plt.plot(corr_3d.psipts, corr_3d.get_xy()[4,:])
# # plt.figure()
# # plt.plot(corr_3d.qpts, corr_3d.get_xy()[:,0])

# plt.figure()
# plt.plot(corr_3d.psipts, corr_3d.get_xy()[9,:])

# corr_3d.qpsi_correction()

# # plt.figure()
# # plt.plot(corr_3d.psipts, corr_3d.get_xy()[-7,:])
# # plt.figure()
# # plt.plot(corr_3d.psipts, corr_3d.get_xy()[4,:])
# # plt.figure()
# # plt.plot(corr_3d.qpts, corr_3d.get_xy()[:,0])

# plt.figure()
# plt.plot(corr_3d.psipts, corr_3d.get_xy()[9,:])

# runs = [13]

# for run in runs:
    # datapath = f'/home/ec2-user/corr/data/p11'
    # runpath = f'{datapath}/crystfel_calc/{run}/pk8_thr5_snr5'
    # corr_run = scorpy.CorrelationVol(path=f'{datapath}/qcor/p11_run{run}_total_qcor.dbin')
    # corr_run.qpsi_correction()


    # corr_run.plot_q1q2(vminmax=(0, corr_run.vol.max()/100), xlabel='$\\psi$', ylabel='$q_1=q_2$', title=f'run {run}')





corrsim = scorpy.CorrelationVol(path=f'/home/ec2-user/corr/data/qcor/nsums/193l-80nm-19MPz040-x1-n32768-s1-qcor.dbin')
corrsimb = scorpy.CorrelationVol(path=f'/home/ec2-user/corr/data/qcor/nsums/193l-80nm-19MPz040-x1-n32768-s2-qcor.dbin')

corrsim.vol +=corrsimb.vol
corrsim.qpsi_correction()







# run = 13
datapath = f'/home/ec2-user/corr/data/p11'

runs = [i for i in range(11, 25)] + [i for i in range(40, 61)]


correxp = corrsim.copy()
correxp.vol *= 0

for run in runs:

    print(run)

    corr_a = scorpy.CorrelationVol(path=f'{datapath}/qcor/thresh1e4/p11_run{run}_a_thresh.dbin')
    corr_b = scorpy.CorrelationVol(path=f'{datapath}/qcor/thresh1e4/p11_run{run}_b_thresh.dbin')

    correxp.vol +=corr_a.vol
    correxp.vol +=corr_b.vol


correxp.qpsi_correction()
# corr_b.qpsi_correction()

correxp.convolve(kern_L =5, kern_n = 7, std_x = 1.0, std_y=1.0, std_z=1.0)



correxp.vol[90:,90:,:] = 0
corrsim.vol[90:,90:,:] = 0

fig, axes = plt.subplots(1,3, sharex=True, sharey=True)

corrsim.plot_q1q2(vminmax=(0, 1e6), title='64k simulated 2d patterns',fig=fig, axes=axes[0])
correxp.plot_q1q2(vminmax=(0, 1e7), title='run 13 (intens thresh <1e4)',fig=fig, axes=axes[1])


corr3d = scorpy.CorrelationVol(path='/home/ec2-user/corr/data/qcor/193l_3d_qcor.dbin')
corr3d.plot_q1q2(vminmax=(0, 1e13), title='corr 3d',fig=fig, axes=axes[2])










# runs = [11,12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
# runs = [40, 41, 42]

# runs = [11,12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
# runs = [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]

# runs = [i for i in range(11, 25)] + [i for i in range(40, 61)]
# css = np.zeros( (len(runs), len(runs)) )

# datapath = f'/home/ec2-user/corr/data/p11'

# for i_run_a,  run_a in enumerate(runs):

    # corr_a = scorpy.CorrelationVol(path=f'{datapath}/qcor/p11_run{run_a}_total_qcor.dbin')

    # # corr_a.vol[:, :, 0] = 0
    # corr_a.convolve(kern_L=4, kern_n=7, std_x=2, std_y=2, std_z=2)


    # for i_run_b,  run_b in enumerate(runs[i_run_a:]):

        # corr_b = scorpy.CorrelationVol(path=f'{datapath}/qcor/p11_run{run_b}_total_qcor.dbin')
        # # corr_b.vol[:, :, 0] = 0
        # corr_b.convolve(kern_L=4, kern_n=7, std_x=2, std_y=2, std_z=2)

        # print(run_a, run_b, scorpy.utils.utils.cosinesim(corr_a.vol, corr_b.vol))

        # ab_css =  scorpy.utils.utils.cosinesim(corr_a.vol, corr_b.vol)
        # css[i_run_a, i_run_b+i_run_a] = ab_css
        # if i_run_b>0:
            # css[i_run_b+i_run_a, i_run_a] = ab_css
        # # css[i_run_b, i_run_a] = scorpy.utils.utils.cosinesim(corr_a.vol, corr_b.vol)


# plt.imshow(css)
# plt.colorbar()

# plt.title('css runs 40-60')









plt.show()


