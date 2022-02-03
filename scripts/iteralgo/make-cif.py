import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')





a_mag = 42.156
b_mag = 53.122
c_mag = 54.809
alpha = 103.983
beta = 101.997
gamma = 100.048

qmax = 0.5




c1 = scorpy.CifData(a_mag=a_mag, b_mag=b_mag, c_mag=c_mag, alpha=alpha, beta=beta, gamma=gamma)

sphv_rand = scorpy.SphericalVol(qmax=qmax)
sphv_rand.vol = np.random.random( sphv_rand.vol.shape)

c1.fill_from_sphv(sphv_rand)

c1.save(f'{scorpy.DATADIR}/cifs/p1-inten-r0-sf.cif')





plt.show()











