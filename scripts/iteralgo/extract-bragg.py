import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')





a_mag = 20
b_mag = 24.6
c_mag = 21.8
alpha = 90
beta = 90
gamma = 90

qmax = 1




c1= scorpy.CifData(a_mag=a_mag, b_mag=b_mag, c_mag=c_mag, alpha=alpha, beta=beta, gamma=gamma)

sphv_rand = scorpy.SphericalVol(qmax=qmax)
sphv_rand.vol = np.ones( sphv_rand.vol.shape)

c1.fill_from_sphv(sphv_rand)


c1.save(f'{scorpy.DATADIR}/cifs/x.cif')

# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# ax.scatter( c1.scat_bragg[:,0], c1.scat_bragg[:,1], c1.scat_bragg[:,2])

# sphv_bragg = scorpy.SphericalVol(qmax=qmax)
# sphv_bragg.fill_from_cif(c1)


# c2 = scorpy.CifData(a_mag=a_mag, b_mag=b_mag, c_mag=c_mag, alpha=alpha, beta=beta, gamma=gamma)
# c2.fill_from_sphv(sphv_bragg)


# loc = np.where(c1.scat_bragg != c2.scat_bragg)






# c1 = scorpy.CifData(path=f'{scorpy.DATADIR}/cifs/p1-rand0-sf.cif')

# sphv_x = scorpy.SphericalVol(qmax= c1.qmax)

# sphv_x.fill_from_cif(c1)

# c2 = scorpy.CifData(a_mag=c1.a_mag, b_mag=c1.b_mag, c_mag=c1.c_mag, 
                    # alpha=np.degrees(c1.alpha), beta=np.degrees(c1.beta), gamma=np.degrees(c1.gamma))

# c2.fill_from_sphv(sphv_x)



# loc = np.where(c1.scat_bragg != c2.scat_bragg)






plt.show()











