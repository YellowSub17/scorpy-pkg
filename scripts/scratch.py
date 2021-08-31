
import numpy as np
import pyshtools as pysh
import matplotlib.pyplot as plt
plt.close('all')

import scorpy


v = scorpy.Vol(10,10,10, 0,0,0, 1,1,1)




v.vol = np.ones(v.vol.shape)


for i in range(10):
    v.vol[i,...] *=i

v.vol +=1




fig, axes = plt.subplots(2,2)


v.plot_xy(fig=fig, axes=axes[0,0])
v.plot_slice(axis=0, index=0, fig=fig, axes=axes[0,1])
v.plot_slice(axis=0, index=2, fig=fig, axes=axes[1,0])
axes[1,0].set_title('snap')
v.plot_slice(axis=2, index=4, fig=fig, axes=axes[1,1], xlabel='x', title='yahoo')








plt.show()


