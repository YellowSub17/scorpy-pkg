import scorpy
import numpy as np
import matplotlib.pyplot as plt





data_dir = '/home/ec2-user/corr/data'
xtal_size= '100nm'
geom_code = '19MPz040'
pdb_code = '193l'




y = []
y2 = []

for i in range(7):
    nframes = (2**i)*256

    corr_ab_dir =  f'{data_dir}/qcor/nsums'
    corra = scorpy.CorrelationVol(path=f'{corr_ab_dir}/{pdb_code}-{xtal_size}-{geom_code}-n{nframes}-a-qcor.dbin')
    corrb = scorpy.CorrelationVol(path=f'{corr_ab_dir}/{pdb_code}-{xtal_size}-{geom_code}-n{nframes}-b-qcor.dbin')

    css = scorpy.utils.utils.cosinesim(corra.vol, corrb.vol)
    y.append(css)

    corra.vol[:,:,0] = 0
    corrb.vol[:,:,0] = 0

    css = scorpy.utils.utils.cosinesim(corra.vol, corrb.vol)
    y2.append(css)
    print(css)


x = np.power(2, np.arange(7))*256
# x = np.arange(7)



plt.figure()
plt.plot(x,y, 'x-b')
plt.plot(x,y2, 'o-b')
plt.show()




# print(scorpy.utils.utils.cosinesim(corra.vol, corrb.vol))
# fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
# corra.plot_q1q2(fig=fig, axes=axes[0], vminmax=(0, 3e5))
# corrb.plot_q1q2(fig=fig, axes=axes[1], vminmax=(0, 3e5))
# plt.show()

