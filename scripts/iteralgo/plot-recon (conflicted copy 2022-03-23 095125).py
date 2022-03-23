#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')









tag = 'nicotineamide-dres1-loose-supp-bigpsi-crop-poles'
tag = 'anilinomethylphenol'

sub_tags = ['a', 'b', 'c']
# sub_tags = ['long_er']
# sub_tags = ['x']

cmap = 'viridis'



plt.figure()
for sub_tag, color in zip(sub_tags, 'rgb'):
    y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/errs_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)
    plt.plot(np.log10(y[1:]), label=f'{sub_tag}', color=color)
plt.legend()
plt.title(f'{tag}')

plt.figure()
for sub_tag, color in zip(sub_tags, 'rgb'):
    y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/errs_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)
    plt.plot(y[1:], label=f'{sub_tag}', color=color)
plt.legend()
plt.title(f'{tag}')



ss = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')


st = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
qloc = np.unique(np.where(st.vol !=0)[0])
print(qloc)

qq = 51


ss.plot_slice(0, qq, title='supp', cmap=cmap)
fig, axes = plt.subplots(2,2, sharex=True, sharey=True)
plt.tight_layout()
st.plot_slice(0, qq, title='targ', cmap=cmap, fig=fig, axes=axes.flatten()[0], log=False)
for i, sub_tag in enumerate(sub_tags):
    sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')
    si = sf.copy()

    si.integrate_peaks(mask_vol=st)



    si.plot_slice(0,qq, title=f'{tag}_{sub_tag}', cmap=cmap, fig=fig, axes=axes.flatten()[i+1], log=False)

    rf = scorpy.utils.rfactor(si.vol, st.vol)
    print(rf)

    fsc = scorpy.utils.fsc(si.vol, st.vol)

    plt.figure()
    plt.plot(fsc)















plt.show()
