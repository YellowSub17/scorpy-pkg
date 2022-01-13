#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')

import matplotlib.colors as pltc
from matplotlib import cm






# ncolors=10
# cmap = cm.viridis(np.linspace(0,1,ncolors))
# cmap[0, :] = [0,0,0,1]
# cmap[1, :] = [0,0,0,1]
# cmap = pltc.ListedColormap(cmap)




# qloc = np.unique(np.where(ss.vol>0)[0])
# qq = qloc[-14]
qq=128



tag = 'fcc_inten_r_5pc0_supp_t'
# tag = 'fcc_inten_r1_supp_t'
### Error Plot
plt.figure()
plt.tight_layout()
plt.title('FCC Random Intensity')

y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/a/errs_{tag}_a.txt', delimiter=',', usecols=0)
plt.plot(np.log10(y[1:]), label='Run A', color='r')

y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/b/errs_{tag}_b.txt', delimiter=',', usecols=0)
plt.plot(np.log10(y[1:]), label='Run B', color='g')

y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/c/errs_{tag}_c.txt', delimiter=',', usecols=0)
plt.plot(np.log10(y[1:]), label='Run C', color='b')

plt.xlabel('Iteration Number')
plt.ylabel('$\\log_{10}(\\epsilon)$')
plt.legend()


figsize = (6,6)
dpi = 125


fig, axes = plt.subplots(2,2, sharex=True, sharey=True, figsize=figsize, dpi=dpi)


plt.tight_layout()

cmap = 'viridis'

blur = 1
s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
s.plot_slice(0, qq, title='Target Intensity', cmap=cmap, fig=fig, axes=axes[0,0], blur=blur, ylabel='$\\theta$ [rad]')

s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/a/sphv_{tag}_a_final.dbin')
s.plot_slice(0, qq, title='Run A', cmap=cmap, fig=fig, axes=axes[0,1], blur=blur)

s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/b/sphv_{tag}_b_final.dbin')
s.plot_slice(0, qq, title='Run B', cmap=cmap, fig=fig, axes=axes[1,0], blur=blur, ylabel='$\\theta$ [rad]', xlabel='$\\phi$ [rad]')

s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/c/sphv_{tag}_c_final.dbin')
s.plot_slice(0, qq, title='Run C', cmap=cmap, fig=fig, axes=axes[1,1], blur=blur, xlabel='$\\phi$ [rad]')











plt.show()
