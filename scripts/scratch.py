
import numpy as np
import pyshtools as pysh
import matplotlib.pyplot as plt
plt.close('all')

import scorpy



print(scorpy.Vol.__doc__)
print(scorpy.Vol.nx.__doc__)
print(scorpy.Vol.ls_pts.__doc__)



# v = scorpy.Vol(10,10,10, 0,0,0, 1,1,1)
# v.vol = np.random.random(v.vol.shape)


# fig, axes = plt.subplots(2,2, figsize=(5,5),dpi=150,  sharey=True, sharex=True)

# v.plot_xy(fig=fig, axes=axes[0,0])
# v.plot_sumax(1, fig=fig, axes=axes[0,1], title='Yahoo!')
# v.plot_sumax(1, fig=fig, axes=axes[1,0], vminmax=(None, 4), ylabel='apple')
# v.plot_sumax(1, fig=fig, axes=axes[1,1], vminmax=(6,None), xlabel='orange')









plt.show()


