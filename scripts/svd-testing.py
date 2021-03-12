import scorpy
import numpy as np
from scipy import special
import matplotlib.pyplot as plt

cor = scorpy.CorrelationVol(path=f'../data/dbins/1al1_qcor')

#get eigenvectors
bl = scorpy.BlqqVol(cor.nq, 17, cor.qmax)
bl.fill_from_corr(cor)




bl_l, bl_u = bl.get_eigh()




args = np.cos( np.linspace(0, np.pi,cor.ntheta ))

fmat = np.zeros( (cor.ntheta, bl.nl) )

for l in range(0, bl.nl, 2):
    leg_vals = (1/(4*np.pi))*special.eval_legendre(l, args)
    fmat[:,l] = leg_vals



fmat_inv = np.linalg.pinv(fmat)


plt.figure()
plt.imshow(fmat_inv)

u, s, vh = np.linalg.svd(fmat)

plt.figure()
plt.plot(s, 'x')
plt.xlabel('l')
plt.ylabel('Singular Values')
plt.title('Singular values of Fmat (with odds)')
plt.show()


