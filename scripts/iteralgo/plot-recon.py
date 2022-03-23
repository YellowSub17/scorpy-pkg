#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')









tag = 'nicotineamide-dres1-loose-supp-bigpsi-crop-poles'
tag = 'anilinomethylphenol'
tag = 'agno3'

sub_tags = ['a', 'b', 'c']
# sub_tags = ['long_er']
# sub_tags = ['x']

sub_tags = ['hio10_glopos']

cmap = 'viridis'



# plt.figure()
# for sub_tag, color in zip(sub_tags, 'rgb'):
    # y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/errs_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)
    # plt.plot(np.log10(y[1:]), label=f'{sub_tag}', color=color)
# plt.legend()
# plt.title(f'{tag}')

# plt.figure()
# for sub_tag, color in zip(sub_tags, 'rgb'):
    # y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/errs_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)
    # plt.plot(y[1:], label=f'{sub_tag}', color=color)
# plt.legend()
# plt.title(f'{tag}')


xq = 50

ss = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')

ss.vol[xq:,:,:] =0


st = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
st.vol[xq:,:,:] =0
qloc = np.unique(np.where(st.vol !=0)[0])
print(qloc)

qq = 48


ss.plot_slice(0, qq, title='supp', cmap=cmap)
fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
plt.tight_layout()
st.plot_slice(0, qq, title='targ', cmap=cmap, fig=fig, axes=axes.flatten()[0], log=False)
# st.plot_slice(0, qq, title='targ', cmap=cmap, log=False)
for i, sub_tag in enumerate(sub_tags):
    sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')
    si = sf.copy()
    si.vol[xq:,:,:] =0

    si.integrate_peaks(mask_vol=st)



    si.plot_slice(0,qq, title=f'{tag}_{sub_tag}', cmap=cmap, fig=fig, axes=axes.flatten()[i+1], log=False)
    # si.plot_slice(0,qq, title=f'{tag}_{sub_tag}', cmap=cmap,log=False)

    rf = scorpy.utils.rfactor(si.vol/si.vol.sum(), st.vol/st.vol.sum())
    print(rf)

    fsc = scorpy.utils.fsc(si.vol, st.vol)
    plt.figure()
    plt.plot(fsc)




sd = si.copy()

sd.vol[st.vol!=0] /= st.vol[st.vol!=0]




# for count in range(1,10):
    # sc = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_count{count}.dbin')
    # sc.vol[xq:,:,:] =0
    # sc.integrate_peaks(mask_vol=st)

    # sc.plot_slice(0, qq, title=f'count {count}')










plt.show()
