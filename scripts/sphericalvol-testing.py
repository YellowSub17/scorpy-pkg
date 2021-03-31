import scorpy
import numpy as np
import pyshtools as pysh
import matplotlib.pyplot as plt
from scorpy.utils import index_x_arr


plt.close('all')

n_angle = 180
grid_type = 'DH2'
# grid_type = 'GLQ'
extend=False


cif = scorpy.CifData('../data/xtal/1al1-sf.cif')
sphvol = scorpy.SphericalVol(256, n_angle,qmax=cif.qmax, grid_type=grid_type, extend=extend)

sphvol.fill_from_cif(cif)
# sphvol.pass_filter()
# sphvol.convolve(kern_L = 5, kern_n=11, std_x=2,std_y=2, std_z=2)


i = 190

shell1 = sphvol.vol[i,...]


lats, lons = sphvol.get_angle_sampling()


pp, tt = np.meshgrid(lons, lats)


cor_t = np.zeros(n_angle)



sin_terms = np.sin(0)*np.sin(0)
cos_terms = np.cos(0)*np.cos(0)*np.cos(pp)
angle_between = np.arccos(sin_terms + cos_terms)

indices_base = index_x_arr(angle_between,np.pi, n_angle)



for it1 in range(0,sphvol.ny):

    print(it1,'/',sphvol.ny)

    for ip1 in range(0,sphvol.nz):

#         sin_terms = np.sin(tt)*np.sin(lats[it1])
        # cos_terms = np.cos(tt)*np.cos(lats[it1])*np.cos(pp-lons[ip1])
        # angle_between = np.arccos(sin_terms + cos_terms)

        # indices = index_x_arr(angle_between,np.pi, n_angle)
        # indices[np.where(indices <0)] = 0

        indices = np.roll(indices_base, (it1,ip1), (0,1))

        shell2 = np.roll(shell1, (it1,ip1), (0,1))

        II = shell1*shell2


        ind_flat = indices.flatten()
        II_flat = II.flatten()

        loc = np.where(II_flat>0)
        
        ind_flat = ind_flat[loc]
        II_flat = II_flat[loc]
        
        for ind_val, II_val in zip(ind_flat, II_flat):
            cor_t[ind_val] +=II_val


        # break
    # break

# plt.figure()
# plt.imshow(angle_between, origin='lower', extent=[0,360,0,180])

# plt.figure()
# plt.imshow(indices, origin='lower', extent=[0,360,0,180])


plt.figure()
plt.imshow(shell1, origin='lower', extent=[0,360,0,180])

plt.figure()
plt.imshow(shell2, origin='lower', extent=[0,360,0,180])

plt.figure()
plt.imshow(II, origin='lower', extent=[0,360,0,180])

plt.figure()
plt.plot(cor_t)


# q_slice = sphvol.vol[i,...]
# ft_q_slice = np.fft.fft(q_slice)
# autocor = np.fft.ifft(ft_q_slice*np.conj(ft_q_slice))
# plt.figure()
# plt.imshow(np.abs(autocor))




# theta_space = np.linspace(0, np.pi,sphvol.ny)
# phi_space = np.linspace(0, 2*np.pi,sphvol.nz)
# for it1 in range(sphvol.ny):
    # print(it1,'/',sphvol.ny)
    # for ip1 in range(sphvol.nz):

        # theta1 = theta_space[it1]
        # phi1 = phi_space[ip1]

        # for it2 in range(sphvol.ny):
            # for ip2 in range(sphvol.nz):

                # theta2 = theta_space[it2]
                # phi2 = phi_space[ip2]

                # sin_terms = np.sin(theta1)*np.sin(theta2)
                # cos_terms = np.cos(theta1)*np.cos(theta2)*np.cos(theta1-theta2)

                # angle_between = np.arccos(sin_terms + cos_terms)

                # # print(angle_between)





plt.show()

