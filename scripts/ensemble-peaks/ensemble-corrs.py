

import scorpy
from scorpy.utils import __DATADIR
import matplotlib.pyplot as plt

import numpy as np







corr4_0 = scorpy.CorrelationVol(path = f'{__DATADIR}/dbins/ensemble_peaks/ensemble_n4_0.dbin')
corr4_1 = scorpy.CorrelationVol(path = f'{__DATADIR}/dbins/ensemble_peaks/ensemble_n4_1.dbin')
corr1024_0 = scorpy.CorrelationVol(path = f'{__DATADIR}/dbins/ensemble_peaks/ensemble_n1024_0.dbin')
corr1024_1 = scorpy.CorrelationVol(path = f'{__DATADIR}/dbins/ensemble_peaks/ensemble_n1024_1.dbin')



# corr4_0.sub_t_mean()
# corr4_1.sub_t_mean()
# corr1024_0.sub_t_mean()
# corr1024_1.sub_t_mean()




im4_0 = corr4_0.get_xy()
im4_1 = corr4_1.get_xy()
im1024_0 = corr1024_0.get_xy()
im1024_1 = corr1024_1.get_xy()

plt.figure()
plt.imshow(np.log10(np.abs(im4_0)+1), origin='lower')
plt.title('corr N4_0 q1=q2 log10(I)')

plt.figure()
plt.imshow(np.log10(np.abs(im4_1)+1), origin='lower')
plt.title('corr N4_1 q1=q2 log10(I)')

plt.figure()
plt.imshow(np.log10(np.abs(im4_1)+1)*np.log10(np.abs(im4_0)+1), origin='lower')
plt.title('corr N4_1*N4_0 q1=q2 log10(I)')


plt.figure()
plt.imshow(np.log10(np.abs(im1024_0)+1), origin='lower')
plt.title('corr N1024_0 q1=q2 log10(I)')


plt.figure()
plt.imshow(np.log10(np.abs(im1024_1)+1), origin='lower')
plt.title('corr N1024_1 q1=q2 log10(I)')

plt.figure()
plt.imshow(np.log10(np.abs(im1024_1)+1)*np.log10(np.abs(im1024_0)+1), origin='lower')
plt.title('corr N1024_1*N1024_0 q1=q2 log10(I)')




plt.show()

