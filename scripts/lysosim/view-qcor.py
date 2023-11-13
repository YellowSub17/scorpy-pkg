import scorpy
import numpy as np
import matplotlib.pyplot as plt





data_dir = '/home/ec2-user/corr/data'
xtal_size= '100nm'
geom_code = '19MPz040'
pdb_code = '193l'
super_chunk = 'x1'

chunk = 0
frames = [15, 16, 17, 18,19]




# for frame in frames:

    # print('y')
    # npz_fname =  f'{data_dir}/frames/{xtal_size}-{geom_code}-{super_chunk}/{chunk}/{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-{chunk}-{frame}.npz'
    # pk = scorpy.PeakData(npz_fname, f'/home/ec2-user/corr/data/geom/19MPz040.geom')
    # r_inte = 0.003395225941658224 
    # inte = pk.integrate_peaks(r_inte)
    # pk.calc_scat(inte[:,0:3], inte[:,-1])

    # fig, axes = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300)
    # pk.plot_peaks(fig=fig, ax=axes)
    # plt.title(str(frame))




frame = 15
# frame = 17
# frame = 18


print('x')
corr_dir = f'{data_dir}/qcor/{xtal_size}-{geom_code}-{super_chunk}'
corr = scorpy.CorrelationVol(path=f'{corr_dir}/{chunk}/{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-{chunk}-{frame}-qcor.npy')

corr.convolve(kern_L=5, kern_n=9, std_x=1, std_y=1, std_z=1)
# corr.convolve(kern_L=3, kern_n=11, std_x=0.5, std_y=0.5, std_z=0.5)


fig, axes = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300)
# corr._plot_2D(corr.get_xy(), vminmax=(10,50), fig=fig, axes=axes)
corr.plot_q1q2(vminmax=(10,50), fig=fig, axes=axes)

axes.text(0.38, corr.qpts[21], 'BC' , color=(1,0,0), ha='center')
axes.text(1.58, corr.qpts[19], 'AB' , color=(1,0,0), ha='center')
axes.text(1.91, corr.qpts[8], 'AC' , color=(1,0,0), ha='center')



# axes.text(0.38, corr.qpts[21], 'BC' , color=(1,0,0), ha='center')
# axes.text(1.58, corr.qpts[19], 'AB' , color=(1,0,0), ha='center')
# axes.text(1.91, corr.qpts[10], 'AC' , color=(1,0,0), ha='center')

plt.savefig('/home/ec2-user/corr/data/figs/aws-corr-eg.png')



print('y')
npz_fname =  f'{data_dir}/frames/{xtal_size}-{geom_code}-{super_chunk}/{chunk}/{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-{chunk}-{frame}.npz'
pk = scorpy.PeakData(npz_fname, f'/home/ec2-user/corr/data/geom/19MPz040.geom')
r_inte = 0.003395225941658224 
inte = pk.integrate_peaks(r_inte)
pk.calc_scat(inte[:,0:3], inte[:,-1])

fig, axes = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300)

pk.plot_annulus(qmin=corr.qpts[14], qmax=corr.qpts[19], color=(1,0,0,0.5))
axes.text(-0.0182, +0.0243, 'A' )
axes.text(+0.0424, +0.0256, 'B' )
axes.text(+0.0490, +0.0082, 'C' )

pk.plot_annulus(qmin=corr.qpts[92], qmax=corr.qpts[102], color=(0, 1, 1, 0.5))
axes.text(+0.0351, +0.0976, 'D' )
axes.text(+0.0381, +0.0675, 'E' )
axes.text(-0.0059, -0.1044, 'F' )
axes.text(+0.0546, -0.0896, 'G' )

# pk.plot_annulus(qmin=corr.qpts[74], qmax=corr.qpts[78], color=(1, 0, 1, 0.5))
# pk.plot_annulus(qmin=corr.qpts[144], qmax=corr.qpts[149], color=(0, 1, 1, 0.5))
# axes.text(-0.0686, +0.0959, 'D' )
# axes.text(-0.0441, -0.1170, 'E' )
# axes.text(+0.0140, -0.1230, 'F' )




pk.plot_peaks(fig=fig, ax=axes)

plt.savefig('/home/ec2-user/corr/data/figs/aws-corr-eg-frame.png')


plt.show()



