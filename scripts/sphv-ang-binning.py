import matplotlib.pyplot as plt
import numpy as np
import scorpy
from scorpy.utils import norm01


sphv1 = scorpy.SphericalVol(path='../data/dbins/sphharm_sphv1')
sphv2 = scorpy.SphericalVol(path='../data/dbins/sphharm_sphv2')

corr1 = scorpy.CorrelationVol(path='../data/dbins/sphharm_qcor1')
corr2 = scorpy.CorrelationVol(path='../data/dbins/sphharm_qcor2')


sphv1.plot_slice(0, 2)
plt.title('sphv x1')
sphv2.plot_slice(0, 2)
plt.title('sphv x2')
corr1.plot_q1q2()
plt.title('corr x1')
corr2.plot_q1q2()
plt.title('corr x2')


plt.figure()
plt.plot(corr1.psipts, norm01(corr1.get_xy()[1, :]), 'b-.', label='corr11')
plt.plot(corr2.psipts, norm01(corr2.get_xy()[1, :]), 'b-', label='corr21')
plt.plot(corr1.psipts, norm01(corr1.get_xy()[2, :]), 'r-.', label='corr12')
plt.plot(corr2.psipts, norm01(corr2.get_xy()[2, :]), 'r-', label='corr22')
plt.plot(corr1.psipts, norm01(corr1.get_xy()[3, :]), 'g-.', label='corr13')
plt.plot(corr2.psipts, norm01(corr2.get_xy()[3, :]), 'g-', label='corr23')
# # plt.plot(corr1.psipts, norm01(corr1.get_xy()[4, :]), label='corr14')
# # plt.plot(corr1.psipts, norm01(corr1.get_xy()[5, :]), label='corr15')

# # plt.plot(corr2.psipts, norm01(corr2.get_xy()[4, :]), label='corr24')
# # plt.plot(corr2.psipts, norm01(corr2.get_xy()[5, :]), label='corr25')
plt.legend()


plt.show()
