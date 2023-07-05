import scorpy
import numpy as np
import matplotlib.pyplot as plt





data_dir = '/home/ec2-user/corr/data'
xtal_size= '100nm'
geom_code = '19MPz040'
pdb_code = '193l'

css = np.zeros((2,7))
x = np.zeros(7)


# for xtal_size in ['100nm', '200nm', '500nm']:
for xtal_size in ['100nm']:
    for super_chunk in range(2):
        for exponent in range(7):
            nframes = (2**exponent)*256
            x[exponent] = nframes
            

            corr_ab_dir =  f'{data_dir}/qcor/nsums'
            corra = scorpy.CorrelationVol(path=f'{corr_ab_dir}/{pdb_code}-{xtal_size}-{geom_code}-x{super_chunk}-n{nframes}-a-qcor.dbin')
            corrb = scorpy.CorrelationVol(path=f'{corr_ab_dir}/{pdb_code}-{xtal_size}-{geom_code}-x{super_chunk}-n{nframes}-b-qcor.dbin')

            corra.vol[:,:,0] = 0
            corrb.vol[:,:,0] = 0

            css_ab = scorpy.utils.utils.cosinesim(corra.vol, corrb.vol)

            css[super_chunk, exponent] = css_ab

            # print(f'{nframes}, x{super_chunk} {css}')

print(css)





plt.figure()
plt.plot(x,css[0,:], 'x', label=f'{xtal_size}')
plt.plot(x,css[1,:], 'x', label=f'{xtal_size}')
plt.show()




# print(scorpy.utils.utils.cosinesim(corra.vol, corrb.vol))
# fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
# corra.plot_q1q2(fig=fig, axes=axes[0], vminmax=(0, 3e5))
# corrb.plot_q1q2(fig=fig, axes=axes[1], vminmax=(0, 3e5))
# plt.show()

