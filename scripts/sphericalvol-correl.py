import scorpy
import numpy as np
import pyshtools as pysh
import matplotlib.pyplot as plt
from scorpy.utils import index_x_arr


plt.close('all')

n_angle = 180
# grid_type = 'DH2'
grid_type = 'GLQ'
extend=False


cif = scorpy.CifData('../data/xtal/1al1-sf.cif')
sphvol = scorpy.SphericalVol(256, n_angle,qmax=cif.qmax, grid_type=grid_type, extend=extend)

sphvol.fill_from_cif(cif)
# sphvol.pass_filter()
# sphvol.convolve(kern_L = 5, kern_n=11, std_x=2,std_y=2, std_z=2)


i = 190

shell1 = sphvol.vol[i,...]


#get theta sampling
lats, lons=  sphvol.get_angle_sampling()

#meshgrids of the theta and phi
tt1, pp1 = np.meshgrid(lons, lats)

#init plot for correlation
cor_t = np.zeros(n_angle)

#for every theta and phi index
for it in range(13,sphvol.ny):
    print(it,'/',sphvol.ny)
    for ip in range(0,sphvol.nz):

        #roll the theta, phi, and intensity matrices 
        tt2 = np.roll(tt1, (it,ip), (0,1))
        pp2 = np.roll(pp1, (it,ip), (0,1))
        shell2 = np.roll(shell1, (it,ip), (0,1))

        #angle between
        sin_terms = np.sin(tt1)*np.sin(tt2)
        cos_terms = np.cos(tt1)*np.cos(tt2)*np.cos(np.abs(pp1-pp2))
        arccos_term = sin_terms + cos_terms
        
        #condition arccos term
        arccos_term[np.where(arccos_term > 1)]=1
        arccos_term[np.where(arccos_term < -1)]=-1

        angle_between = np.arccos(arccos_term)

        indices = index_x_arr(angle_between,np.pi, n_angle)
        II = shell1*shell2
        ind_flat = indices.flatten()
        II_flat = II.flatten()
        np.add.at(cor_t, ind_flat, II_flat)


        break
    break


# plt.figure()
# plt.imshow(indices, origin='lower', extent=[0,np.pi*2,0,np.pi])
# plt.title('indices')


plt.figure()
plt.imshow(shell1, origin='lower', extent=[0,np.pi*2,0,np.pi])
plt.title('shell1')

plt.figure()
plt.imshow(shell2, origin='lower', extent=[0,np.pi*2,0,np.pi])
plt.title('shell2')

# plt.figure()
# plt.imshow(angle_between, origin='lower', extent=[0,np.pi*2,0,np.pi])


plt.figure()
plt.imshow(II, origin='lower', extent=[0,np.pi*2,0,np.pi])
plt.title('Correlation (shell1 * shell2)')

plt.figure()
plt.plot(cor_t)




plt.show()

