import random
import matplotlib.pyplot as plt
import scorpy
import numpy as np
np.random.seed(0)


nq = 100
npsi = 700
ntheta = 700
qmax = 1
nl = 341


sphv1 = scorpy.SphericalVol(nq, ntheta, ntheta * 2, qmax)


# scat_sph = np.zeros( (40, 4))

# for i in range(40):
    # q = random.uniform(0, qmax)
    # theta = random.uniform(0, np.pi)
    # phi = random.uniform(0, 2*np.pi)

    # scat_sph[i,:] = [q, theta, phi, 1]


corr1 = scorpy.CorrelationVol(nq, npsi, qmax)


for i in range(40):
    q1 = np.random.randint(nq)
    q2 = np.random.randint(nq)
    p = np.random.randint(npsi)
    corr1.vol[q1, q2, p] += 1
    corr1.vol[q2, q1, p] += 1

corr1.force_sym()

blqq1 = scorpy.BlqqVol(nq, nl, qmax)
blqq1.fill_from_corr(corr1)

corr2 = scorpy.CorrelationVol(nq, npsi, qmax)
corr2.fill_from_blqq(blqq1)


corr1.plot_q1q2()
plt.title('corr1 q1=q2')
blqq1.plot_q1q2()
plt.title('blqq q1=q2')
corr2.plot_q1q2()
plt.title('corr2 q1=q2')


corr1.plot_sumax()
plt.title('corr1 sumax')
blqq1.plot_sumax()
plt.title('blqq sumax')
corr2.plot_sumax()
plt.title('corr2 sumax')


plt.figure()
plt.hist(np.unique(corr1.vol))

plt.figure()
plt.hist(np.unique(corr2.vol))

plt.show()
