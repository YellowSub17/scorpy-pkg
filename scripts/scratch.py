import scorpy
import numpy as np
import matplotlib.pyplot as plt






v = scorpy.Vol(100, 100, 100, 0, 0, 0, 1,1,1)


v.vol = np.random.random(v.vol.shape)






v.plot_xy()

plt.show()


