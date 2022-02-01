#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')





# tag = 'fcc_inten_r1_supp_t'
tag = 'fcc_inten_r_5pc0_supp_t'
# # tag = '4lzt_supp_t'
# # tag = 'ccc_inten_r1_supp_t'


# tag = 'p1_inten_r0_supp_t'


cmap = 'viridis'



st = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
ss = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')


qloc = np.unique(np.where(ss.vol>0)[0])
# qq = qloc[-22*5]
qq = qloc[-5]





plt.figure()
plt.title(f'{tag}')
for sub_tag, color in zip(['a', 'b', 'c'], 'rgb'):
    y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/errs_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)
    plt.plot(np.log10(y[1:]), label=f'{sub_tag}', color=color)
plt.legend()

plt.figure()
plt.title(f'{tag}')
for sub_tag, color in zip(['a', 'b', 'c'], 'rgb'):
    y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/errs_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)
    plt.plot(y[1:], label=f'{sub_tag}', color=color)
plt.legend()



fig, axes = plt.subplots(2,2, sharex=True, sharey=True)
st.plot_slice(0, qq, title='targ', cmap=cmap, fig=fig, axes=axes[0,0])
for i, sub_tag in enumerate(['a', 'b', 'c']):
    si = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_init.dbin')
    sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')
    sf.plot_slice(0, qq, title=f'{sub_tag}', cmap=cmap, fig=fig, axes=axes.flatten()[i+1])

    print(f'R factors of target vs initial ({sub_tag}) (just peaks)')
    ned = np.sum(np.abs(np.sqrt(si.vol[ss.vol>0])- np.sqrt(st.vol[ss.vol>0])))
    donk = np.sum(np.abs(np.sqrt(st.vol[ss.vol>0])))

    ned = np.sum(np.abs(si.vol[ss.vol>0]- st.vol[ss.vol>0]))
    donk = np.sum(np.abs(st.vol[ss.vol>0]))

    r = ned/donk
    print(r)
    print()

    print(f'R factors of target vs final ({sub_tag}) (just peaks)')
    ned = np.sum(np.abs(np.sqrt(sf.vol[ss.vol>0]) - np.sqrt(st.vol[ss.vol>0])))
    donk = np.sum(np.abs(np.sqrt(st.vol[ss.vol>0])))

    ned = np.sum(np.abs(sf.vol[ss.vol>0]- st.vol[ss.vol>0]))
    donk = np.sum(np.abs(st.vol[ss.vol>0]))

    r = ned/donk
    print(r)
    print()









plt.show()
