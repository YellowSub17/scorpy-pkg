
import numpy as np
import pyshtools as pysh
import matplotlib.pyplot as plt
plt.close('all')

import scorpy


v = scorpy.Vol(20,20,25, 0,0,0, 1,1,1)

v.vol = np.random.random(v.vol.shape)


fig, axes = plt.subplots(2,2)
v.plot_sumax(0, fig, axes[0,0], vminmax=(None, None))

v.plot_sumax(0, fig, axes[0,1], vminmax=(None, 9))
v.plot_sumax(0, fig, axes[1,0], vminmax=(10, None))
v.plot_sumax(0, fig, axes[1,1], vminmax=(9, 10))





plt.show()


# v.plot_xy()

# plt.show()
