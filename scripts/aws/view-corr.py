import scorpy
import numpy as np
import matplotlib.pyplot as plt





data_dir = '/home/ec2-user/corr/data'
xtal_size= '100nm'
geom_code = '19MPz040'
pdb_code = '193l'





corr_ab_dir =  f'{data_dir}/qcor/{xtal_size}-{geom_code}'
corra = scorpy.CorrelationVol(path=f'{corr_ab_dir}/{pdb_code}-{xtal_size}-{geom_code}-a-qcor.dbin')
corrb = scorpy.CorrelationVol(path=f'{corr_ab_dir}/{pdb_code}-{xtal_size}-{geom_code}-b-qcor.dbin')

# corra = scorpy.CorrelationVol(path=f'{corr_ab_dir}/0/{pdb_code}-{xtal_size}-{geom_code}-0-chunksum-qcor.dbin')
# corrb = scorpy.CorrelationVol(path=f'{corr_ab_dir}/1/{pdb_code}-{xtal_size}-{geom_code}-1-chunksum-qcor.dbin')


# chunk=0
# i_frame=  17
# j_frame=  30
# corra = scorpy.CorrelationVol(path=f'{corr_ab_dir}/0/{pdb_code}-{xtal_size}-{geom_code}-0-{i_frame}-qcor.npy')
# corrb = scorpy.CorrelationVol(path=f'{corr_ab_dir}/0/{pdb_code}-{xtal_size}-{geom_code}-0-{j_frame}-qcor.npy')

# pka = scorpy.PeakData(f'{data_dir}/frames/{xtal_size}-{geom_code}/0/{pdb_code}-{xtal_size}-{geom_code}-0-{i_frame}.npz',
                     # f'{data_dir}/geom/{geom_code}.geom')
# pkb = scorpy.PeakData(f'{data_dir}/frames/{xtal_size}-{geom_code}/0/{pdb_code}-{xtal_size}-{geom_code}-0-{j_frame}.npz',
                     # f'{data_dir}/geom/{geom_code}.geom')
# pka.plot_peaks()
# pkb.plot_peaks()


# css_max = 0
# i_frame_max = -1
# j_frame_max = -1

# for i_frame in range(50):
        # for j_frame in range(i_frame+1, 50):
            # corra = scorpy.CorrelationVol(path=f'{corr_ab_dir}/0/{pdb_code}-{xtal_size}-{geom_code}-0-{i_frame}-qcor.npy')
            # corrb = scorpy.CorrelationVol(path=f'{corr_ab_dir}/0/{pdb_code}-{xtal_size}-{geom_code}-0-{j_frame}-qcor.npy')

            # corra.vol[:,:,0] = 10
            # corrb.vol[:,:,0] = 10


            # both_non_zero = np.logical_not(np.logical_and(corra.vol==0, corrb.vol==0))
            # css = scorpy.utils.utils.cosinesim(corra.vol[both_non_zero], corrb.vol[both_non_zero])

            # if css > css_max:
                # css_max=css
                # i_frame_max = i_frame
                # j_frame_max = j_frame

                # print('\n\n new  max')
                # print(i_frame_max, j_frame_max, css_max)

            # # print(i_frame,j_frame, css, np.sum(both_non_zero), sep='\t', end='\n')

# print('\n\n maxs')
# print(i_frame_max, j_frame_max, css_max)


corra.vol[:,:,0] = 0
corrb.vol[:,:,0] = 0


both_non_zero = np.logical_not(np.logical_and(corra.vol==0, corrb.vol==0))
css = scorpy.utils.utils.cosinesim(corra.vol[both_non_zero], corrb.vol[both_non_zero])
print(css)








# print(scorpy.utils.utils.cosinesim(corra.vol, corrb.vol))
fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
corra.plot_q1q2(fig=fig, axes=axes[0], vminmax=(0, 3e4))
corrb.plot_q1q2(fig=fig, axes=axes[1], vminmax=(0, 3e4))
plt.show()

