#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')









tag = 'nicotineamide-dres1-loose-supp-bigpsi-crop-poles'

sub_tags = ['a', 'b', 'c']
# sub_tags = ['er10']

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
qloc = np.unique(np.where(ss.vol !=0)[0])

print(qloc)

qq = 131

st = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')



ss.plot_slice(0, qq, title='supp', cmap=cmap)
fig, axes = plt.subplots(2,2, sharex=True, sharey=True)
plt.tight_layout()
st.plot_slice(0, qq, title='targ', cmap=cmap, fig=fig, axes=axes.flatten()[0], log=False)
for i, sub_tag in enumerate(sub_tags):
    sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')

    sf.plot_slice(0,qq, title=f'{tag}', cmap=cmap, fig=fig, axes=axes.flatten()[i+1], log=False)




# ss = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')
# qloc = np.unique(np.where(ss.vol !=0)[0])

# print(qloc)

# qq = 120

# st = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
# st.plot_slice(0, qq, title=f'target')



# # for count in [1, 2, 4, 8, 16, 32, 59, 60, 61, 62, 64, 68, 76]:
# for count in [1,2,3,4,5,6,7,8,9,10]:
    # s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/er10/sphv_{tag}_er10_c{count}.dbin')

    # s.plot_slice(0, qq, title=f'{count}')

# ss = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')
# ss.plot_slice(0, qq, title=f'support')

# st.make_mask()
# ss.vol+=st.vol
# ss.plot_slice(0, qq, title=f'support')














# # # print(f'R factors of target vs final ({sub_tag}) (just peaks)')
# # # ned = np.sum(np.abs(np.sqrt(sf.vol[ss.vol>0]) - np.sqrt(st.vol[ss.vol>0])))
# # # donk = np.sum(np.abs(np.sqrt(st.vol[ss.vol>0])))

# # # ned = np.sum(np.abs(sf.vol[ss.vol>0]- st.vol[ss.vol>0]))
# # # donk = np.sum(np.abs(st.vol[ss.vol>0]))

# # # r = ned/donk
# # # print(r)
# # # print()












tag = 'p1-inten-r0-from-corr-qloose-supp'


sub_tags = ['a', 'b', 'c']

cmap = 'viridis'




plt.figure()
for sub_tag, color in zip(sub_tags, 'rgb'):
    y = np.loadtxt(f'{scorpy.DATADIR}/algo/old_algo/{tag}/{sub_tag}/errs_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)
    plt.plot(np.log10(y[1:]), label=f'{tag}', color=color)
plt.legend()

plt.figure()
for sub_tag, color in zip(sub_tags, 'rgb'):
    y = np.loadtxt(f'{scorpy.DATADIR}/algo/old_algo/{tag}/{sub_tag}/errs_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)
    plt.plot(y[1:], label=f'{tag}', color=color)
plt.legend()



ss = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/old_algo/{tag}/sphv_{tag}_supp.dbin')
qloc = np.unique(np.where(ss.vol !=0)[0])

print(qloc)

qq = 44



st = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/old_algo/{tag}/sphv_{tag}_targ.dbin')


ss.plot_slice(0, qq, title='supp', cmap=cmap)
fig, axes = plt.subplots(2,2, sharex=True, sharey=True)
st.plot_slice(0, qq, title='targ', cmap=cmap, fig=fig, axes=axes.flatten()[0])
for i, sub_tag in enumerate(sub_tags):
    sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/old_algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')

    sf.plot_slice(0,qq, title=f'{tag}', cmap=cmap, fig=fig, axes=axes.flatten()[i+1])








plt.show()
