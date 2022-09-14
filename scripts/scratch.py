import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')


# v1 = scorpy.CorrelationVol(50, 90, 2,)
# v1.vol = np.random.random(v1.vol.shape)

# v1.plot_q1q2()

# v1.save(scorpy.DATADIR / 'test.dbin')

# v2 = scorpy.CorrelationVol(path=scorpy.DATADIR / 'test.dbin')
# v2.plot_q1q2()


# plt.show()




v = scorpy.SphericalVol(path='/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/data/algo/agno3-d03/sphv_agno3-d03_supp_loose.dbin')



print(np.unique(np.where(v.vol>0)[0]))


qq = 52
v.plot_slice(0, qq, xlabel='$\\phi$ [rad]',ylabel='$\\theta$ [rad]')

qq = 102
v.plot_slice(0, qq, xlabel='$\\phi$ [rad]',ylabel='$\\theta$ [rad]')

qq = 202
v.plot_slice(0, qq, xlabel='$\\phi$ [rad]',ylabel='$\\theta$ [rad]')



plt.show()
