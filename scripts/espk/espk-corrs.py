

import scorpy
from scorpy import __DATADIR
import matplotlib.pyplot as plt

import numpy as np


seed = 0
n = 1024


corr1 = scorpy.CorrelationVol(path=f'{__DATADIR}/dbins/ensemble_peaks/ensemble_n1024_0.dbin')
corr2 = scorpy.CorrelationVol(path=f'{__DATADIR}/dbins/ensemble_peaks/ensemble_n1024_9.dbin')


corr1.plot_q1q2(log=True)
corr2.plot_q1q2(log=True)


x = np.linspace(0, np.pi)
y = 1 / (2 * np.sin(x / 2))
ys = 1.2 / (2 * np.sin(x / 2))

x2 = np.linspace(-1, 1, 1000)
y2 = 1 / (2 * np.sin(np.cos(x2) / 2))
y3 = 1.2 / (2 * np.sin(np.cos(x2) / 2))

plt.figure()
plt.plot(x, y, label='c=1')
plt.plot(x, ys, label='c=1.2')
plt.title('old sampling: c/(2*sin(x/2))')
plt.legend()

plt.figure()
plt.plot(x2, y2, label='c=1')
plt.plot(x2, y3, label='c=1.2')
plt.title('new sampling: c/(2*sin(cos(x)/2))')
plt.legend()


plt.show()


# corr4_0 = scorpy.CorrelationVol(path = f'{__DATADIR}/dbins/ensemble_peaks/ensemble_n4_0.dbin')
# corr4_1 = scorpy.CorrelationVol(path = f'{__DATADIR}/dbins/ensemble_peaks/ensemble_n4_1.dbin')
# # corr1024_0 = scorpy.CorrelationVol(path = f'{__DATADIR}/dbins/ensemble_peaks/ensemble_n1024_0.dbin')
# # corr1024_1 = scorpy.CorrelationVol(path = f'{__DATADIR}/dbins/ensemble_peaks/ensemble_n1024_1.dbin')


# # corr4_0.sub_t_mean()
# # corr4_1.sub_t_mean()
# # corr1024_0.sub_t_mean()
# # corr1024_1.sub_t_mean()


# im4_0 = corr4_0.get_xy()
# im4_1 = corr4_1.get_xy()
# # im1024_0 = corr1024_0.get_xy()
# # im1024_1 = corr1024_1.get_xy()

# plt.figure()
# plt.imshow(np.log10(np.abs(im4_0)+1), origin='lower')
# plt.title('corr N4_0 q1=q2 log10(I)')

# plt.figure()
# plt.imshow(np.log10(np.abs(im4_1)+1), origin='lower')
# plt.title('corr N4_1 q1=q2 log10(I)')

# plt.figure()
# plt.imshow(np.log10(np.abs(im4_1)+1)*np.log10(np.abs(im4_0)+1), origin='lower')
# plt.title('corr N4_1*N4_0 q1=q2 log10(I)')


# plt.figure()
# plt.imshow(np.log10(np.abs(im1024_0)+1), origin='lower')
# plt.title('corr N1024_0 q1=q2 log10(I)')


# plt.figure()
# plt.imshow(np.log10(np.abs(im1024_1)+1), origin='lower')
# plt.title('corr N1024_1 q1=q2 log10(I)')

# plt.figure()
# plt.imshow(np.log10(np.abs(im1024_1)+1)*np.log10(np.abs(im1024_0)+1), origin='lower')
# plt.title('corr N1024_1*N1024_0 q1=q2 log10(I)')


plt.show()
