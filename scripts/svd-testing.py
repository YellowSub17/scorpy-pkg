import scorpy
import numpy as np
from scipy import special
import matplotlib.pyplot as plt



ntheta = 180
nl = 27

args = np.cos( np.linspace(0, np.pi,ntheta ))

fmat = np.zeros( (ntheta, nl) )

for l in range(0, nl):
    leg_vals = (1/(4*np.pi))*special.eval_legendre(l, args)
    fmat[:,l] = leg_vals


fmat_inv = np.linalg.pinv(fmat)


u, s, vh = np.linalg.svd(fmat)

plt.plot(s)
plt.xlabel('l')
plt.ylabel('Singular Values')
plt.title('Singular values of Fmat')
plt.show()


