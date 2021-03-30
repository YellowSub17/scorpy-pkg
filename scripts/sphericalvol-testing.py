import scorpy
import numpy as np
import pyshtools as pysh
import matplotlib.pyplot as plt




n_angle = 30

extend = False
extend = True


grid_type = 'DH1'
grid_type = 'DH2'
grid_type = 'GLQ'

n_angles = [30]
extends  = [True, False]
# grid_types = ['DH1', 'DH2']
grid_types = ['DH2']

for n_angle in n_angles:
    for grid_type in grid_types:
        for extend in extends:
            print(f'\n\n#### Testing N:{n_angle}, Ex:{extend}, G:{grid_type}')



            sphvol = scorpy.SphericalVol(1, n_angle, grid_type=grid_type, extend=extend)

            lmax=sphvol.lmax


            coeffs = np.zeros( (2,lmax+1,lmax+1))

            coeffs[0,3,2] = 1

            coeffs_l6m3 = pysh.SHCoeffs.from_array(coeffs)
            expanded = coeffs_l6m3.expand(grid=grid_type,extend=extend)

            try:
                sphvol.vol[0,...] = expanded.data

            #     sphvol.plot_sumax()
                # plt.title(f'{n_angle}, {extend}, {grid_type}')

            except:

                print(f'\n\n####Error N:{n_angle}, Ex:{extend}, G:{grid_type}')
                print(f'sphvol shape: {sphvol.vol.shape}')
                print(f'expanded data shape: {expanded.data.shape}')
                print(f'sphvol lmax: {sphvol.lmax}')
                print(f'expanded: {expanded}')
                

# plt.show()

