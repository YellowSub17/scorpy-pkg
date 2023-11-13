import scorpy
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

plt.rc('font', size=8)


cif = scorpy.CifData('/home/ec2-user/corr/data/xtal/193l-sf.cif')
q_inte_r = min(cif.ast_mag, cif.bst_mag, cif.cst_mag)



pdb_code ='193l'
xtal_size = '100nm'
geom_code = f'19MPz040'
super_chunk = 'x1'
chunk=5
frame = 30


npz_dir =  f'/home/ec2-user/corr/data/frames/{xtal_size}-{geom_code}-{super_chunk}/{chunk}/'
npz_fname = f'{npz_dir}/{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-{chunk}-{frame}.npz'
pk = scorpy.PeakData(npz_fname, f'/home/ec2-user/corr/data/geom/{geom_code}.geom')
r_inte_r = pk.convert_q2r(q_inte_r)/2

fig, axes = plt.subplots(1,1, figsize=(8/2.54, 8/2.54), dpi=300)
pk.plot_peaks(fig=fig, ax=axes)
pk.plot_peakr(r_inte_r, fig=fig, ax=axes)


# ax_x = axes.twinx()
# ax_y = axes.twiny()
# ax_x.set_xlim([-31., -39.])
# ax_y.set_ylim([-40.25, -48.25])
# ax_x.set_xticks([-35.3])
# ax_y.set_yticks([-44.2])


# axes.set_xlim([-0.031, -0.039])
# axes.set_ylim([-0.04025, -0.04825])

axes.set_xlim([-0.03025, -0.03950])
axes.set_ylim([-0.0395, -0.04875])
axes.set_xticks([-0.0353])
axes.set_yticks([-0.0442])

axes.yaxis.set_label_coords(-0.05, 0.01)
axes.xaxis.set_label_coords(0.95, -0.05)



# plt.tight_layout()
plt.savefig("/home/ec2-user/corr/data/figs/aws-frame-eg-unint.png")









fig, axes = plt.subplots(1,1, figsize=(8/2.54, 8/2.54), dpi=300)
inte = pk.integrate_peaks(r_inte_r)
pk.calc_scat(inte[:,0:3], inte[:,-1])
pk.plot_peaks(fig=fig, ax=axes)
pk.plot_qring(0.4)
pk.plot_qring(1.5)

# for i in [0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.4]:
    # pk.plot_qring(i)

axes.set_xlim([-0.15, 0.15])
axes.set_ylim([-0.15, 0.15])

axes.set_xticks([-0.1,  0, 0.1])
axes.set_yticks([-0.1,  0, 0.1])

# pk.plot_qring(40)
# pk.plot_qring(150)
# axes.set_xlim([-15, 15])
# axes.set_ylim([-15, 15])

axes.set_xlabel(f'x [m]')
axes.set_ylabel(f'y [m]')


# plt.tight_layout()
plt.savefig("/home/ec2-user/corr/data/figs/aws-frame-eg-int.png")




plt.show()












