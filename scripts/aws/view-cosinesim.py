import scorpy
import numpy as np
import matplotlib.pyplot as plt
import glob


import matplotlib.cm as cm



data_dir = '/home/ec2-user/corr/data'
geom_code = '19MPz040'
pdb_code = '193l'

corr_dir =  f'{data_dir}/qcor/nsums'



nexponents = 8

nframes_x = [ (2**i)*256 for i in range(nexponents) ]


xtal_sizes = ['60nm', '70nm','80nm','90nm','100nm','125nm','150nm','200nm','500nm', ]
xtal_sizes = ['70nm','80nm','90nm','100nm','125nm','150nm','200nm','500nm', ]
xtal_sizes = ['80nm','90nm','100nm','125nm','150nm','200nm','500nm', ]
# xtal_sizes = ['80nm','500nm' ]


cmap1 = cm.hsv( np.linspace(0.0, 0.8, len(xtal_sizes)))







fig, axes = plt.subplots(1,1)

for i, (xtal_size, color) in enumerate(zip(xtal_sizes, cmap1)):

    css_x  =  np.zeros(nexponents)

    for exponent in range(nexponents):
        nframes = (2**exponent)*256

        corr_glob = glob.glob(f'{corr_dir}/*{xtal_size}*n{nframes}*.dbin')
        corr_glob.sort()

        if len(corr_glob)%2==1:
            corr_glob = corr_glob[:-1]

        css_s  = []

        for corr1fname, corr2fname in zip(corr_glob[::2], corr_glob[1::2]):

            print(corr1fname)
            print(corr2fname)
     
            corr1 = scorpy.CorrelationVol(path=f'{corr1fname}')
            corr2 = scorpy.CorrelationVol(path=f'{corr2fname}')

            corr1.vol[:,:,0] = 0
            corr2.vol[:,:,0] = 0

            css_12 = scorpy.utils.utils.cosinesim(corr1.vol, corr2.vol)
            css_s.append(css_12)

            # axes.plot(nframes, css_12, marker='.', color=color)


        css_mean = np.mean(css_s)
        css_err = np.std(css_s)
        # axes.errorbar(nframes, css_mean, yerr=css_err, marker='.',color=color)
        # axes.errorbar(exponent, css_mean, yerr=css_err, marker='.',color=color)
        axes.errorbar(np.log2(nframes), css_mean, yerr=css_err, marker='.',color=color)

        css_x[exponent] = css_mean


    # axes.plot(nframes_x, css_x, label=f'{xtal_size}', color=color)
    # axes.errorbar(exponent, css_mean, yerr=css_err, marker='.',color=color)
    axes.plot(np.log2(nframes_x), css_x, label=f'{xtal_size}', color=color)





plt.legend()

plt.xlabel('Number of Frames [$log_2(x)$]')
plt.ylabel('Cosine Similarity')





plt.show()

