#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')




# tags = ['p1-inten-r0-from-corr-lcrop40',
        # 'p1-inten-r0-from-corr-nolcrop',
        # 'p1-inten-r0-from-blqq-lcrop40']

# tags = ['p1-inten-r0-from-corr-lcrop40-small',
        # 'p1-inten-r0-from-blqq-lcrop40-small']


# tags = ['p1-inten-r0-from-blqq-x100',
        # 'p1-inten-r0-from-blqq-x1',
        # 'p1-inten-r0-from-blqq-d100']

tags = ['p1-inten-r0-from-blqq-qloose-supp',
        'p1-inten-r0-from-corr-qloose-supp']


sub_tag = 'c'

cmap = 'viridis'




plt.figure()
for tag, color in zip(tags, 'rgb'):
    y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/errs_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)
    plt.plot(np.log10(y[1:]), label=f'{tag}', color=color)
plt.legend()

plt.figure()
for tag, color in zip(tags, 'rgb'):
    y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/errs_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)
    plt.plot(y[1:], label=f'{tag}', color=color)
plt.legend()



ss = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')
qloc = np.unique(np.where(ss.vol !=0)[0])
qq=qloc[-8]
##-8
##10
##5
##25

st = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')


fig, axes = plt.subplots(2,2, sharex=True, sharey=True)
st.plot_slice(0, qq, title='targ', cmap=cmap, fig=fig, axes=axes.flatten()[0])
ss.plot_slice(0, qq, title='supp', cmap=cmap, fig=fig, axes=axes.flatten()[1])
for i, tag in enumerate(tags):
    sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')

    sf.plot_slice(0,qq, title=f'{tag}', cmap=cmap, fig=fig, axes=axes.flatten()[i+2])






# tag = 'p1-inten-r0-from-corr-nolcrop'

# cmap = 'viridis'


# st = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
# ss = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')

# qq = -1




# plt.figure()
# plt.title(f'{tag}')
# for sub_tag, color in zip(['a', 'b', 'c'], 'rgb'):
    # y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/errs_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)
    # plt.plot(np.log10(y[1:]), label=f'{sub_tag}', color=color)
# plt.legend()

# plt.figure()
# plt.title(f'{tag}')
# for sub_tag, color in zip(['a', 'b', 'c'], 'rgb'):
    # y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/errs_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)
    # plt.plot(y[1:], label=f'{sub_tag}', color=color)
# plt.legend()



# fig, axes = plt.subplots(2,2, sharex=True, sharey=True)
# st.plot_slice(0, qq, title='targ', cmap=cmap, fig=fig, axes=axes[0,0])
# for i, sub_tag in enumerate(['a', 'b', 'c']):
    # si = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_init.dbin')
    # sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')
    # sf.plot_slice(0, qq, title=f'{sub_tag}', cmap=cmap, fig=fig, axes=axes.flatten()[i+1])

    # print(f'R factors of target vs initial ({sub_tag}) (just peaks)')
    # ned = np.sum(np.abs(np.sqrt(si.vol[ss.vol>0])- np.sqrt(st.vol[ss.vol>0])))
    # donk = np.sum(np.abs(np.sqrt(st.vol[ss.vol>0])))

    # ned = np.sum(np.abs(si.vol[ss.vol>0]- st.vol[ss.vol>0]))
    # donk = np.sum(np.abs(st.vol[ss.vol>0]))

    # r = ned/donk
    # print(r)
    # print()

    # print(f'R factors of target vs final ({sub_tag}) (just peaks)')
    # ned = np.sum(np.abs(np.sqrt(sf.vol[ss.vol>0]) - np.sqrt(st.vol[ss.vol>0])))
    # donk = np.sum(np.abs(np.sqrt(st.vol[ss.vol>0])))

    # ned = np.sum(np.abs(sf.vol[ss.vol>0]- st.vol[ss.vol>0]))
    # donk = np.sum(np.abs(st.vol[ss.vol>0]))

    # r = ned/donk
    # print(r)
    # print()









plt.show()
