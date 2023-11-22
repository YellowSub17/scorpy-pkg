import scorpy
import numpy as np
import matplotlib.pyplot as plt
import glob

import scipy as sp

import matplotlib.cm as cm



data_dir = '/home/ec2-user/corr/data'
geom_code = '19MPz040'
pdb_code = '193l'

corr_dir =  f'{data_dir}/qcor/nsums'



nexponents = 8

nframes_x = [ (2**i)*256 for i in range(nexponents) ]


xtal_sizes = [60, 70,80,90,100,125,150,200,500, ]
xtal_sizes = [70,80,90,100,125,150,200,500, ]
xtal_sizes = [80,90,100,125,150,200,500, ]
# xtal_sizes = [80,500 ]


cmap1 = cm.hsv( np.linspace(0.0, 0.8, len(xtal_sizes)))


css_x  =  np.zeros((nexponents, len(xtal_sizes)))


fig1, axes1 = plt.subplots(1,1)
fig2, axes2 = plt.subplots(1,1)

for i, (xtal_size, color) in enumerate(zip(xtal_sizes, cmap1)):


    for exponent in range(nexponents):
        nframes = (2**exponent)*256

        corr_glob = glob.glob(f'{corr_dir}/*{xtal_size}nm*n{nframes}*.dbin')
        corr_glob.sort()

        if len(corr_glob)%2==1:
            corr_glob = corr_glob[:-1]

        css_s  = []
        for corr1fname, corr2fname in zip(corr_glob[::2], corr_glob[1::2]):

            print(corr1fname)
            print(corr2fname)
     
            corr1 = scorpy.CorrelationVol(path=f'{corr1fname}')
            corr2 = scorpy.CorrelationVol(path=f'{corr2fname}')

            # corr1.vol[:,:,0] = 0
            # corr2.vol[:,:,0] = 0

            corr1.qpsi_correction()
            corr2.qpsi_correction()

            css_12 = scorpy.utils.utils.cosinesim(corr1.vol, corr2.vol)
            css_s.append(css_12)

            # axes.plot(nframes, css_12, marker='.', color=color)
        np.save(f'{data_dir}/css/{pdb_code}-{xtal_size}nm-{geom_code}-x1-n{nframes}-css.npy', np.array(css_s))


