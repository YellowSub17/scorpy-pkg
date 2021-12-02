#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')





tag = 'fcc_intenr_50pc0_tight'
sub_tag = 'a'
qq = 128


# fig, axes = plt.subplots(1,2, sharex=True, sharey=True)

# s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
# s.plot_slice(0, qq, title='targ', fig=fig, axes=axes[0])

# s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')
# s.plot_slice(0, qq, title='supp', fig=fig, axes=axes[1])





y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/errs_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)

plt.figure()
plt.plot(y[1:])

# plt.figure()
# plt.plot(range(201, len(y)), y[201:])




fig, axes = plt.subplots(1,2, sharex=True, sharey=True)

sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')
sf.plot_slice(0, qq, title='final', fig=fig, axes=axes[0])


st = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
st.plot_slice(0, qq, title='targ', fig=fig, axes=axes[1])

plt.figure()
plt.plot(sf.vol[sf.vol>0])
plt.plot(st.vol[sf.vol>0])















plt.show()
