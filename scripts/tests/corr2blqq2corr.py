
import scorpy
from scorpy import __DATADIR
import matplotlib.pyplot as plt







corr1 = scorpy.CorrelationVol(path = '../data/dbins/fcc_qcor')


blqq1 = scorpy.BlqqVol(corr1.nq, 190, corr1.qmax)
blqq1.fill_from_corr(corr1)

corr2 = scorpy.CorrelationVol(corr1.nq, corr1.npsi, corr1.qmax)
corr2.fill_from_blqq(blqq1)

blqq2 = scorpy.BlqqVol(corr1.nq, 190, corr1.qmax)
blqq2.fill_from_corr(corr2)

corr3 = scorpy.CorrelationVol(corr1.nq, corr1.npsi, corr1.qmax)
corr3.fill_from_blqq(blqq2)



corr1.plot_q1q2()
plt.title('FCC original correlation')

blqq1.plot_slice(2,180)
plt.title('blqq1')

corr2.plot_q1q2()
plt.title('correlation 2')

blqq2.plot_slice(2,180)
plt.title('blqq2')

corr3.plot_q1q2()
plt.title('correlation 3')

plt.show()




