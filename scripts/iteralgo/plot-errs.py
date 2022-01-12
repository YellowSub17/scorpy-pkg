#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')





tag = 'fcc_inten_r1_supp_t'
tag = 'fcc_inten_r_5pc0_supp_t'
# tag = '4lzt_supp_t'
# tag = 'ccc_inten_r1_supp_t'


cmap = 'viridis'



st = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
ss = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')


qloc = np.unique(np.where(ss.vol>0)[0])
qq = qloc[-3]
# qq = 18


# st.convolve()
# ss.convolve()
# st.plot_slice(0, 19, cmap=cmap)


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



# psx, psy = 0, 100
# plt.figure()
# plt.title(f'{tag}')
# for sub_tag, color in zip(['a', 'b', 'c'], 'rgb'):
    # sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')
    # plt.plot(sf.vol[ss.vol>0][psx:psy], label=f'{sub_tag}', color=color, marker='x', linestyle="")
# plt.plot(st.vol[ss.vol>0][psx:psy], label='targ', color='purple', marker='x', linestyle="")
# plt.legend()





# fig, axes = plt.subplots(2,2, sharex=True, sharey=True)
# st.plot_slice(0, qq, title='targ', fig=fig, axes=axes[0,0], cmap=cmap)
# for i, sub_tag in enumerate(['a', 'b', 'c']):
    # sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')
    # # # sf.convolve()
    # sf.plot_slice(0, qq, title=f'{sub_tag}', fig=fig, axes=axes.flatten()[i+1], cmap=cmap)


st.plot_slice(0, qq, title='targ', cmap=cmap)
for i, sub_tag in enumerate(['a', 'b', 'c']):
    sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')
    # # sf.convolve()
    sf.plot_slice(0, qq, title=f'{sub_tag}', cmap=cmap)










plt.show()
