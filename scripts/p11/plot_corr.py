import numpy as np
import scorpy
import matplotlib.pyplot as plt






datapath = f'/home/ec2-user/corr/data/'











# corr3d = scorpy.CorrelationVol(path=f'{datapath}/qcor/193l_3d_big_qcor')

# corr3d.qpsi_correction()
# corr3d.zmean_subtraction()
# # corr3d.plot_q1q2(title='corr 3d',log=True)
# corr3d.plot_q1q2(title='corr 3d')



# corr_thresh = scorpy.CorrelationVol(200, 5760, 1.5, 0.4, cos_sample=False)

# import sys
# option = int(sys.argv[1])
# tag = sys.argv[2]



# i_min = option
# i_max = option + 4





# print(i_min, i_max)
# for i in range(i_min, i_max):
    # print(i)
    # corr_fname = f'{datapath}/p11/qcor/thresh_d5k/p11_allruns_d5k_{i}_{tag}_qcor'
    # corr = scorpy.CorrelationVol(path=corr_fname)
    # corr_thresh.vol +=corr.vol
    # del corr
# corr_thresh.save(f'{datapath}/p11/qcor/thresh_d5k/p11_allruns_d20k_{i_min}_{tag}_qcor')




xy_lower = 0.48
xy_upper = 0.56

fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
corr_a = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_0-5k_a_qcor')
corr_a.qpsi_correction()
corr_a.convolve(kern_L=9, kern_n=15, std_x=3, std_y=3, std_z=6)
corr_a.plot_q1q2(vminmax=(0, 5*corr_a.vol.mean()), fig=fig, axes=axes[0])

axes[0].hlines([xy_lower, xy_upper], corr_a.zmin, corr_a.zmax, color=(1,0,0,0.5), linestyle='dashed')


corr_b = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_0-5k_b_qcor')
corr_b.qpsi_correction()
corr_b.convolve(kern_L=9, kern_n=15, std_x=3, std_y=3, std_z=6)
corr_b.plot_q1q2(vminmax=(0, 5*corr_a.vol.mean()), fig=fig, axes=axes[1])

axes[1].hlines([xy_lower, xy_upper], corr_a.zmin, corr_a.zmax, color=(1,0,0,0.5), linestyle='dashed')

print(scorpy.utils.utils.cosinesim(corr_a.vol, corr_b.vol))


# corr3d = scorpy.CorrelationVol(path=f'{datapath}/qcor/193l_3d_big_qcor')
# corr3d.qpsi_correction()
# corr3d.convolve(kern_L=9, kern_n=15, std_x=3, std_y=3, std_z=6)
# corr3d.plot_q1q2(vminmax=(0, 5*corr3d.vol.mean()),title='corr 3d', fig=fig, axes=axes[2])

# axes[2].hlines([xy_lower, xy_upper], corr_a.zmin, corr_a.zmax, color=(1,0,0,0.5), linestyle='dashed')




line1 = corr_a.get_integrated_xy_line(xy_lower, xy_upper)
line2 = corr_b.get_integrated_xy_line(xy_lower, xy_upper)
# line3 = corr3d.get_integrated_xy_line(xy_lower, xy_upper)
# fig, axes = plt.subplots(1,1, sharex=True, sharey=True)
plt.figure()
plt.plot(line1/np.max(line1))
plt.plot(line2/np.max(line2))
# plt.plot(line3/np.max(line3))


print(scorpy.utils.utils.cosinesim(line1, line2))





plt.show()









# corr = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d5k_0_a_qcor')
# corr.save(f'{datapath}/p11/qcor/thresh/p11_allruns_0-5k_a_qcor')
# corr = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d5k_0_b_qcor')
# corr.save(f'{datapath}/p11/qcor/thresh/p11_allruns_0-5k_b_qcor')

# corr1 = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d5k_0_a_qcor')
# corr2 = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d5k_1_a_qcor')
# corr1.vol +=corr2.vol
# corr1.save(f'{datapath}/p11/qcor/thresh/p11_allruns_0-10k_a_qcor')

# corr1 = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d5k_0_b_qcor')
# corr2 = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d5k_1_b_qcor')
# corr1.vol +=corr2.vol
# corr1.save(f'{datapath}/p11/qcor/thresh/p11_allruns_0-10k_b_qcor')

# corr = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d20k_0_a_qcor')
# corr.save(f'{datapath}/p11/qcor/thresh/p11_allruns_0-20k_a_qcor')
# corr = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d20k_0_b_qcor')
# corr.save(f'{datapath}/p11/qcor/thresh/p11_allruns_0-20k_b_qcor')



# corr1 = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d20k_0_a_qcor')
# corr2 = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d20k_1_a_qcor')
# corr1.vol +=corr2.vol
# corr1.save(f'{datapath}/p11/qcor/thresh/p11_allruns_0-40k_a_qcor')

# corr1 = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d20k_0_b_qcor')
# corr2 = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d20k_1_b_qcor')
# corr1.vol +=corr2.vol
# corr1.save(f'{datapath}/p11/qcor/thresh/p11_allruns_0-40k_b_qcor')

# corr1 = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d20k_0_a_qcor')
# corr2 = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d20k_1_a_qcor')
# corr3 = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d20k_2_a_qcor')
# corr4 = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d20k_3_a_qcor')
# corr1.vol +=corr2.vol +corr3.vol + corr4.vol
# corr1.save(f'{datapath}/p11/qcor/thresh/p11_allruns_0-80k_a_qcor')

# corr1 = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d20k_0_b_qcor')
# corr2 = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d20k_1_b_qcor')
# corr3 = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d20k_2_b_qcor')
# corr4 = scorpy.CorrelationVol(path=f'{datapath}/p11/qcor/thresh/p11_allruns_d20k_3_b_qcor')
# corr1.vol +=corr2.vol +corr3.vol + corr4.vol
# corr1.save(f'{datapath}/p11/qcor/thresh/p11_allruns_0-80k_b_qcor')




