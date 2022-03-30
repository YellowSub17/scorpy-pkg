
import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')









qmax = 9.0
nq = 256
ntheta = 360
nphi = 720

rotk = [1,1,1]
rottheta = np.radians(30)


cif_sf = scorpy.CifData(f'{scorpy.DATADIR}/xtal/agno3-sf.cif', qmax=qmax, rotk=rotk, rottheta=rottheta )
sphv1 = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv1.fill_from_cif(cif_sf)
sphv1.plot_slice(0, 240)


cif_xtal = scorpy.CifData(f'{scorpy.DATADIR}/xtal/agno3.cif', qmax=qmax, rotk=rotk, rottheta=rottheta )

cif_xtal.fill_from_sphv(sphv1, bragg_xyz=cif_sf.scat_bragg[:,:3])
# cif_xtal.fill_from_sphv(sphv1, bragg_xyz=None)






print(cif_sf.scat_bragg.shape)
print(cif_xtal.scat_bragg.shape)





# cif_sf = scorpy.CifData(f'{scorpy.DATADIR}/xtal/agno3-sf.cif', qmax=qmax)
# sphv1 = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
# sphv1.fill_from_cif(cif_sf)
# sphv1.make_mask()
# sphv1.plot_slice(0, 240)




plt.show()




