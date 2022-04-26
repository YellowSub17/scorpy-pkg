import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')


v1 = scorpy.CorrelationVol(50, 90, 2,)
v1.vol = np.random.random(v1.vol.shape)

v1.plot_q1q2()

v1.save(scorpy.DATADIR / 'test.dbin')

v2 = scorpy.CorrelationVol(path=scorpy.DATADIR / 'test.dbin')
v2.plot_q1q2()


plt.show()



