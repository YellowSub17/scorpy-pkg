



import scorpy
import numpy as np

import matplotlib.pyplot as plt


v1 = scorpy.Vol(10, 20,30, 12, 24, 180 )


v1.vol = np.random.random((v1.vol.shape))

# v1.plot_xy()

v1.plot_sumax(axis=2)

# v.save_dbin('./test.dbin')

# v2 = scorpy.Vol(path='./test.dbin')

# v.plot_xy()


plt.show()






