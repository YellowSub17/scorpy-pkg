#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')





cif = scorpy.CifData(f"{scorpy.DATADIR}/cifs/fcc-rand-50pc0-sf.cif", qmax=89)

s =scorpy.SphericalVol(200, 180, 360, 89)

s.fill_from_cif(cif)

s.plot_slice(0, 128)




# tag = 'fcc_rand_50pc0'
# sub_tag = 'a'
# qq = 128


# fig, axes = plt.subplots(1,2, sharex=True, sharey=True)

# s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
# s.plot_slice(0, qq, title='targ', fig=fig, axes=axes[0])

# s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')
# s.plot_slice(0, qq, title='supp', fig=fig, axes=axes[1])





# y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/errs_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)

# plt.figure()
# plt.plot(y[1:])

# plt.figure()
# plt.plot(range(201, len(y)), y[201:])




# fig, axes = plt.subplots(1,2, sharex=True, sharey=True)

# s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')
# s.plot_slice(0, qq, title='final', fig=fig, axes=axes[0])

# s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_targ.dbin')
# s.plot_slice(0, qq, title='targ', fig=fig, axes=axes[1])













plt.show()
